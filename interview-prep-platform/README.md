# AI Interview Prep Platform

Upload your resume and practice for interviews. The app reads your resume (PDF, DOCX or TXT),
detects your skills, generates interview questions, and gives feedback on your answers.

## Features
- Resume upload with text extraction
- Skill detection and tailored technical + behavioral questions
- Answer feedback (offline tips, or full AI feedback with Claude)
- Works with no API key; set `ANTHROPIC_API_KEY` for resume-specific AI questions

## Run
```bash
pip install -r requirements.txt
python app.py          # open http://127.0.0.1:5000
```
Optional: `export ANTHROPIC_API_KEY=your_key`

## Ideas to extend
User accounts, saved sessions, voice answers, mock-interview scoring history.
