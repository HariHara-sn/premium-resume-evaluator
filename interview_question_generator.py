import pdfplumber
import google.generativeai as genai
import json
from dotenv import load_dotenv
import os
load_dotenv()
api_key = os.getenv("API_KEY")
genai.configure(api_key=api_key)

model = genai.GenerativeModel("gemini-2.0-flash")


# ------------------------
# PDF → TEXT
# ------------------------
def extract_text_from_pdf(pdf_path):
    text = ""
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"
    return text.strip()


# ------------------------
# Predict Interview Questions
# ------------------------
def generate_interview_questions(resume_text, jd_text):
    prompt = f"""
You are an expert Technical Interview Panel Lead.

Generate crisp, multiple 1-line interview questions based on:

- The candidate's resume
- The job description
- Their skills, projects, tools, and responsibilities
- The depth of expertise implied in resume

OUTPUT STRICT JSON ONLY in this format:

{{
  "technical_questions": [],
  "project_questions": [],
  "cs_fundamentals_questions": [],
  "behavioral_questions": []
}}

Rules:
- No long questions. One-line only.
- Must be realistic to what interviewers truly ask.
- ALL questions MUST be related to resume + JD.
- NO hallucinations or made-up technologies.
- If a skill is mentioned in JD but not in resume, ask at beginner level.
- Focus more on candidate’s actual projects and experience.

Resume:
{resume_text}

Job Description:
{jd_text}
"""

    response = model.generate_content(prompt)

    raw = response.text.strip().replace("```json", "").replace("```", "")
    return json.loads(raw)


# ------------------------
# MAIN TEST
# ------------------------
if __name__ == "__main__":
    resume_pdf = "C:\\Users\\ACER\\Documents\\resumes\\HariHaraSudhan-AI-Resume.pdf"
    jd_text = """We are looking for a skilled AI Developer to join our team. The ideal candidate will have experience in designing, developing, and deploying AI and Machine Learning models. Responsibilities include:

- Develop and fine-tune machine learning models using Python and frameworks like PyTorch or TensorFlow.
- Build and maintain AI-powered applications and APIs.
- Collaborate with data engineers and product teams to integrate ML solutions.
- Conduct research to implement state-of-the-art AI techniques.
- Optimize models for performance and scalability.
- Write clean, maintainable code and documentation.

Required Skills:

- Strong proficiency in Python.
- Experience with machine learning frameworks (TensorFlow, PyTorch, scikit-learn).
- Knowledge of NLP and computer vision techniques.
- Experience with APIs and web frameworks (FastAPI, Flask).
- Familiarity with cloud platforms (AWS, GCP, Azure) is a plus.
- Good understanding of data structures, algorithms, and software engineering best practices.
"""

    print("\nExtracting resume...")
    resume_text = extract_text_from_pdf(resume_pdf)

    print("Generating interview questions...")
    questions = generate_interview_questions(resume_text, jd_text)

    print("\nPredicted Interview Questions:")
    print(json.dumps(questions, indent=2))
