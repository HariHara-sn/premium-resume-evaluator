from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import chatbot, ats_resume_builder, job_detector, compare_resumes, interview_questions, resume_analyzer

app = FastAPI(
    title="Resume & Career Tools API",
    description="Comprehensive API for resume analysis, ATS optimization, job detection, interview preparation, and career chatbot",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(chatbot.router)
app.include_router(ats_resume_builder.router)
app.include_router(job_detector.router)
app.include_router(compare_resumes.router)
app.include_router(interview_questions.router)
app.include_router(resume_analyzer.router)


@app.get("/")
async def root():
    """API root endpoint with information about available routes"""
    return {
        "message": "Resume & Career Tools API",
        "version": "1.0.0",
        "endpoints": {
            "chatbot": {
                "POST /chatbot": "Ask questions about resume and JD"
            },
            "ats_resume": {
                "POST /rewrite-resume": "Rewrite and optimize resume based on JD"
            },
            "job_detector": {
                "POST /job-detector": "Detect suitable job roles from resume"
            },
            "compare_resumes": {
                "POST /compare-resumes": "Compare multiple resumes"
            },
            "interview_questions": {
                "POST /interview-questions/generate": "Generate interview questions based on resume and JD"
            },
            "analyze": {
                "POST /analyze": "Analyze resume match against job description"
            }
        },
        "documentation": "/docs"
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
