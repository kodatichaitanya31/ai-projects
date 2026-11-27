"""CLI chatbot. Uses the Claude API if ANTHROPIC_API_KEY is set, otherwise a simple offline mode.

Run: python chat.py     (type 'quit' to exit)
"""
import json
import os
import urllib.request

API_KEY = os.environ.get("ANTHROPIC_API_KEY")
MODEL = os.environ.get("CLAUDE_MODEL", "claude-sonnet-5-5")

def claude_reply(history):
    body = json.dumps({"model": MODEL, "max_tokens": 500, "messages": history}).encode()
    req = urllib.request.Request(
        "https://api.anthropic.com/v1/messages", data=body,
        headers={"x-api-key": API_KEY, "anthropic-version": "2023-06-01",
                 "content-type": "application/json"})
    with urllib.request.urlopen(req, timeout=60) as r:
        return json.load(r)["content"][0]["text"]

RULES = {
    "hello": "Hi there! Ask me anything about AI.",
    "ai": "AI is the field of building machines that perform tasks needing human-like intelligence.",
    "ml": "Machine learning lets computers learn patterns from data.",
    "bye": "Goodbye!",
}

def offline_reply(text):
    t = text.lower()
    for key, answer in RULES.items():
        if key in t:
            return answer
    return "I'm in offline mode. Set ANTHROPIC_API_KEY for full answers."

def main():
    print("Chatbot ready" + (" (Claude)" if API_KEY else " (offline mode)") + ". Type 'quit' to exit.")
    history = []
    while True:
        user = input("You: ").strip()
        if user.lower() in {"quit", "exit"}:
            break
        if not user:
            continue
        history.append({"role": "user", "content": user})
        try:
            reply = claude_reply(history) if API_KEY else offline_reply(user)
        except Exception as e:
            reply = f"(API error: {e})"
        history.append({"role": "assistant", "content": reply})
        print("Bot:", reply)

if __name__ == "__main__":
    main()
