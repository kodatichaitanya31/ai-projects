"""Enterprise Helpdesk AI - run: python app.py  then open http://127.0.0.1:5000

Web dashboard + REST API:
  POST /api/tickets {"subject","body"}  -> creates a triaged ticket
  GET  /api/tickets?status=open         -> list tickets
  POST /api/tickets/<id>/resolve        -> resolve a ticket
  GET  /api/stats                       -> open-ticket counts
  GET  /api/kb?q=...                    -> search the knowledge base
"""
import os

from flask import Flask, jsonify, redirect, render_template_string, request

import ai
import db
import kb
from page import PAGE
from triage import triage

app = Flask(__name__)

def create_ticket(subject, body):
    text = f"{subject}. {body}"
    result = triage(text)
    articles = kb.search(text)
    suggestion = ai.draft_reply(subject, body, articles)
    tid = db.add(subject, body, result["dept"], result["priority"],
                 result["confidence"], result["sla_hours"], suggestion)
    return {"id": tid, **result, "suggestion": suggestion, "articles": articles}

@app.get("/")
def dashboard():
    return render_template_string(PAGE, tickets=db.get_all("open"), stats=db.stats())

@app.post("/tickets")
def form_ticket():
    create_ticket(request.form["subject"].strip(), request.form["body"].strip())
    return redirect("/")

@app.post("/tickets/<int:tid>/resolve")
def form_resolve(tid):
    db.resolve(tid)
    return redirect("/")

@app.post("/api/tickets")
def api_create():
    data = request.get_json(silent=True) or {}
    subject, body = str(data.get("subject", "")).strip(), str(data.get("body", "")).strip()
    if not subject or not body:
        return jsonify(error="subject and body are required"), 400
    return jsonify(create_ticket(subject, body)), 201

@app.get("/api/tickets")
def api_list():
    return jsonify(db.get_all(request.args.get("status")))

@app.post("/api/tickets/<int:tid>/resolve")
def api_resolve(tid):
    if not db.resolve(tid):
        return jsonify(error="ticket not found"), 404
    return jsonify(status="resolved")

@app.get("/api/stats")
def api_stats():
    return jsonify(db.stats())

@app.get("/api/kb")
def api_kb():
    return jsonify(kb.search(request.args.get("q", "")))

db.init()

if __name__ == "__main__":
    app.run(host=os.environ.get("HELPDESK_HOST", "127.0.0.1"), port=5000)
