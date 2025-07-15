import openai
from config import OPENAI_API_KEY

openai.api_key = OPENAI_API_KEY


def extract_tasks(transcription):
    system_prompt = """
You are an assistant that extracts structured task lists from either paragraph descriptions or field-based task inputs.

The input may be:
- A paragraph like: "Assign Apurvi to design a media plan for iCraft by July 14."
- Or a labeled list like:
  Task Description: Media Plan
  Employee Name: Apurvi Jain
  Target Date: 14-7
  Priority: Medium

Your job is to convert the input into a Markdown table with **exactly 9 columns**:

1. Task Description  
2. Employee Name  
3. Target Date  
4. Priority (High/Medium/Low/Urgent)  
5. Approval Needed (Yes/No)  
6. Client Name  
7. Department  
8. Comments  
9. Assigned By

⚠️ Rules:
- If any field is missing, leave the column blank.
- Never write explanations, just return the table.
- Handle mixed Hindi/English if needed.
- Always output a table even if only one task is found.
"""

    user_prompt = f"""Transcript:
{transcription}
"""

    response = openai.ChatCompletion.create(
        model="gpt-4.1-2025-04-14",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
        temperature=0.2,
    )
    return response["choices"][0]["message"]["content"]
