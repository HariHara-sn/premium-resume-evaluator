# interview_api.py
from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
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

app = FastAPI(title="AI Interview Question Generator")

# Optional: allow CORS for local frontends
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # restrict in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


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

- Candidate’s Resume
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


@app.post("/generate-interview-questions")
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


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("interview_question_generator:app", host="0.0.0.0", port=8000, reload=True)

## Below is raw code without postman
# import pdfplumber
# import google.generativeai as genai
# import json
# from dotenv import load_dotenv
# import os
# load_dotenv()
# api_key = os.getenv("API_KEY")
# genai.configure(api_key=api_key)

# model = genai.GenerativeModel("gemini-2.0-flash")


# # ------------------------
# # PDF → TEXT
# # ------------------------
# def extract_text_from_pdf(pdf_path):
#     text = ""
#     with pdfplumber.open(pdf_path) as pdf:
#         for page in pdf.pages:
#             page_text = page.extract_text()
#             if page_text:
#                 text += page_text + "\n"
#     return text.strip()


# # ------------------------
# # Predict Interview Questions
# # ------------------------
# def generate_interview_questions(resume_text, jd_text):
#     prompt = f"""
# You are an expert Technical Interview Panel Lead.

# Generate crisp, multiple 1-line interview questions based on:

# - The candidate's resume
# - The job description
# - Their skills, projects, tools, and responsibilities
# - The depth of expertise implied in resume

# OUTPUT STRICT JSON ONLY in this format:

# {{
#   "technical_questions": [],
#   "project_questions": [],
#   "cs_fundamentals_questions": [],
#   "behavioral_questions": []
# }}

# Rules:
# - No long questions. One-line only.
# - Must be realistic to what interviewers truly ask.
# - ALL questions MUST be related to resume + JD.
# - NO hallucinations or made-up technologies.
# - If a skill is mentioned in JD but not in resume, ask at beginner level.
# - Focus more on candidate’s actual projects and experience.

# Resume:
# {resume_text}

# Job Description:
# {jd_text}
# """

#     response = model.generate_content(prompt)

#     raw = response.text.strip().replace("```json", "").replace("```", "")
#     return json.loads(raw)


# # ------------------------
# # MAIN TEST
# # ------------------------
# if __name__ == "__main__":
#     resume_pdf = "C:\\Users\\ACER\\Documents\\resumes\\HariHaraSudhan-AI-Resume.pdf"
#     jd_text = """We are looking for a skilled AI Developer to join our team. The ideal candidate will have experience in designing, developing, and deploying AI and Machine Learning models. Responsibilities include:

# - Develop and fine-tune machine learning models using Python and frameworks like PyTorch or TensorFlow.
# - Build and maintain AI-powered applications and APIs.
# - Collaborate with data engineers and product teams to integrate ML solutions.
# - Conduct research to implement state-of-the-art AI techniques.
# - Optimize models for performance and scalability.
# - Write clean, maintainable code and documentation.

# Required Skills:

# - Strong proficiency in Python.
# - Experience with machine learning frameworks (TensorFlow, PyTorch, scikit-learn).
# - Knowledge of NLP and computer vision techniques.
# - Experience with APIs and web frameworks (FastAPI, Flask).
# - Familiarity with cloud platforms (AWS, GCP, Azure) is a plus.
# - Good understanding of data structures, algorithms, and software engineering best practices.
# """

#     print("\nExtracting resume...")
#     resume_text = extract_text_from_pdf(resume_pdf)

#     print("Generating interview questions...")
#     questions = generate_interview_questions(resume_text, jd_text)

#     print("\nPredicted Interview Questions:")
#     print(json.dumps(questions, indent=2))
