"""AI Interview Prep Platform. Run: python app.py  then open http://127.0.0.1:5000

Upload a resume (PDF, DOCX or TXT) to get skill-based interview questions and answer
feedback. Set ANTHROPIC_API_KEY for resume-specific AI questions and feedback.
"""
import io

from flask import Flask, jsonify, render_template_string, request

import ai
from page import PAGE
from questions import find_skills, offline_feedback, offline_questions

app = Flask(__name__)
app.config["MAX_CONTENT_LENGTH"] = 5 * 1024 * 1024  # 5 MB uploads
API_KEY = ai.API_KEY

def extract_text(file):
    name = (file.filename or "").lower()
    data = file.read()
    if name.endswith(".pdf"):
        from pypdf import PdfReader
        return "\n".join(p.extract_text() or "" for p in PdfReader(io.BytesIO(data)).pages)
    if name.endswith(".docx"):
        import docx
        return "\n".join(p.text for p in docx.Document(io.BytesIO(data)).paragraphs)
    return data.decode("utf-8", errors="ignore")

@app.post("/api/analyze")
def analyze():
    f = request.files.get("resume")
    if not f or not f.filename:
        return jsonify(error="Please upload a resume file."), 400
    text = extract_text(f)
    if len(text.strip()) < 30:
        return jsonify(error="Could not read text from this file."), 400
    skills = find_skills(text)
    role = request.form.get("role", "")
    mode, questions = "offline", offline_questions(skills)
    if API_KEY:
        try:
            questions, mode = ai.ai_questions(text, role), "claude"
        except Exception:
            pass
    return jsonify(skills=skills, questions=questions, mode=mode)

@app.post("/api/feedback")
def feedback():
    d = request.get_json(force=True)
    q, a = d.get("question", ""), d.get("answer", "")
    if API_KEY:
        try:
            return jsonify(feedback=ai.ai_feedback(q, a))
        except Exception:
            pass
    return jsonify(feedback=offline_feedback(a))

@app.get("/")
def index():
    return render_template_string(PAGE)

if __name__ == "__main__":
    app.run(debug=False)
