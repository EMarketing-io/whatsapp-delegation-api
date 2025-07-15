import uuid
from datetime import datetime
from employee import load_employee_data
import difflib
from utils import get_india_timestamp


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
            if line.strip() == "" or "---" in line:
                continue
            if "Task Description" in line and "Employee Name" in line:
                continue

            if "|" in line:
                parts = [p.strip() for p in line.split("|")]
                parts = parts[1:-1]  # Remove leading/trailing blank splits

                if len(parts) >= 3:
                    while len(parts) < 9:
                        parts.append("")

                    task_id = uuid.uuid4().hex[:8]
                    emp_name = parts[1]
                    emp_email = employee_data.get(emp_name, "")
                    assigned_name = parts[8]
                    assigned_email = employee_data.get(assigned_name, "")

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

        print("✅ Returning rows:", rows)
        return rows

    except Exception as e:
        print("❌ Error inside parse_structured_output:", str(e))
        return []
