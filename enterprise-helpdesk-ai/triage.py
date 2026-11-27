"""AI triage: routes a ticket to a department and assigns priority + SLA."""
import re
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import make_pipeline

DATA = {
    "IT": ["I cannot log in to my laptop", "VPN keeps disconnecting", "Email is not syncing on my phone",
           "Need software installed on my computer", "Printer on floor 3 is not working",
           "Server is down and the website is not loading", "Forgot my password and my account is locked",
           "Wifi is very slow in the office", "Laptop screen is broken", "Cannot access the shared drive"],
    "HR": ["I want to apply for annual leave", "Question about my payslip", "Update my bank details for salary",
           "Need information on health insurance benefits", "Request for maternity leave policy",
           "Complaint about workplace behaviour", "Onboarding documents for a new joiner",
           "How many sick days do I have left", "Request for employment verification letter"],
    "Finance": ["Invoice has not been paid by the client", "Need reimbursement for travel expenses",
                "Purchase order approval is pending", "Wrong amount charged on the vendor bill",
                "Budget approval for the new project", "Tax deduction question for this quarter",
                "Expense report was rejected", "Need a corporate credit card", "Vendor payment is overdue"],
    "Facilities": ["Air conditioning is not working in the meeting room", "Need a new desk and chair",
                   "Water leak in the pantry", "Office lights are flickering", "Request for parking permit",
                   "Elevator is out of order", "Security badge does not open the door",
                   "Meeting room booking system is broken", "Office is too cold"],
}
HIGH = r"\b(down|outage|urgent|asap|immediately|critical|breach|leak|security|everyone|whole office|production)\b"
MEDIUM = r"\b(slow|broken|not working|cannot|can't|failed|rejected|overdue|pending)\b"
SLA = {"HIGH": 4, "MEDIUM": 24, "LOW": 72}

_texts = [t for items in DATA.values() for t in items]
_labels = [d for d, items in DATA.items() for _ in items]
_model = make_pipeline(TfidfVectorizer(ngram_range=(1, 2)), LogisticRegression(max_iter=1000, C=10))
_model.fit(_texts, _labels)

def priority_of(text):
    low = text.lower()
    if re.search(HIGH, low):
        return "HIGH"
    return "MEDIUM" if re.search(MEDIUM, low) else "LOW"

def triage(text):
    probs = _model.predict_proba([text])[0]
    best = probs.argmax()
    priority = priority_of(text)
    return {"dept": _model.classes_[best], "confidence": round(float(probs[best]), 2),
            "priority": priority, "sla_hours": SLA[priority]}
