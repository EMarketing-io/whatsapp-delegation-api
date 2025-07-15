import uuid
import difflib
from employee import load_employee_data
from utils import get_india_timestamp


def parse_structured_output(structured_output, choice, source_link=""):
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

        if any(d in line for d in ["|", "\t", ","]):
            if "|" in line:
                parts = [p.strip() for p in line.split("|") if p.strip()]
            elif "\t" in line:
                parts = [p.strip() for p in line.split("\t") if p.strip()]
            else:
                parts = [p.strip() for p in line.split(",") if p.strip()]

            if len(parts) >= 3:  # At least Task, Employee Name, Target Date
                while len(parts) < 9:
                    parts.append("")  # Pad missing fields

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
                    get_india_timestamp(),  # Timestamp
                    task_id,  # Task ID
                    parts[0],  # Task Description
                    emp_name,  # Employee Name
                    emp_email,  # Email ID
                    parts[2],  # Target Date
                    parts[3],  # Priority
                    parts[4],  # Approval Needed
                    parts[5],  # Client Name
                    parts[6],  # Department
                    assigned_name,  # Assigned By
                    assigned_email,  # Assigned By Email
                    parts[7],  # Comments
                    matched_source or source_link,  # Source Link
                ]

                rows.append(row_data)

    return rows
