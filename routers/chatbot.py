'''
Sample questions to ask the chatbot:
1. Am I suitable for this job?
2. What percentage match is my resume compared to this JD?
3. What are my strengths for this role?
4. What skills am I missing for this job?
5. How can I improve my resume for this specific JD?
6. Am I ready for this AI Engineer role?
7. Is my experience enough for this job level?
'''
from fastapi import APIRouter, UploadFile, Form
from fastapi.responses import JSONResponse
import pdfplumber
import google.generativeai as genai
from dotenv import load_dotenv
import os

load_dotenv()
api_key = os.getenv("API_KEY")
genai.configure(api_key=api_key)

model = genai.GenerativeModel("gemini-2.5-flash")

# Create router
router = APIRouter(prefix="/chatbot", tags=["Chatbot"])


# --------------------------
# PDF → TEXT
# --------------------------
def extract_pdf_text(file_path):
    text = ""
    with pdfplumber.open(file_path) as pdf:
        for page in pdf.pages:
            t = page.extract_text()
            if t:
                text += t + "\n"
    return text


# --------------------------
# LLM Answer Generator
# --------------------------
def answer_question(question, resume_text, jd_text):
    prompt = f"""
You are an expert career advisor AI.

--- RESUME ---
{resume_text}

--- JOB DESCRIPTION ---
{jd_text}

The user now asks:
{question}

Your job:
- Answer ONLY the question asked.
- Keep answer short, max 4–5 lines.
- If user asks "Am I suitable?", reply only suitability.
- No extra explanations.
- No long paragraphs.
- Direct, simple, precise.

"""

    resp = model.generate_content(prompt)
    return resp.text.strip()


# --------------------------
# FASTAPI ENDPOINT
# --------------------------
@router.post("")
async def ask_resume_question(
    resume_file: UploadFile,
    jd_text: str = Form(...),
    question: str = Form(...)
):
    # Save file temporarily
    temp_path = f"temp_{resume_file.filename}"
    with open(temp_path, "wb") as f:
        f.write(await resume_file.read())

    try:
        resume_text = extract_pdf_text(temp_path)

        answer = answer_question(question, resume_text, jd_text)

        return JSONResponse({
            "answer": answer
        })
    finally:
        # Clean up temp file
        try:
            if os.path.exists(temp_path):
                os.remove(temp_path)
        except Exception:
            pass  # Ignore deletion errors on Windows

