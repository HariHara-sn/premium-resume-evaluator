# import pdfplumber
# import google.generativeai as genai
# import re
# import json
# from dotenv import load_dotenv
# import os
# load_dotenv()
# api_key = os.getenv("API_KEY")
# genai.configure(api_key=api_key)
# model = genai.GenerativeModel("gemini-2.5-flash")


# # --------------------------
# # Extract Resume Text
# # --------------------------
# def extract_text(pdf_path):
#     text = ""
#     with pdfplumber.open(pdf_path) as pdf:
#         for page in pdf.pages:
#             t = page.extract_text()
#             if t:
#                 text += t + "\n"
#     return text


# # --------------------------
# # JOB DETECTOR USING LLM
# # --------------------------
# def detect_job_role(resume_text):
#     prompt = f"""
# You are an expert HR recruiter and job classification system.

# Your task:
# Analyze the candidate resume and predict the TOP 5 most suitable job roles.

# Return output in STRICT JSON ONLY with this format:

# {{
#   "primary_role": "", 
#   "roles": [
#     {{"role": "", "confidence": ""}}
#   ],
#   "skills_detected": []
# }}

# Rules:
# - confidence is a % value (like "92%")
# - roles must be real job titles
# - do NOT hallucinate skills not found in resume
# - JSON ONLY. No extra comments.

# Resume:
# {resume_text}
# """

#     response = model.generate_content(prompt)
#     output = response.text

#     # remove accidental markdown
#     output = re.sub(r'^```(?:json)?\s*\n?', '', output)
#     output = re.sub(r'\n?```\s*$', '', output)

#     return json.loads(output)


# # --------------------------
# # MAIN
# # --------------------------
# if __name__ == "__main__":
#     resume_file = "C:\\Users\\ACER\\Documents\\resumes\\HariHaraSudhan-AI-Resume.pdf"

#     print("\nExtracting resume text...")
#     text = extract_text(resume_file)

#     print("Detecting job roles...")
#     result = detect_job_role(text)

#     print("\n=== JOB DETECTOR OUTPUT ===")
#     print(json.dumps(result, indent=4))

## below is from postman
from fastapi import FastAPI, UploadFile, File
import pdfplumber
import google.generativeai as genai
import json
import re
import tempfile
from dotenv import load_dotenv
import os

# Load API key
load_dotenv()
api_key = os.getenv("API_KEY")
genai.configure(api_key=api_key)

model = genai.GenerativeModel("gemini-2.5-flash")

app = FastAPI()


# --------------------------
# Extract Resume Text
# --------------------------
def extract_text(pdf_path):
    text = ""
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"
    return text


# --------------------------
# JOB DETECTOR USING LLM
# --------------------------
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

    # Clean accidental markdown
    output = re.sub(r'^```(?:json)?\s*\n?', '', output)
    output = re.sub(r'\n?```\s*$', '', output)

    return json.loads(output)


# --------------------------
# FASTAPI ENDPOINT
# --------------------------
@app.post("/job-detector")
async def job_detector_api(file: UploadFile = File(...)):
    # Save uploaded file temporarily
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as temp_file:
        temp_file.write(await file.read())
        temp_path = temp_file.name

    # Extract text
    resume_text = extract_text(temp_path)

    # LLM processing
    result = detect_job_role(resume_text)

    return result
# run as (venv) PS D:\FastApi> uvicorn job_detector:app --reload