#user upload the resume and job desc , 
# the system will build a modern resume based on JD 

import pdfplumber
import google.generativeai as genai
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.pagesizes import letter
from reportlab.lib.enums import TA_LEFT
from reportlab.lib import colors
import json
import re
from dotenv import load_dotenv
import os
load_dotenv()
api_key = os.getenv("API_KEY")
genai.configure(api_key=api_key)

model = genai.GenerativeModel("gemini-2.0-flash")


# ------------------------
# PDF → TEXT
# ------------------------
def extract_text(pdf_path):
    text = ""
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            t = page.extract_text()
            if t:
                text += t + "\n"
    return text


# ------------------------
# LLM REWRITE
# ------------------------
#  def rewrite_resume(resume_text, jd_text):
    prompt = f"""
You are an expert technical resume writer.

Rewrite the resume so it aligns strongly with the Job Description.

OUTPUT STRICT VALID JSON ONLY in this format:

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
- Improve clarity, action verbs, measurable results.
- No hallucination. Only rewrite the user's actual content.
- Do NOT invent companies or projects.
- Bullets must be strong, concise, achievement-oriented.
- Add missing keywords *only* if actually true and safe.
IMPORTANT:
- Output STRICT JSON ONLY.
- No explanation.
- No markdown.
- No extra text.
- No comments.
- Just raw JSON.


Resume:
{resume_text}

Job Description:
{jd_text}
"""

    response = model.generate_content(prompt)
    return response.text

def rewrite_resume(resume_text, jd_text):
    prompt = f"""
You are an expert ATS resume optimizer and technical hiring specialist.

Your tasks:
1. Extract important keywords, skills, and responsibilities from the Job Description.
2. Compare with candidate resume.
3. Add missing but *relevant and believable* JD keywords to skills, summary, experience bullets.
4. Improve resume using STAR-based strong action verbs.
5. Do NOT create fake experience or fake tools that user never mentioned.
6. If skills match logically (ex: Python resume + JD has NumPy), you MAY add them.
7. Final output MUST be ATS-friendly, clean, professional.

OUTPUT STRICT VALID JSON ONLY in this format:

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

STRICT RULES:
- No hallucinations.
- No invented companies or projects.
- Only rewrite and enhance the user’s actual content.
- Add missing JD keywords ONLY when realistic.
- No paragraphs longer than 4 lines.
- JSON ONLY. No markdown, no explanation.

Candidate Resume:
{resume_text}

Job Description:
{jd_text}
"""

    response = model.generate_content(prompt)
    return response.text



def generate_modern_pdf(data, output="Modern_Resume.pdf"):
    doc = SimpleDocTemplate(output, pagesize=letter)
    styles = getSampleStyleSheet()
    story = []

    # Name
    story.append(Paragraph(data['name'], styles['Title']))
    story.append(Spacer(1, 12))

    # Title
    story.append(Paragraph(data['title'], styles['Heading2']))
    story.append(Spacer(1, 12))

    # Summary
    story.append(Paragraph("Summary", styles['Heading3']))
    story.append(Paragraph(data['summary'], styles['Normal']))
    story.append(Spacer(1, 12))

    # Skills
    story.append(Paragraph("Skills", styles['Heading3']))
    skills = ', '.join(data['skills'])
    story.append(Paragraph(skills, styles['Normal']))
    story.append(Spacer(1, 12))

    # Experience
    story.append(Paragraph("Experience", styles['Heading3']))
    for exp in data['experience']:
        story.append(Paragraph(f"{exp['role']} at {exp['company']}, {exp['location']} ({exp['date']})", styles['Heading4']))
        for point in exp['points']:
            story.append(Paragraph(f"• {point}", styles['Normal']))
        story.append(Spacer(1, 6))
    story.append(Spacer(1, 12))

    # Projects
    if data['projects']:
        story.append(Paragraph("Projects", styles['Heading3']))
        for proj in data['projects']:
            story.append(Paragraph(f"{proj['title']} ({proj['date']})", styles['Heading4']))
            for point in proj['points']:
                story.append(Paragraph(f"• {point}", styles['Normal']))
            story.append(Spacer(1, 6))
        story.append(Spacer(1, 12))

    # Education
    story.append(Paragraph("Education", styles['Heading3']))
    for edu in data['education']:
        story.append(Paragraph(f"{edu['degree']} from {edu['institution']}, {edu['score']} ({edu['date']})", styles['Normal']))
    story.append(Spacer(1, 12))

    # Achievements
    if data['achievements']:
        story.append(Paragraph("Achievements", styles['Heading3']))
        for ach in data['achievements']:
            story.append(Paragraph(f"• {ach}", styles['Normal']))
        story.append(Spacer(1, 12))

    # Interests
    if data['interests']:
        story.append(Paragraph("Interests", styles['Heading3']))
        interests = ', '.join(data['interests'])
        story.append(Paragraph(interests, styles['Normal']))

    doc.build(story)
    return output



# ------------------------
# MAIN FUNCTION
# ------------------------
if __name__ == "__main__":
    resume_path = "C:\\Users\\ACER\\Documents\\resumes\\HariHaraSudhan-AI-Resume.pdf"
    jd_text = """Python / ML Engineer with FastAPI, PyTorch, AWS, Data Structures..."""


    print("\nExtracting resume text...")
    resume_txt = extract_text(resume_path)

    print("Rewriting using Gemini...")
    rewritten = rewrite_resume(resume_txt, jd_text)

    # Clean the response to extract JSON
    rewritten = re.sub(r'^```(?:json)?\s*\n?', '', rewritten)
    rewritten = re.sub(r'\n?```\s*$', '', rewritten)
    rewritten = rewritten.strip()

    print("Parsing JSON...")
    try:
        data = json.loads(rewritten)
    except json.JSONDecodeError:
        print("Gemini returned invalid JSON. Raw output:")
        print(rewritten)
        raise

    print("Generating Modern Resume PDF...")
    output_file = generate_modern_pdf(data)

    print("Generating ATS PDF...")
    output_file = generate_modern_pdf(data)

    print("\nDONE! Generated:", output_file)
