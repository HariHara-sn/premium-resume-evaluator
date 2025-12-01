# main.py
# import os
# import json
# import tempfile
# from typing import List
# from fastapi import FastAPI, File, UploadFile, Form
# from pydantic import BaseModel
# import pdfplumber
# import re
# from rapidfuzz import process, fuzz
# from sentence_transformers import SentenceTransformer
# import numpy as np
# import google.generativeai as genai

# # ---------------------------
# # GEMINI CONFIG
# # ---------------------------
# genai.configure(api_key="AIzaSyBs9JPqB5FgPTAxSk0Xd75QrMLwmfhI81Q")

# gemini_model = genai.GenerativeModel("gemini-2.0-flash")

# app = FastAPI(title="Resume Evaluator + RAG") 
# embedding_model = SentenceTransformer("all-MiniLM-L6-v2")

# RAG_DB = [
#     {"skill": "Docker", "desc": "Containerization tool for applications."},
#     {"skill": "AWS", "desc": "Cloud platform for hosting services."},
#     {"skill": "FastAPI", "desc": "Python framework for APIs."},
#     {"skill": "Python", "desc": "High-level programming language."},
# ]

# # ---------------------------
# # Pydantic Output Model
# # ---------------------------
# class AnalyzeResult(BaseModel):
#     verdict: str
#     match_score: float
#     missing_skills: List[str]
#     one_tip: str
#     improvements: List[dict]


# # ---------------------------
# # HELPERS
# # ---------------------------
# def extract_text_from_pdf(path: str) -> str:
#     text = ""
#     with pdfplumber.open(path) as pdf:
#         for page in pdf.pages:
#             page_text = page.extract_text()
#             if page_text:
#                 text += page_text + "\n"
#     print("\n--- PDF TEXT EXTRACTED ---")
#     print(text)
#     return text


# def parse_sections(text: str) -> dict:
#     sections = {"skills": [], "experience": [], "education": []}

#     # skills
#     skills_match = re.search(
#         r"(skills|technologies|tools)\s*[:\n](.*?)(\n\n|\Z)",
#         text,
#         re.I | re.S
#     )
#     if skills_match:
#         skills_text = skills_match.group(2)
#         sections["skills"] = [
#             s.strip() for s in re.split(r",|;|\n", skills_text) if s.strip()
#         ]

#     # experience
#     exp_matches = re.findall(
#         r"(\d{4})\s*[-–]\s*(\d{4}|Present).*?(?:at|@)\s*(.*?)\n",
#         text,
#         re.I,
#     )
#     sections["experience"] = [
#         {"years": f"{m[0]}-{m[1]}", "company": m[2]}
#         for m in exp_matches
#     ]

#     # education
#     edu_matches = re.findall(
#         r"(Bachelor|Master|B\.Tech|M\.Tech|B\.Sc|M\.Sc).*?\n",
#         text,
#         re.I,
#     )
#     sections["education"] = [e.strip() for e in edu_matches]

#     print("\n--- PARSED SECTIONS ---")
#     print(json.dumps(sections, indent=2))
#     return sections


# def extract_skills_from_jd(jd: str) -> List[str]:
#     parts = re.split(r",|;|\n| and ", jd)
#     skills = [p.strip() for p in parts if p.strip()]
#     print("\n--- JD SKILLS ---")
#     print(skills)
#     return skills


# def compute_scores(jd_skills: List[str], sections: dict) -> dict:
#     resume_skills = sections.get("skills", [])
#     matched = 0

#     for s in jd_skills:
#         best = process.extractOne(s, resume_skills, scorer=fuzz.token_sort_ratio)
#         if best and best[1] > 70:
#             matched += 1

#     skill_score = (matched / len(jd_skills)) * 100 if jd_skills else 0
#     exp_score = len(sections["experience"]) * 10
#     exp_score = min(100, exp_score)

