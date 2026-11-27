"""Knowledge base: finds help articles relevant to a ticket (TF-IDF search)."""
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

ARTICLES = [
    ("Reset your password", "Forgot password or account locked: open the self-service portal, choose Reset Password, verify with your phone code and set a new password. Accounts unlock automatically after 30 minutes."),
    ("Fix VPN connection problems", "VPN disconnecting or not connecting: restart the VPN client, check your internet, update the client to the latest version and try another server. Contact IT if the problem continues."),
    ("Apply for leave", "To apply for annual leave open the HR portal, choose Leave, pick the dates and submit for manager approval. Sick leave over 2 days needs a medical certificate."),
    ("Read your payslip", "Payslips are published on the 25th in the HR portal under Payroll. To change bank details submit the bank change form with a cancelled cheque."),
    ("Claim travel expenses", "Submit expense reports within 30 days with receipts attached in the Finance portal. Reimbursement is paid in the next payroll cycle after manager approval."),
    ("Raise a purchase order", "Create purchase orders in the procurement tool. Orders above the budget limit need finance director approval and take up to 3 working days."),
    ("Printer and hardware issues", "For printer, laptop or monitor problems restart the device, check cables and drivers, then raise an IT ticket with the asset tag for replacement."),
    ("Book meeting rooms and request facilities", "Book rooms in the calendar system. For desks, chairs, parking permits, temperature or lighting problems contact Facilities with your floor and seat number."),
    ("Security badge not working", "If your badge does not open doors visit the security desk with photo ID. Lost badges are deactivated immediately and replaced within one day."),
]
_vec = TfidfVectorizer(stop_words="english")
_matrix = _vec.fit_transform([f"{t}. {b}" for t, b in ARTICLES])

def search(query, k=2, min_score=0.08):
    scores = cosine_similarity(_vec.transform([query]), _matrix)[0]
    top = scores.argsort()[::-1][:k]
    return [{"title": ARTICLES[i][0], "text": ARTICLES[i][1], "score": round(float(scores[i]), 2)}
            for i in top if scores[i] >= min_score]
