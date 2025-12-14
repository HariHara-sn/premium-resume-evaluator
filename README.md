
# Career Compass – AI Job & Career Assistant

A modern AI-powered career guidance platform designed to help students evaluate job readiness, improve resumes, and prepare for interviews.
The system analyzes resumes and job descriptions to provide actionable insights and personalized guidance.

---

## Demo Video

Watch the complete working demo of Career Compass:

**[Demo Video – Google Drive Link]**

---

## 🌟 Overview

Career Compass acts as a **virtual career mentor** for students and early professionals.
It evaluates how well a resume matches a job role, identifies skill gaps, and provides AI-driven recommendations to strengthen applications.

The project demonstrates how to design an **intelligent, modular AI system** using resume parsing, structured reasoning, and job-role analysis.

---

## ✨ Core Features

### 🧠 Resume & Job Match Analysis

* Intelligent resume–job description alignment scoring
* Visual readiness score (e.g., Strong Match – 8/10)
* Clear explanation of matching and missing areas

### 📄 AI Resume Rewrite & Enhancement

* ATS-friendly resume rewriting
* Job-description-aligned keyword optimization
* Improved bullet points and structure
* Downloadable optimized resume in PDF format

### 🔍 Skill Gap Analysis

* Identifies missing or weak skills required by the job
* Suggests safe and realistic improvements
* Highlights transferable skills where applicable

### 🎯 Job Detector

* Predicts the most suitable job role based on resume content
* Explains why the role is a good match

### 💬 Career Guidance Chatbot

* Answers natural language career questions
* Examples:

  * “What skills should I learn for data science roles?”
  * “Am I ready for frontend developer positions?”

### 🎤 Interview Question Prediction (Advanced Feature)

* Generates role-specific interview questions based on your resume and JD.
* Covers:

  * Technical questions
  * Project-based questions

### 🧾 Multi-Resume Comparison (Elite Feature)

* Compare 2–3 resume versions
* AI scores each resume objectively
* Identifies the best-performing resume
* Shows percentage improvement between versions

---

## 🏗️ System Architecture

**Click Here for architecture flow:**

https://miro.com/app/board/uXjVGbwuzsY=/

**Input Layer**

* Resume upload (PDF)
* Job description input
* Multiple resume upload (elite feature)

**AI Processing Layer**

* Resume text extraction
* Job description skill extraction
* Structured data normalization

**Intelligence Layer**

* Resume–JD match scoring
* Skill gap analysis
* Resume rewriting
* Job detection
* Career chatbot
* Interview question prediction
* Multi-resume comparison

**Output Layer**

* Visual match scores
* Actionable feedback
* Skill gap insights
* Downloadable resumes (PDF)


---

## 🛠️ Tech Stack

| Layer          | Tools                |
| -------------- | -------------------- |
| Backend        | Python, FastAPI      |
| Frontend       | React, Tailwind CSS  |
| AI             | Google Gemini API    |
| Resume Parsing | pdfplumber           |
| PDF Generation | ReportLab            |
| Data Format    | JSON                 |
| Architecture   | Modular AI Pipelines |


---

## 📁 Folder Structure

```
.
├── resume_analysis/          # Resume & JD analysis logic
├── resume_rewrite/           # ATS-friendly resume generation
├── interview_questions/      # Interview question prediction
├── multi_resume_compare/     # Elite resume comparison feature
├── chatbot/                  # Career guidance chatbot
├── utils/                    # PDF extraction, helpers
├── templates/                # PDF resume templates
├── main.py                   # Application entry point
└── README.md
```

---

## ⚙️ Installation & Setup

### 1️⃣ Clone the Repository

```bash
git clone https://github.com/HariHara-sn/premium-resume-evaluator.git
cd premium-resume-evaluator
```

### 2️⃣ Create Virtual Environment

```bash
python -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate
```

### 3️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

### 4️⃣ Environment Variables

Create a `.env` file:

```
GEMINI_API_KEY=your_api_key_here
```

---

## 🚀 Run the Application

```bash
uvicorn main:app --reload or
python main.py
```

---

## 🧠 How the AI Works

1. User uploads resume and provides job description
2. Resume and JD are converted into structured data
3. AI performs multi-step reasoning:

   * Skill extraction
   * Matching & gap detection
   * Resume enhancement
   * Interview preparation
4. Results are returned as structured insights and downloadable PDFs

---

## 🎯 Design Principles

* Accuracy over hallucination
* Explainable AI outputs
* Student-focused guidance
* Modular and extensible architecture
* Production-oriented thinking

---

## 📌 Conclusion

Career Compass is not just a resume checker — it is a **complete AI-powered career assistant** that helps students understand job readiness, improve applications, and prepare for interviews.
