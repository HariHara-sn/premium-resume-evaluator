from fastapi import APIRouter, UploadFile, File, Form
from fastapi.responses import FileResponse
import pdfplumber
import google.generativeai as genai
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.pagesizes import letter
import json
import re
import tempfile
import os
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("API_KEY")
genai.configure(api_key=api_key)

model = genai.GenerativeModel("gemini-2.5-flash")

router = APIRouter(prefix="/rewrite-resume", tags=["ATS Resume Builder"])


def extract_text(pdf_path):
    text = ""
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            t = page.extract_text()
            if t:
                text += t + "\n"
    return text


def rewrite_resume(resume_text, jd_text):
    prompt = f"""
You are an expert ATS resume optimizer.

Rewrite the resume so it aligns with the Job Description, but keep the content 
SHORT, PRECISE, and CRISP.

STRICT INSTRUCTIONS:
- SUMMARY must be max 3 lines.
- Each bullet must be max 12–14 words.
- Do NOT produce long paragraphs.
- NO story-like language.
- NO filler phrases (avoid dynamic, passionate, enthusiastic, etc.).
- NO exaggerations.
- No invented companies, projects, or achievements.
- Use only information found in the original resume.
- Missing fields should be ignored.

OUTPUT MUST BE STRICT JSON ONLY:

{{
  "name": "",
  "title": "",
  "summary": "",
  "skills": [],
  "experience": [
    {{
      "role": "",
      "company": "",
      "location": "",
      "date": "",
      "points": []
    }}
  ],
  "projects": [
    {{
      "title": "",
      "date": "",
      "points": []
    }}
  ],
  "education": [
    {{
      "degree": "",
      "institution": "",
      "score": "",
      "date": ""
    }}
  ],
  "achievements": [],
  "interests": []
}}

Resume Content:
{resume_text}

Job Description:
{jd_text}
"""


    response = model.generate_content(prompt)
    return response.text


def generate_modern_pdf(data):
    temp_output = tempfile.NamedTemporaryFile(delete=False, suffix=".pdf").name

    doc = SimpleDocTemplate(temp_output, pagesize=letter)
    styles = getSampleStyleSheet()
    story = []

    
    story.append(Paragraph(data["name"], styles["Title"]))
    story.append(Spacer(1, 12))

    
    story.append(Paragraph(data["title"], styles["Heading2"]))
    story.append(Spacer(1, 12))

    
    story.append(Paragraph("Summary", styles["Heading3"]))
    story.append(Paragraph(data["summary"], styles["Normal"]))
    story.append(Spacer(1, 12))

    
    story.append(Paragraph("Skills", styles["Heading3"]))
    story.append(Paragraph(", ".join(data["skills"]), styles["Normal"]))
    story.append(Spacer(1, 12))

    
    story.append(Paragraph("Experience", styles["Heading3"]))
    for exp in data["experience"]:
        story.append(Paragraph(
            f"{exp['role']} at {exp['company']}, {exp['location']} ({exp['date']})",
            styles["Heading4"]
        ))
        for point in exp["points"]:
            story.append(Paragraph(f"• {point}", styles["Normal"]))
        story.append(Spacer(1, 10))

    
    story.append(Paragraph("Projects", styles["Heading3"]))
    for proj in data["projects"]:
        story.append(Paragraph(f"{proj['title']} ({proj['date']})", styles["Heading4"]))
        for point in proj["points"]:
            story.append(Paragraph(f"• {point}", styles["Normal"]))
        story.append(Spacer(1, 10))

    
    story.append(Paragraph("Education", styles["Heading3"]))
    for edu in data["education"]:
        story.append(Paragraph(
            f"{edu['degree']} - {edu['institution']} ({edu['date']}) | Score: {edu['score']}",
            styles["Normal"]
        ))
        story.append(Spacer(1, 8))

    if data["achievements"]:
        story.append(Paragraph("Achievements", styles["Heading3"]))
        for ach in data["achievements"]:
            story.append(Paragraph(f"• {ach}", styles["Normal"]))
        story.append(Spacer(1, 10))

    if data["interests"]:
        story.append(Paragraph("Interests", styles["Heading3"]))
        story.append(Paragraph(", ".join(data["interests"]), styles["Normal"]))

    doc.build(story)
    return temp_output


@router.post("")
async def rewrite_resume_api(
    file: UploadFile = File(...),
    jd_text: str = Form(...)
):
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as temp_file:
        temp_file.write(await file.read())
        temp_path = temp_file.name

    try:
        resume_text = extract_text(temp_path)

        rewritten = rewrite_resume(resume_text, jd_text)

        rewritten = re.sub(r"^```(?:json)?\s*\n?", "", rewritten)
        rewritten = re.sub(r"\n?```\s*$", "", rewritten)

        data = json.loads(rewritten)

        final_pdf_path = generate_modern_pdf(data)

        return FileResponse(
            final_pdf_path,
            media_type="application/pdf",
            filename="Modern_Resume.pdf"
        )
    finally:
        try:
            if os.path.exists(temp_path):
                os.remove(temp_path)
        except Exception:
            pass  
