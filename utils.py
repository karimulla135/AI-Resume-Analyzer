from PyPDF2 import PdfReader

# 📄 Extract text
def extract_text(file):
    reader = PdfReader(file)
    text = ""
    for page in reader.pages:
        if page.extract_text():
            text += page.extract_text()
    return text.lower()


# 🧠 Skill matching
def match_skills(resume_text, skills):
    found = []
    for skill in skills:
        if skill in resume_text:
            found.append(skill)
    
    score = (len(found) / len(skills)) * 100
    return found, score


# 📄 Simple summary
def generate_summary(text):
    sentences = text.split(".")
    return ". ".join(sentences[:4])


# 💼 Job database
JOBS = {
    "Data Analyst": [
        "Data Analyst Intern - SQL & Excel",
        "Business Analyst - Power BI",
        "Junior Data Analyst - Python"
    ],
    
    "ML Engineer": [
        "ML Intern - TensorFlow",
        "AI Engineer - Deep Learning",
        "Data Scientist - NLP"
    ]
}


# 🔍 Job recommendation
def recommend_jobs(role, score):
    jobs = JOBS.get(role, [])
    
    if score > 70:
        return jobs
    elif score > 40:
        return jobs[:2]
    else:
        return ["Upskill before applying"]


# 📄 PDF report
from reportlab.platypus import SimpleDocTemplate, Paragraph
from reportlab.lib.styles import getSampleStyleSheet

def create_pdf(score, found, missing, summary):
    doc = SimpleDocTemplate("report.pdf")
    styles = getSampleStyleSheet()
    
    content = []
    content.append(Paragraph(f"Match Score: {score:.2f}%", styles["Normal"]))
    content.append(Paragraph(f"Skills Found: {', '.join(found)}", styles["Normal"]))
    content.append(Paragraph(f"Missing Skills: {', '.join(missing)}", styles["Normal"]))
    content.append(Paragraph(f"Summary: {summary}", styles["Normal"]))
    
    doc.build(content)
    return "report.pdf"