"""Optional Claude-powered questions and feedback (needs ANTHROPIC_API_KEY)."""
import json
import os
import urllib.request

API_KEY = os.environ.get("ANTHROPIC_API_KEY")
MODEL = os.environ.get("CLAUDE_MODEL", "claude-sonnet-5-5")

def call_claude(prompt):
    body = json.dumps({"model": MODEL, "max_tokens": 1200,
                       "messages": [{"role": "user", "content": prompt}]}).encode()
    req = urllib.request.Request(
        "https://api.anthropic.com/v1/messages", data=body,
        headers={"x-api-key": API_KEY, "anthropic-version": "2023-06-01",
                 "content-type": "application/json"})
    with urllib.request.urlopen(req, timeout=60) as r:
        return json.load(r)["content"][0]["text"]

def ai_questions(resume, role):
    prompt = (f"You are an interviewer hiring for: {role or 'a software role'}.\n"
              "Based on this resume, write 10 interview questions (mix of technical, "
              "project-based and behavioral). Return only a JSON array of strings.\n\n"
              f"RESUME:\n{resume[:6000]}")
    text = call_claude(prompt)
    return json.loads(text[text.index("["): text.rindex("]") + 1])

def ai_feedback(question, answer):
    return call_claude(f"Interview question: {question}\nCandidate answer: {answer}\n"
                       "Give brief, constructive feedback (strengths, gaps, a score out of 10).")

