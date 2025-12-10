from fastapi import FastAPI, UploadFile, File, Form
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

app = FastAPI()

# -----------------------------------
# Extract text from PDF
# -----------------------------------
def extract_text(pdf_path):
    text = ""
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            t = page.extract_text()
            if t:
                text += t + "\n"
    return text


# -----------------------------------
# Rewrite Resume Using Gemini
# -----------------------------------
def rewrite_resume(resume_text, jd_text):
    prompt = f"""
You are an expert ATS resume optimizer.

Rewrite the resume so it strongly aligns with the Job Description.

STRICT JSON OUTPUT ONLY:

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

Rules:
- No hallucinations.
- Do NOT invent fake companies or projects.
- Enhance bullets with strong action verbs.
- Add JD keywords only if relevant.
- JSON ONLY. No markdown.

Resume:
{resume_text}

Job Description:
{jd_text}
"""

    response = model.generate_content(prompt)
    return response.text


# -----------------------------------
# Create Modern Resume PDF
# -----------------------------------
def generate_modern_pdf(data):
    temp_output = tempfile.NamedTemporaryFile(delete=False, suffix=".pdf").name

    doc = SimpleDocTemplate(temp_output, pagesize=letter)
    styles = getSampleStyleSheet()
    story = []

    # Name
    story.append(Paragraph(data["name"], styles["Title"]))
    story.append(Spacer(1, 12))

    # Title
    story.append(Paragraph(data["title"], styles["Heading2"]))
    story.append(Spacer(1, 12))

    # Summary
    story.append(Paragraph("Summary", styles["Heading3"]))
    story.append(Paragraph(data["summary"], styles["Normal"]))
    story.append(Spacer(1, 12))

    # Skills
    story.append(Paragraph("Skills", styles["Heading3"]))
    story.append(Paragraph(", ".join(data["skills"]), styles["Normal"]))
    story.append(Spacer(1, 12))

    # Experience
    story.append(Paragraph("Experience", styles["Heading3"]))
    for exp in data["experience"]:
        story.append(Paragraph(
            f"{exp['role']} at {exp['company']}, {exp['location']} ({exp['date']})",
            styles["Heading4"]
        ))
        for point in exp["points"]:
            story.append(Paragraph(f"• {point}", styles["Normal"]))
        story.append(Spacer(1, 10))

    # Projects
    story.append(Paragraph("Projects", styles["Heading3"]))
    for proj in data["projects"]:
        story.append(Paragraph(f"{proj['title']} ({proj['date']})", styles["Heading4"]))
        for point in proj["points"]:
            story.append(Paragraph(f"• {point}", styles["Normal"]))
        story.append(Spacer(1, 10))

    # Education
    story.append(Paragraph("Education", styles["Heading3"]))
    for edu in data["education"]:
        story.append(Paragraph(
            f"{edu['degree']} - {edu['institution']} ({edu['date']}) | Score: {edu['score']}",
            styles["Normal"]
        ))
        story.append(Spacer(1, 8))

    # Achievements
    if data["achievements"]:
        story.append(Paragraph("Achievements", styles["Heading3"]))
        for ach in data["achievements"]:
            story.append(Paragraph(f"• {ach}", styles["Normal"]))
        story.append(Spacer(1, 10))

    # Interests
    if data["interests"]:
        story.append(Paragraph("Interests", styles["Heading3"]))
        story.append(Paragraph(", ".join(data["interests"]), styles["Normal"]))

    doc.build(story)
    return temp_output


# -----------------------------------
# FASTAPI ENDPOINT
# -----------------------------------
@app.post("/rewrite-resume")
async def rewrite_resume_api(
    file: UploadFile = File(...),
    jd_text: str = Form(...)
):
    # Save uploaded file temporarily
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as temp_file:
        temp_file.write(await file.read())
        temp_path = temp_file.name

    # Extract resume text
    resume_text = extract_text(temp_path)

    # Rewrite using Gemini
    rewritten = rewrite_resume(resume_text, jd_text)

    # Remove extra markdown
    rewritten = re.sub(r"^```(?:json)?\s*\n?", "", rewritten)
    rewritten = re.sub(r"\n?```\s*$", "", rewritten)

    # Parse JSON
    data = json.loads(rewritten)

    # Generate Modern Resume PDF
    final_pdf_path = generate_modern_pdf(data)

    # Return PDF file to user
    return FileResponse(
        final_pdf_path,
        media_type="application/pdf",
        filename="Modern_Resume.pdf"
    )
# run as : uvicorn ats_resume_builder:app --reload
