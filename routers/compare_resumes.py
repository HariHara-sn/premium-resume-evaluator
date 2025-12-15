import pdfplumber
import google.generativeai as genai
import json
from fastapi import APIRouter, UploadFile, File
from typing import List
from dotenv import load_dotenv
import os

load_dotenv()
api_key = os.getenv("API_KEY")
genai.configure(api_key=api_key)

model = genai.GenerativeModel("gemini-2.5-flash")

router = APIRouter(prefix="/compare-resumes", tags=["Resume Comparison"])



def extract_text_from_pdf(file_bytes):
    file_bytes.seek(0)  # IMPORTANT
    text = ""
    with pdfplumber.open(file_bytes) as pdf:
        for page in pdf.pages:
            p = page.extract_text()
            if p:
                text += p + "\n"
    return text.strip()

def compare_resumes(resume_dict):

    prompt = f"""
You are an expert ATS evaluator and career analyst.

Compare ALL resumes provided.  
There is NO Job Description.

Analyze each resume based on:
- Clarity
- ATS friendliness
- Strong action verbs
- Skill depth
- Project relevance
- Structure & formatting
- Technical strength
- Overall completeness

Give EACH resume a score out of 100.

OUTPUT STRICT JSON ONLY:

{{
  "scores": {{
      "resume_1_name": 0,
      "resume_2_name": 0,
      "resume_3_name": 0
  }},
  "best_resume": "",
  "reason": ""
}}

Rules:
- No hallucination
- Score only based on provided resume content
- No markdown
- No extra explanation

Resumes Provided:
{json.dumps(resume_dict, indent=2)}
"""

    response = model.generate_content(prompt)

    clean = response.text.replace("```json", "").replace("```", "").strip()

    return json.loads(clean)


@router.post("")
async def compare_resumes_api(files: List[UploadFile] = File(...)):
    resume_text_map = {}

    for file in files:
        text = extract_text_from_pdf(file.file)
        resume_text_map[file.filename] = text

    result = compare_resumes(resume_text_map)
    return result

