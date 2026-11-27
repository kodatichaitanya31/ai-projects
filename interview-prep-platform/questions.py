"""Skill bank, skill detection and offline question/feedback engine."""
import re

SKILLS = {
    "python": ["Explain the difference between a list and a tuple in Python.",
               "How do decorators work in Python? Give a use case."],
    "java": ["Explain how the JVM manages memory and garbage collection.",
             "What is the difference between an interface and an abstract class?"],
    "javascript": ["Explain closures and a practical use of them.",
                   "What is the event loop in JavaScript?"],
    "react": ["How do hooks like useState and useEffect work?",
              "How do you avoid unnecessary re-renders in React?"],
    "sql": ["Explain the difference between INNER JOIN and LEFT JOIN.",
            "How would you optimize a slow SQL query?"],
    "machine learning": ["Explain overfitting and how you would prevent it.",
                         "How do you choose evaluation metrics for a classification model?"],
    "aws": ["How would you design a highly available web app on AWS?",
            "What is the difference between EC2 and Lambda?"],
    "docker": ["What is the difference between an image and a container?",
               "How do you reduce a Docker image's size?"],
    "git": ["Explain the difference between merge and rebase.",
            "How do you resolve a merge conflict?"],
    "node": ["How does Node.js handle concurrency?",
             "How would you structure a REST API in Express?"],
    "django": ["Explain Django's MVT architecture.", "How do Django migrations work?"],
    "flask": ["How does Flask differ from Django?", "How do you structure a larger Flask app?"],
    "c++": ["Explain RAII and smart pointers in C++.",
            "What is the difference between a pointer and a reference?"],
    "kubernetes": ["What is a Pod, and how does a Deployment manage it?"],
    "data structures": ["When would you use a hash map instead of a tree?"],
    "html": ["What is semantic HTML and why does it matter?"],
    "css": ["Explain the CSS box model and flexbox vs grid."],
}
GENERAL = [
    "Tell me about yourself and walk me through your resume.",
    "Describe the most challenging project on your resume and your exact role.",
    "Tell me about a time you faced a conflict in a team and how you handled it.",
    "Why do you want this role, and where do you see yourself in 3 years?",
    "Tell me about a mistake you made and what you learned.",
]

def find_skills(text):
    low = text.lower()
    found = []
    for skill in SKILLS:
        pattern = r"(?<![a-z0-9+])" + re.escape(skill) + r"(?![a-z0-9+])"
        if re.search(pattern, low):
            found.append(skill)
    return found

def offline_questions(skills):
    qs = list(GENERAL[:2])
    for s in skills:
        qs += SKILLS[s]
    qs += GENERAL[2:]
    return qs

def offline_feedback(answer):
    words = len(answer.split())
    tips = []
    if words < 40:
        tips.append("Your answer is short. Aim for 80-150 words with a concrete example.")
    if not re.search(r"\d", answer):
        tips.append("Add numbers or measurable results (e.g. 'cut load time by 30%').")
    if not re.search(r"\b(I|my|we)\b", answer, re.I):
        tips.append("Say what YOU did, not only what the team did.")
    return " ".join(tips) or "Good structure. Make sure you state the situation, action and result."

