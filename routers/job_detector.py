from fastapi import APIRouter, UploadFile, File
import pdfplumber
import google.generativeai as genai
import json
import re
import tempfile
import os
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("API_KEY")
genai.configure(api_key=api_key)

model = genai.GenerativeModel("gemini-2.5-flash")

router = APIRouter(prefix="/job-detector", tags=["Job Detector"])


def extract_text(pdf_path):
    text = ""
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"
    return text


def detect_job_role(resume_text):
    prompt = f"""
You are an expert HR recruiter and job classification system.

Your task:
Analyze the candidate resume and predict the TOP 5 most suitable job roles.

Return output in STRICT JSON ONLY with this format:

{{
  "primary_role": "", 
  "roles": [
    {{"role": "", "confidence": ""}}
  ],
  "skills_detected": []
}}

Rules:
- confidence is a % value (like "92%")
- roles must be real job titles
- do NOT hallucinate skills not found in resume
- JSON ONLY. No extra comments.

Resume:
{resume_text}
"""

    response = model.generate_content(prompt)
    output = response.text

    output = re.sub(r'^```(?:json)?\s*\n?', '', output)
    output = re.sub(r'\n?```\s*$', '', output)

    return json.loads(output)


@router.post("")
async def job_detector_api(file: UploadFile = File(...)):
    # Save uploaded file temporarily
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as temp_file:
        temp_file.write(await file.read())
        temp_path = temp_file.name

    try:
        resume_text = extract_text(temp_path)

        result = detect_job_role(resume_text)

        return result
    finally:
        # Clean up temp file
        try:
            if os.path.exists(temp_path):
                os.remove(temp_path)
        except Exception:
            pass  # Ignore deletion errors on Windows

