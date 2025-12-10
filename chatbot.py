'''
Sample questions to ask the chatbot:
1.Am I suitable for this job?
2.What percentage match is my resume compared to this JD?
3.What are my strengths for this role?
4.What skills am I missing for this job?
5.How can I improve my resume for this specific JD?
6.Am I ready for this AI Engineer role?
7.Is my experience enough for this job level?
'''
from fastapi import FastAPI, UploadFile, Form
from fastapi.responses import JSONResponse
import pdfplumber
import google.generativeai as genai
from dotenv import load_dotenv
import os
import uvicorn

load_dotenv()
api_key = os.getenv("API_KEY")
genai.configure(api_key=api_key)

model = genai.GenerativeModel("gemini-2.5-flash")

app = FastAPI()


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
- If user asks “Am I suitable?”, reply only suitability.
- No extra explanations.
- No long paragraphs.
- Direct, simple, precise.

"""

    resp = model.generate_content(prompt)
    return resp.text.strip()


# --------------------------
# FASTAPI ENDPOINT
# --------------------------
@app.post("/chatbot")
async def ask_resume_question(
    resume_file: UploadFile,
    jd_text: str = Form(...),
    question: str = Form(...)
):

    # Save file temporarily
    temp_path = f"temp_{resume_file.filename}"
    with open(temp_path, "wb") as f:
        f.write(await resume_file.read())

    # Extract text
    resume_text = extract_pdf_text(temp_path)

    # Ask LLM
    answer = answer_question(question, resume_text, jd_text)

    return JSONResponse({
        "answer": answer
    })


# --------------------------
# RUN SERVER
# --------------------------
if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)

#below is just run python file
# import pdfplumber
# import google.generativeai as genai
# from dotenv import load_dotenv
# import os
# load_dotenv()
# api_key = os.getenv("API_KEY")
# genai.configure(api_key=api_key)

# model = genai.GenerativeModel("gemini-2.0-flash")


# # --------------------------
# # EXTRACT TEXT FROM PDF
# # --------------------------
# def extract_text_from_pdf(path):
#     text = ""
#     with pdfplumber.open(path) as pdf:
#         for page in pdf.pages:
#             t = page.extract_text()
#             if t:
#                 text += t + "\n"
#     return text


# # --------------------------
# # LLM ANSWER GENERATOR
# # --------------------------
# def answer_question(question, resume_text, jd_text):
#     prompt = f"""
# You are an expert career advisor AI.

# You are given:

# --- RESUME ---
# {resume_text}

# --- JOB DESCRIPTION ---
# {jd_text}

# The user now asks:
# {question}

# Your task:
# - Give helpful, accurate answers.
# - Compare resume to JD when needed.
# - Identify strengths, missing skills, improvements.
# - Keep the answer short (2–3 paragraphs).
# """

#     try:
#         response = model.generate_content(prompt)
#         return response.text.strip()
#     except Exception as e:
#         return f"Error: {str(e)}"


# # --------------------------------------------------
# # MAIN PROGRAM (NO API)
# # --------------------------------------------------
# if __name__ == "__main__":

#     # ---- Load Resume ----
#     resume_path = r"C:\Users\ACER\Documents\resumes\HariHaraSudhan-AI-Resume.pdf"
#     print("\nExtracting resume...")
#     resume_text = extract_text_from_pdf(resume_path)

#     # ---- Sample JD (Paste Any JD here) ----
#     jd_text = """
# We are looking for an AI/ML Engineer with experience in Python, FastAPI, 
# Machine Learning, Deep Learning, Pandas, PyTorch, TensorFlow, SQL, AWS, Data Pipelines,
# Model Deployment, API development, and problem-solving skills.
# """

#     print("Resume & JD loaded successfully.\n")

#     # ---- Query Loop ----
#     print("💬 Ask anything about your Resume or JD! (type 'exit' to quit)\n")

#     while True:
#         user_q = input("\nYour Question: ")

#         if user_q.lower() in ["exit", "quit", "bye"]:
#             print("\nThank you! Chat ended.")
#             break

#         answer = answer_question(user_q, resume_text, jd_text)
#         print("\nAI Answer:\n", answer)