#     final_score = (
#         0.4 * skill_score +
#         0.25 * exp_score +
#         0.15 * 100 +
#         0.2 * skill_score
#     )

#     scores = {
#         "skills_score": skill_score,
#         "exp_score": exp_score,
#         "ats_score": 100,
#         "keyword_score": skill_score,
#         "final_score": final_score,
#     }

#     print("\n--- COMPUTED SCORES ---")
#     print(scores)
#     return scores


# def retrieve_rag_skills(missing_skills):
#     results = []
#     db_skills = [r["skill"] for r in RAG_DB]

#     for skill in missing_skills:
#         matches = process.extract(skill, db_skills, limit=3)
#         for m in matches:
#             for r in RAG_DB:
#                 if r["skill"] == m[0]:
#                     results.append({"skill": skill, "desc": r["desc"]})

#     print("\n--- RAG OUTPUT ---")
#     print(results)
#     return results


# def call_llm_for_evaluation(payload: dict) -> dict:
#     try:
#         prompt = f"""
# You are a JSON-only resume evaluator. Respond with *only* valid JSON.

# Resume:
# {json.dumps(payload['sections'], indent=2)}

# JD Skills:
# {json.dumps(payload['jd_skills'], indent=2)}

# Missing:
# {json.dumps(payload['missing_skills'], indent=2)}

# Scores:
# {json.dumps(payload['scores'], indent=2)}

# Output strictly this JSON:
# {{
#     "verdict": "",
#     "match_score": 0,
#     "missing_skills": [],
#     "one_tip": "",
#     "improvements": []
# }}
# """

#         response = gemini_model.generate_content(prompt)
        
#         raw = response.text.strip()
#         # raw = response.candidates[0].content.parts[0].text

#         print("\n--- RAW LLM RESPONSE ---")
#         print(raw)
        

#         json_start = raw.find("{")
#         json_end = raw.rfind("}")

#         clean = raw[json_start:json_end + 1]
#         parsed = json.loads(clean)

#         return parsed

#     except Exception as e:
#         print("LLM ERROR:", e)
#         return {
#             "verdict": "Failed",
#             "match_score": 0,
#             "missing_skills": payload["missing_skills"],
#             "one_tip": "LLM failed to evaluate.",
#             "improvements": []
#         }


# # ---------------------------
# # API ENDPOINT
# # ---------------------------
# # @app.post("/analyze",response_model=AnalyzeResult)
# data = {
#     "Hari" : "software engineer",
#     "location" : "canada"
# }
# @app.post("/analyze")
# async def analyze_resume(jd_text: str = Form(...), resume_file: UploadFile = File(...)):
#     tmp = tempfile.NamedTemporaryFile(delete=False, suffix=".pdf")
#     content = await resume_file.read()
#     tmp.write(content)
#     tmp.flush()

#     resume_txt = extract_text_from_pdf(tmp.name)
#     sections = parse_sections(resume_txt)
#     jd_skills = extract_skills_from_jd(jd_text)
#     scores = compute_scores(jd_skills, sections)

#     resume_skills = sections.get("skills", [])
#     matched_skills = [
#         s for s in jd_skills
#         if s in resume_skills or any(fuzz.ratio(s, rs) > 70 for rs in resume_skills)
#     ]
#     missing_skills = [s for s in jd_skills if s not in matched_skills]

#     rag_info = retrieve_rag_skills(missing_skills)

#     payload = {
#         "sections": sections,
#         "jd_skills": jd_skills,
#         "missing_skills": missing_skills,
#         "scores": scores,
#         "rag_info": rag_info
#     }
#     print("Payload for LLM :",payload)
#     result = call_llm_for_evaluation(payload)

#     print("\n--- FINAL RETURN JSON Hari ---")
#     print(json.dumps(result, indent=2))
#     data["result"] = result
#     return data


# # ---------------------------
# # RUN
# # ---------------------------
# if __name__ == "__main__":
#     import uvicorn
#     uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
