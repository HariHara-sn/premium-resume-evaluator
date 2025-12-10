from fastapi import APIRouter, UploadFile, File, Form, HTTPException
from fastapi.responses import JSONResponse
import pdfplumber
import google.generativeai as genai
import json
import re
import tempfile
import os
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("API_KEY")
if not API_KEY:
    raise RuntimeError("API_KEY not found in environment. Set it in .env")

genai.configure(api_key=API_KEY)
model = genai.GenerativeModel("gemini-2.5-flash")

# Create router
router = APIRouter(prefix="/interview-questions", tags=["Interview Questions"])


def extract_text_from_pdf(pdf_path: str) -> str:
    text = ""
    try:
        with pdfplumber.open(pdf_path) as pdf:
            for page in pdf.pages:
                t = page.extract_text()
                if t:
                    text += t + "\n"
    except Exception as e:
        raise RuntimeError(f"Failed to read PDF: {e}")
    return text.strip()


def generate_interview_questions(resume_text: str, jd_text: str) -> dict:
    prompt = f"""
You are an expert Technical Interview Panel Lead.

Generate crisp, 1-line questions based on:

- Candidate's Resume
- Job Description
- Projects + Skills

Output STRICT JSON ONLY in this format:

{{
  "technical_questions": [],
  "project_questions": [],
  "cs_fundamentals_questions": [],
  "behavioral_questions": []
}}

Rules:
- One-line questions only.
- No hallucinations.
- Must relate to Resume + JD.
- Ask realistic interview questions.

Resume:
{resume_text}

Job Description:
{jd_text}
"""
    response = model.generate_content(prompt)
    raw = response.text.strip()
    # remove code fences if any
    raw = re.sub(r"^```(?:json)?\s*\n?", "", raw)
    raw = re.sub(r"\n?```\s*$", "", raw)
    # try to parse JSON
    try:
        parsed = json.loads(raw)
    except json.JSONDecodeError as e:
        # return debugging info but preserve JSON response structure
        raise RuntimeError(f"LLM returned invalid JSON: {e}\nRaw output:\n{raw}")
    return parsed


@router.post("/generate")
async def generate_questions_api(
    resume_file: UploadFile = File(...),
    jd_text: str = Form(...)
):
    # Validate file
    if not resume_file.filename.lower().endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDF files are supported for resume_file")

    # Save uploaded file to a temp file
    tmp = tempfile.NamedTemporaryFile(delete=False, suffix=".pdf")
    tmp_path = tmp.name
    try:
        tmp.write(await resume_file.read())
        tmp.flush()
        tmp.close()

        # Extract text
        resume_text = extract_text_from_pdf(tmp_path)

        # Call LLM and generate questions
        result = generate_interview_questions(resume_text, jd_text)

        return JSONResponse(content=result)

    except RuntimeError as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        # cleanup temp file
        try:
            if os.path.exists(tmp_path):
                os.remove(tmp_path)
        except Exception:
            pass

