# FastAPI Router Structure

This project uses modular routing similar to Express.js routers. All routes are organized in separate router files under the `routers/` directory.

## Project Structure

```
FastApi/
├── main.py                          # Main FastAPI application
├── routers/                         # Router modules
│   ├── __init__.py
│   ├── chatbot.py                  # Chatbot routes
│   ├── ats_resume_builder.py       # ATS resume builder routes
│   ├── job_detector.py             # Job detection routes
│   ├── compare_resumes.py          # Resume comparison routes
│   ├── interview_questions.py      # Interview question generator routes
│   └── resume_analyzer.py          # Resume analysis routes
└── .env                             # Environment variables (API_KEY)
```

## Running the Application

```bash
# Method 1: Using uvicorn directly
uvicorn main:app --reload

# Method 2: Using Python
python main.py
```

The server will start on `http://localhost:8000`

## Available Endpoints

### 1. Chatbot (`/chatbot`)
- **POST** `/chatbot`
  - Upload resume and JD, ask questions
  - Form data: `resume_file`, `jd_text`, `question`

### 2. ATS Resume Builder (`/ats-resume`)
- **POST** `/ats-resume/rewrite`
  - Rewrite and optimize resume based on JD
  - Form data: `file` (PDF), `jd_text`
  - Returns: Optimized resume PDF

### 3. Job Detector (`/job-detector`)
- **POST** `/job-detector`
  - Detect suitable job roles from resume
  - Form data: `file` (PDF)
  - Returns: Job roles with confidence scores

### 4. Resume Comparison (`/compare-resumes`)
- **POST** `/compare-resumes`
  - Compare multiple resumes
  - Form data: `files` (multiple PDF files)
  - Returns: Scores and best resume analysis

### 5. Interview Questions (`/interview-questions`)
- **POST** `/interview-questions/generate`
  - Generate interview questions based on resume and JD
  - Form data: `resume_file` (PDF), `jd_text`
  - Returns: Categorized interview questions

### 6. Resume Analyzer (`/analyze`)
- **POST** `/analyze`
  - Analyze resume match against job description
  - Form data: `resume_file` (PDF), `jd_text`
  - Returns: Match score, verdict, missing skills, improvements

## API Documentation

Once the server is running, visit:
- **Swagger UI**: `http://localhost:8000/docs`
- **ReDoc**: `http://localhost:8000/redoc`

## Adding New Routers

To add a new router:

1. Create a new file in `routers/` directory:
   ```python
   # routers/my_new_router.py
   from fastapi import APIRouter
   
   router = APIRouter(prefix="/my-route", tags=["My Tag"])
   
   @router.get("")
   async def my_endpoint():
       return {"message": "Hello"}
   ```

2. Import and include in `main.py`:
   ```python
   from routers import my_new_router
   
   app.include_router(my_new_router.router)
   ```

## Environment Variables

Create a `.env` file in the project root:
```
API_KEY=your_gemini_api_key_here
```

## Notes

- Each router is independent and can be developed separately
- All routers share the same FastAPI app instance
- CORS is enabled for all origins (adjust in production)
- All routers use the same Gemini API configuration

