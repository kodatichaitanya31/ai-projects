# Enterprise Helpdesk AI

An AI-powered internal support platform for enterprises. Employees raise tickets; the system
automatically routes each one, sets its priority and SLA, finds relevant knowledge-base
articles and drafts a reply for the support agent.

## Features
- **AI triage** - TF-IDF + Logistic Regression routes tickets to IT, HR, Finance or Facilities
- **Priority & SLA engine** - HIGH (4h), MEDIUM (24h), LOW (72h)
- **Knowledge-base search** - suggests help articles and a draft reply for every ticket
- **Optional Claude integration** - set `ANTHROPIC_API_KEY` for AI-written replies
- **Dashboard** - live counts by priority and department, resolve tickets in one click
- **REST API**, **SQLite** storage, **unit tests**, **Docker** support

## Run
```bash
pip install -r requirements.txt
python app.py                       # http://127.0.0.1:5000
python -m unittest discover tests   # run tests
docker build -t helpdesk-ai . && docker run -p 5000:5000 helpdesk-ai
```

## API
| Method | Endpoint | Purpose |
|---|---|---|
| POST | `/api/tickets` | create a ticket `{"subject","body"}` |
| GET | `/api/tickets?status=open` | list tickets |
| POST | `/api/tickets/<id>/resolve` | resolve a ticket |
| GET | `/api/stats` | open tickets by department / priority |
| GET | `/api/kb?q=...` | search the knowledge base |

```bash
curl -X POST localhost:5000/api/tickets -H 'Content-Type: application/json' \
  -d '{"subject":"VPN down","body":"VPN is down for the whole office"}'
```

## Structure
`app.py` routes - `triage.py` AI routing - `kb.py` knowledge base - `ai.py` Claude replies -
`db.py` storage - `page.py` dashboard - `tests/` unit tests
