def generate_resume_html(data):
    name = data.get("name", "")
    contact = data.get("contact", {})
    summary = data.get("summary", "")

    technicalSkills = data.get("technicalSkills", {})
    softSkills = data.get("softSkills", [])

    projects = data.get("projects", [])
    experience = data.get("experience", [])
    education = data.get("education", [])
    certifications = data.get("certifications", [])

    # Convert to HTML exactly like your JS template
    html = f"""
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>{name or "Resume"}</title>

<style>
    @page {{ size: A4; margin: 0.6in; }}
    body {{ font-family: 'Times New Roman', serif; font-size: 11pt; }}
    .name {{ font-size: 24pt; font-weight: bold; text-align:center }}
    .contact {{ text-align:center; margin-top:6px }}
    .section-title {{ font-size: 12pt; font-weight: bold; text-transform: uppercase; margin-top:18px }}
    .section-rule {{ border-top:1px solid black; margin:4px 0 }}
    ul {{ margin-top:4px }}
</style>
</head>

<body>
<div class="name">{name or ""}</div>
<div class="contact">
    {contact.get("phone", "")} &nbsp; 
    {contact.get("email", "")} &nbsp; 
    {contact.get("location", "")}
</div>

{"<div class='section-title'>Summary</div><div class='section-rule'></div><p>" + summary + "</p>" if summary else ""}

{"""
<div class='section-title'>Technical Skills</div>
<div class='section-rule'></div>
""" + "".join(
        f"<p><strong>{cat}:</strong> {', '.join(skills) if isinstance(skills, list) else skills}</p>"
        for cat, skills in technicalSkills.items()
    ) if technicalSkills else ""}

{"""
<div class='section-title'>Soft Skills</div>
<div class='section-rule'></div>
<ul>
""" + "".join(f"<li>{s}</li>" for s in softSkills) + "</ul>" if softSkills else ""}

{"""
<div class='section-title'>Projects</div>
<div class='section-rule'></div>
""" + "".join(f"""
<p><strong>{p.get('title','')}</strong> ({p.get('dates','')})</p>
{("<ul>" + "".join(f"<li>{pt}</li>" for pt in p.get('description', [])) + "</ul>") if p.get("description") else ""}
""" for p in projects) if projects else ""}

{"""
<div class='section-title'>Experience</div>
<div class='section-rule'></div>
""" + "".join(f"""
<p><strong>{e.get('role','')}</strong> — {e.get('company','')} ({e.get('dates','')})</p>
{("<ul>" + "".join(f"<li>{pt}</li>" for pt in e.get('responsibilities', [])) + "</ul>") if e.get("responsibilities") else ""}
""" for e in experience) if experience else ""}

{"""
<div class='section-title'>Education</div>
<div class='section-rule'></div>
""" + "".join(f"""
<p><strong>{ed.get('degree','')}</strong> — {ed.get('institution','')} ({ed.get('dates','')})</p>
""" for ed in education) if education else ""}

{"""
<div class='section-title'>Certifications</div>
<div class='section-rule'></div>
<ul>
""" + "".join(f"<li>{c}</li>" for c in certifications) + "</ul>" if certifications else ""}

</body>
</html>
"""
    return html
