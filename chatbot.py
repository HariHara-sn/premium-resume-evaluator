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
import pdfplumber
import google.generativeai as genai
from dotenv import load_dotenv
import os
load_dotenv()
api_key = os.getenv("API_KEY")
genai.configure(api_key=api_key)

model = genai.GenerativeModel("gemini-2.0-flash")


# --------------------------
# EXTRACT TEXT FROM PDF
# --------------------------
def extract_text_from_pdf(path):
    text = ""
    with pdfplumber.open(path) as pdf:
        for page in pdf.pages:
            t = page.extract_text()
            if t:
                text += t + "\n"
    return text


# --------------------------
# LLM ANSWER GENERATOR
# --------------------------
def answer_question(question, resume_text, jd_text):
    prompt = f"""
You are an expert career advisor AI.

You are given:

--- RESUME ---
{resume_text}

--- JOB DESCRIPTION ---
{jd_text}

The user now asks:
{question}

Your task:
- Give helpful, accurate answers.
- Compare resume to JD when needed.
- Identify strengths, missing skills, improvements.
- Keep the answer short (2–3 paragraphs).
"""

    try:
        response = model.generate_content(prompt)
        return response.text.strip()
    except Exception as e:
        return f"Error: {str(e)}"


# --------------------------------------------------
# MAIN PROGRAM (NO API)
# --------------------------------------------------
if __name__ == "__main__":

    # ---- Load Resume ----
    resume_path = r"C:\Users\ACER\Documents\resumes\HariHaraSudhan-AI-Resume.pdf"
    print("\nExtracting resume...")
    resume_text = extract_text_from_pdf(resume_path)

    # ---- Sample JD (Paste Any JD here) ----
    jd_text = """
We are looking for an AI/ML Engineer with experience in Python, FastAPI, 
Machine Learning, Deep Learning, Pandas, PyTorch, TensorFlow, SQL, AWS, Data Pipelines,
Model Deployment, API development, and problem-solving skills.
"""

    print("Resume & JD loaded successfully.\n")

    # ---- Query Loop ----
    print("💬 Ask anything about your Resume or JD! (type 'exit' to quit)\n")

    while True:
        user_q = input("\nYour Question: ")

        if user_q.lower() in ["exit", "quit", "bye"]:
            print("\nThank you! Chat ended.")
            break

        answer = answer_question(user_q, resume_text, jd_text)
        print("\nAI Answer:\n", answer)






# """
# Resume & JD Chatbot System
# Supports natural language queries about resume, JD, and career readiness
# """

# import os
# import json
# import tempfile
# import uuid
# from typing import Optional, Dict
# from fastapi import FastAPI, File, UploadFile, Form, HTTPException
# from fastapi.middleware.cors import CORSMiddleware
# from pydantic import BaseModel
# import pdfplumber
# import google.generativeai as genai

# # ---------------------------
# # GEMINI CONFIG
# # ---------------------------
# genai.configure(api_key="AIzaSyBs9JPqB5FgPTAxSk0Xd75QrMLwmfhI81Q")
# gemini_model = genai.GenerativeModel("gemini-2.0-flash")

# app = FastAPI(title="Resume & JD Chatbot")

# # ---------------------------
# # CORS MIDDLEWARE (for React frontend)
# # ---------------------------
# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["http://localhost:3000", "http://localhost:3001"],
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )

# # ---------------------------
# # IN-MEMORY STORAGE (can be replaced with database)
# # ---------------------------
# # Store resume and JD text by session_id
# sessions: Dict[str, Dict[str, str]] = {}


# # ---------------------------
# # PYDANTIC MODELS
# # ---------------------------
# class ChatRequest(BaseModel):
#     question: str
#     session_id: Optional[str] = None


# class ChatResponse(BaseModel):
#     answer: str
#     session_id: str


# class UploadResponse(BaseModel):
#     message: str
#     session_id: str


# # ---------------------------
# # HELPER FUNCTIONS
# # ---------------------------
# def extract_text_from_pdf(path: str) -> str:
#     """Extract text from PDF file"""
#     text = ""
#     try:
#         with pdfplumber.open(path) as pdf:
#             for page in pdf.pages:
#                 page_text = page.extract_text()
#                 if page_text:
#                     text += page_text + "\n"
#     except Exception as e:
#         raise HTTPException(status_code=400, detail=f"Error reading PDF: {str(e)}")
#     return text


# def get_or_create_session(session_id: Optional[str] = None) -> str:
#     """Get existing session or create new one"""
#     if session_id and session_id in sessions:
#         return session_id
#     new_session_id = str(uuid.uuid4())
#     sessions[new_session_id] = {"resume": "", "jd": ""}
#     return new_session_id


# def answer_question(question: str, resume_text: str, jd_text: str) -> str:
#     """Use LLM to answer questions based on resume and JD"""
    
#     # Check if documents are uploaded
#     if not resume_text and not jd_text:
#         return "Please upload both your resume and job description first before asking questions."
    
