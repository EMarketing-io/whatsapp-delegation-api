import uuid
import difflib
import traceback
from employee import load_employee_data
from utils import get_india_timestamp


def fuzzy_lookup(name, employee_data):
    if not name:
        return "", ""
    normalized = name.strip().lower()
    matches = difflib.get_close_matches(
        normalized, [n.lower() for n in employee_data], n=1, cutoff=0.6
    )
    if matches:
        original_name = next(
            orig for orig in employee_data if orig.lower() == matches[0]
        )
        return original_name, employee_data[original_name]
    return "", ""


def parse_structured_output(structured_output, choice, source_link=""):
    try:
        print("🔍 Raw structured_output:", structured_output)
        employee_data = load_employee_data()
        rows = []
        lines = structured_output.strip().split("\n")

        source_segments = []
        if choice in ["audio", "text"] and source_link:
            source_segments = [
                s.strip() for s in source_link.strip().split("\n") if s.strip()
            ]

        for line in lines:
            try:
                if line.strip() == "" or "---" in line:
                    continue
                if "Task Description" in line and "Employee Name" in line:
                    continue

                if "|" in line:
                    parts = [p.strip() for p in line.split("|")]
                    parts = parts[1:-1]  # Trim table edges

                    if len(parts) >= 3:
                        while len(parts) < 9:
                            parts.append("")

                        task_id = uuid.uuid4().hex[:8]

                        emp_name_raw = parts[1]
                        emp_name, emp_email = fuzzy_lookup(emp_name_raw, employee_data)

                        assigned_name_raw = parts[8]
                        assigned_name, assigned_email = fuzzy_lookup(
                            assigned_name_raw, employee_data
                        )

                        matched_source = ""
                        if source_segments:
                            best_match = difflib.get_close_matches(
                                parts[0], source_segments, n=1, cutoff=0.3
                            )
                            if best_match:
                                matched_source = best_match[0]

                        row_data = [
                            get_india_timestamp(),
                            task_id,
                            parts[0],
                            emp_name,
                            emp_email,
                            parts[2],
                            parts[3],
                            parts[4],
                            parts[5],
                            parts[6],
                            assigned_name,
                            assigned_email,
                            parts[7],
                            matched_source or source_link,
                        ]

                        rows.append(row_data)

            except Exception as row_error:
                print("⚠️ Error parsing line:", line)
                print("⚠️ Exception:", str(row_error))
                traceback.print_exc()

        print("✅ Returning rows:", rows)
        return rows

    except Exception as e:
        print("❌ Error inside parse_structured_output:", str(e))
        traceback.print_exc()
        return []
