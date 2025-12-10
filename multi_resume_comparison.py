import pdfplumber
import google.generativeai as genai
import json
from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
import os
from typing import List

load_dotenv()
api_key = os.getenv("API_KEY")
genai.configure(api_key=api_key)

model = genai.GenerativeModel("gemini-2.5-flash")

app = FastAPI()

# Allow CORS clients (Postman, browser)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ------------------------
# Extract text from PDF
# ------------------------
def extract_text_from_pdf(file_bytes):
    file_bytes.seek(0)  # IMPORTANT
    text = ""
    with pdfplumber.open(file_bytes) as pdf:
        for page in pdf.pages:
            p = page.extract_text()
            if p:
                text += p + "\n"
    return text.strip()


# ------------------------
# Compare resumes with Gemini
# ------------------------
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


# ------------------------
# API endpoint
# ------------------------
@app.post("/compare-resumes")
async def compare_resumes_api(files: List[UploadFile] = File(...)):
    resume_text_map = {}

    for file in files:
        text = extract_text_from_pdf(file.file)
        resume_text_map[file.filename] = text

    result = compare_resumes(resume_text_map)
    return result


# ------------------------
# Run FastAPI
# ------------------------
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("multi_resume_comparison:app", host="0.0.0.0", port=8000, reload=True)


#Basic code without FastAPI
# import pdfplumber
# import google.generativeai as genai
# import json


# from dotenv import load_dotenv
# import os
# load_dotenv()
# api_key = os.getenv("API_KEY")
# genai.configure(api_key=api_key)

# model = genai.GenerativeModel("gemini-2.5-flash")


# # ------------------------
# # Extract PDF Text
# # ------------------------
# def extract_text(pdf_path):
#     text = ""
#     with pdfplumber.open(pdf_path) as pdf:
#         for page in pdf.pages:
#             page_text = page.extract_text()
#             if page_text:
#                 text += page_text + "\n"
#     return text.strip()


# # ------------------------
# # Multi Resume Comparison
# # ------------------------
# def compare_resumes(resume_dict):
#     """
#     resume_dict = {
#         "hari_ai_resume.pdf": "text...",
#         "hari_softwaredev_resume.pdf": "text...",
#         "hari_ml_dl_resume.pdf": "text..."
#     }
#     """

#     prompt = f"""
# You are an expert ATS evaluator and career analyst.

# Compare ALL resumes provided.  
# There is NO Job Description for this feature.

# Analyze each resume based on:
# - Clarity
# - ATS friendliness
# - Strong action verbs
# - Skill depth
# - Project relevance
# - Structure & formatting
# - Technical strength
# - Overall completeness

# Give EACH resume a score out of 100.

# OUTPUT STRICT JSON ONLY:

# {{
#   "scores": {{
#       "resume_1_name": 0,
#       "resume_2_name": 0,
#       "resume_3_name": 0
#   }},
#   "best_resume": "",
#   "reason": ""
# }}

# Rules:
# - No hallucination
# - Score only based on provided resume content
# - Be objective
# - Select the best resume with clear reasoning
# - No markdown
# - No extra text

# Resumes Provided:
# {json.dumps(resume_dict, indent=2)}
# """

#     response = model.generate_content(prompt)
#     cleaned = response.text.strip().replace("```json", "").replace("```", "")
#     return json.loads(cleaned)


# # ------------------------
# # MAIN TEST
# # ------------------------
# if __name__ == "__main__":

#     resumes = [
#         r"C:\Users\ACER\Documents\resumes\HariHaraSudhan-AI-Resume.pdf",
#         r"C:\Users\ACER\Documents\resumes\Hari-Software Developer-Resume.pdf",
#         r"C:\Users\ACER\Documents\resumes\Guruprasath_v_Resume (2).pdf"
#     ]

#     print("\nExtracting multiple resumes...")
#     resume_text_map = {}

#     for res in resumes:
#         print(f"Reading {res}")
#         resume_text_map[res] = extract_text(res)

#     print("\nComparing resumes...")
#     result = compare_resumes(resume_text_map)

#     print("\nMULTI RESUME COMPARISON RESULT:\n")
#     print(json.dumps(result, indent=2))
