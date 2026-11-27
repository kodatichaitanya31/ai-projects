"""Optional Claude-written draft replies (set ANTHROPIC_API_KEY). Offline fallback included."""
import json
import os
import urllib.request

API_KEY = os.environ.get("ANTHROPIC_API_KEY")
MODEL = os.environ.get("CLAUDE_MODEL", "claude-sonnet-5-5")

def _call_claude(prompt):
    body = json.dumps({"model": MODEL, "max_tokens": 400,
                       "messages": [{"role": "user", "content": prompt}]}).encode()
    req = urllib.request.Request(
        "https://api.anthropic.com/v1/messages", data=body,
        headers={"x-api-key": API_KEY, "anthropic-version": "2023-06-01",
                 "content-type": "application/json"})
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.load(r)["content"][0]["text"]

def draft_reply(subject, body, articles):
    """Return a suggested reply for the support agent."""
    if API_KEY:
        try:
            ctx = "\n".join(f"- {a['title']}: {a['text']}" for a in articles)
            return _call_claude(f"Write a short, polite support reply.\nTicket: {subject}\n{body}\n"
                                f"Use these help articles if relevant:\n{ctx}")
        except Exception:
            pass
    if articles:
        steps = " ".join(f"See '{a['title']}': {a['text']}" for a in articles[:1])
        return f"Hello, thanks for contacting us about '{subject}'. {steps} Reply here if this does not solve it."
    return f"Hello, thanks for contacting us about '{subject}'. Your ticket has been routed and an agent will respond shortly."
