import os
from dotenv import load_dotenv, find_dotenv
from groq import Groq

# Load environment variables
load_dotenv(find_dotenv())

client = Groq(api_key=os.getenv("GROQ_API_KEY"))


def generate_ddr_report(inspection_text, thermal_text):
    prompt = f"""
You are a professional civil engineer preparing a Detailed Diagnostic Report (DDR).

Your goal is to generate a CLIENT-READY, DETAILED report — not a summary.
Return ONLY valid JSON.
Do NOT include:
- markdown
- ```json
- explanations
- text before or after JSON
STRICT RULES:
- Do NOT give short answers
- Each section must be 3–5 lines minimum
- Explain observations clearly
- Provide reasoning (why the issue is happening)
- Use thermal data as supporting evidence
- Avoid repetition
- If missing → write "Not Available"
- DO NOT include any text outside JSON

OUTPUT FORMAT (STRICT JSON ONLY):

{{
  "summary": "Detailed paragraph explaining overall condition",

  "areas": [
    {{
      "area": "Area name",

      "observation": "Detailed explanation of issue (not 1 line)",

      "root_cause": "Explain WHY the issue is happening (technical reasoning)",

      "evidence": "Support using inspection + thermal findings",

      "severity": "High / Medium / Low with reasoning",

      "recommendation": "Step-by-step practical repair actions"
    }}
  ],

  "additional_notes": "Detailed notes about risks and future impact",

  "missing_info": "Explicit missing data"
}}

Inspection Report:
{inspection_text}

Thermal Report:
{thermal_text}
"""

    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[
            {"role": "user", "content": prompt}
        ],
        temperature=0.2
    )

    return response.choices[0].message.content