#     if not resume_text:
#         return "Please upload your resume first before asking questions."
    
#     if not jd_text:
#         return "Please upload the job description first before asking questions."
    
#     prompt = f"""You are a helpful career advisor chatbot. Your role is to answer questions about a candidate's resume and a job description (JD).

# You have access to:
# 1. The candidate's RESUME
# 2. The JOB DESCRIPTION (JD) they are interested in

# Your task is to answer the user's question by analyzing both documents and providing helpful, accurate, and actionable advice.

# IMPORTANT GUIDELINES:
# - Be conversational and friendly
# - Provide specific, actionable advice
# - Reference specific skills, experiences, or requirements from the documents when relevant
# - If asked about readiness for a role, compare the resume against JD requirements
# - If asked about skills to learn, identify gaps between resume and JD
# - Be honest but encouraging
# - Keep responses concise but informative (2-4 paragraphs max)

# ---
# RESUME:
# {resume_text}

# ---
# JOB DESCRIPTION:
# {jd_text}

# ---
# USER QUESTION:
# {question}

# ---
# Please provide a helpful answer to the user's question:"""

#     try:
#         response = gemini_model.generate_content(prompt)
#         return response.text.strip()
#     except Exception as e:
#         return f"Sorry, I encountered an error: {str(e)}. Please try again."


# # ---------------------------
# # API ENDPOINTS
# # ---------------------------
# @app.post("/upload-resume", response_model=UploadResponse)
# async def upload_resume(
#     resume_file: UploadFile = File(...),
#     session_id: Optional[str] = Form(None)
# ):
#     """Upload resume PDF"""
#     if not resume_file.filename.endswith('.pdf'):
#         raise HTTPException(status_code=400, detail="Only PDF files are supported")
    
#     session_id = get_or_create_session(session_id)
    
#     # Save uploaded file temporarily
#     tmp = tempfile.NamedTemporaryFile(delete=False, suffix=".pdf")
#     try:
#         content = await resume_file.read()
#         tmp.write(content)
#         tmp.flush()
        
#         # Extract text
#         resume_text = extract_text_from_pdf(tmp.name)
        
#         # Store in session
#         sessions[session_id]["resume"] = resume_text
        
#         return UploadResponse(
#             message="Resume uploaded successfully",
#             session_id=session_id
#         )
#     finally:
#         os.unlink(tmp.name)


# @app.post("/upload-jd", response_model=UploadResponse)
# async def upload_jd(
#     jd_text: str = Form(...),
#     session_id: Optional[str] = Form(None)
# ):
#     """Upload job description text"""
#     session_id = get_or_create_session(session_id)
    
#     # Store JD in session
#     sessions[session_id]["jd"] = jd_text
    
#     return UploadResponse(
#         message="Job description uploaded successfully",
#         session_id=session_id
#     )


# @app.post("/chat", response_model=ChatResponse)
# async def chat(request: ChatRequest):
#     """Chat endpoint - answer questions about resume and JD"""
    
#     session_id = get_or_create_session(request.session_id)
    
#     # Get stored documents
#     session_data = sessions.get(session_id, {"resume": "", "jd": ""})
#     resume_text = session_data.get("resume", "")
#     jd_text = session_data.get("jd", "")
    
#     # Answer the question
#     answer = answer_question(request.question, resume_text, jd_text)
    
#     return ChatResponse(
#         answer=answer,
#         session_id=session_id
#     )


# @app.get("/session/{session_id}")
# async def get_session_status(session_id: str):
#     """Check what documents are uploaded for a session"""
#     if session_id not in sessions:
#         raise HTTPException(status_code=404, detail="Session not found")
    
#     session_data = sessions[session_id]
#     return {
#         "session_id": session_id,
#         "resume_uploaded": bool(session_data.get("resume")),
#         "jd_uploaded": bool(session_data.get("jd")),
#         "resume_length": len(session_data.get("resume", "")),
#         "jd_length": len(session_data.get("jd", ""))
#     }


# @app.get("/")
# async def root():
#     """API information"""
#     return {
#         "message": "Resume & JD Chatbot API",
#         "endpoints": {
#             "POST /upload-resume": "Upload resume PDF (form-data: resume_file, session_id?)",
#             "POST /upload-jd": "Upload job description (form-data: jd_text, session_id?)",
#             "POST /chat": "Ask questions (JSON: {question, session_id?})",
#             "GET /session/{session_id}": "Check session status"
#         },
#         "example_queries": [
#             "What skills should I learn for data science roles?",
#             "Am I ready for frontend developer positions?",
#             "What are my strengths for this role?",
#             "What skills am I missing for this job?",
#             "How can I improve my resume for this position?"
#         ]
#     }


# if __name__ == "__main__":
#     import uvicorn
#     uvicorn.run("chatbot:app", host="0.0.0.0", port=8000, reload=True)