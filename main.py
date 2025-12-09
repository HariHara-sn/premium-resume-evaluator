# #---------------------------------------------------------------------------------------------------------
# # from fastapi import FastAPI, Form
# # from pydantic import BaseModel
# # from google import generativeai as genai
# from dotenv import load_dotenv
# import os
# load_dotenv()
# api_key = os.getenv("API_KEY")
# genai.configure(api_key=api_key)

# # model = genai.GenerativeModel("models/gemini-2.5-flash")

# # app = FastAPI()

# # class AIRequest(BaseModel):
# #     prompt: str


# # data = {
# #     "Hari" : "software engineer",
# #     "location" : "canada"
# # }
# # @app.post("/ai")
# # def ai(req: AIRequest):
# #     print("Received prompt:", req.prompt)
# #     response = model.generate_content(req.prompt)
# #     print("Generated response:", response.text)
# #     data["response"] = response.text
# #     return data
#---------------------------------------------------------------------------------------------------

#-----------------------------------------------------------------------------------------------------------
#below code is for direct JD and Resume parsing to LLM
import os
import json
import tempfile
from typing import List
from fastapi import FastAPI, File, UploadFile, Form
from pydantic import BaseModel
import pdfplumber
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()
api_key = os.getenv("API_KEY")
genai.configure(api_key=api_key)
gemini_model = genai.GenerativeModel("gemini-2.0-flash")

app = FastAPI(title="Resume Evaluator Clean Version")


# ---------------------------
# OUTPUT MODEL
# ---------------------------
class AnalyzeResult(BaseModel):
    verdict: str
    match_score: float
    missing_skills: List[str]
    one_tip: str
    improvements: List[dict]



def extract_text_from_pdf(path: str) -> str:
    text = ""
    with pdfplumber.open(path) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"
    return text


# ---------------------------
# LLM EVALUATION
# ---------------------------
def evaluate_resume_with_llm(resume_text: str, jd_text: str) -> dict:
    prompt = f"""
You are an expert resume evaluator. 
Your job is to MATCH the resume to the Job Description (JD) and output ONLY valid JSON.

-------------------------
RESUME:
{resume_text}

-------------------------
JOB DESCRIPTION:
{jd_text}

-------------------------
Return STRICT JSON in this format:

{{
  "verdict": "Shortlisted / Average / Rejected",
  "match_score": 0,
  "missing_skills": [],
  "one_tip": "",
  "improvements": [
    {{"area": "skill/experience/education", "suggestion": "specific improvement suggestion"}}
]
}}
Rules:
- match_score must be a number 0–100
- missing_skills: only JD-required skills missing in resume
- one_tip: single best improvement tip
- improvements: 2–4 specific improvement items
- DO NOT include any explanations or text outside the JSON
"""

    response = gemini_model.generate_content(prompt)
    raw = response.text.strip()

    # extract JSON properly
    json_start = raw.find("{")
    json_end = raw.rfind("}")
    clean_json = raw[json_start:json_end + 1]

    return json.loads(clean_json)



@app.post("/analyze", response_model=AnalyzeResult)
async def analyze_resume(
        jd_text: str = Form(...),
        resume_file: UploadFile = File(...)
):
    tmp = tempfile.NamedTemporaryFile(delete=False, suffix=".pdf")
    tmp.write(await resume_file.read())
    tmp.flush()

    resume_text = extract_text_from_pdf(tmp.name)

    result = evaluate_resume_with_llm(resume_text, jd_text)

    return result



if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)