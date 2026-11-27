"""Score how well a resume matches a job description.

Usage: python scorer.py resume.txt job.txt
"""
import re
import sys
from sklearn.feature_extraction.text import ENGLISH_STOP_WORDS, TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def words(text):
    return {w for w in re.findall(r"[a-zA-Z+#.]{2,}", text.lower())
            if w not in ENGLISH_STOP_WORDS}

def score(resume, job):
    vec = TfidfVectorizer(stop_words="english", ngram_range=(1, 2))
    m = vec.fit_transform([resume, job])
    similarity = cosine_similarity(m[0], m[1])[0][0]
    missing = sorted(words(job) - words(resume))
    return round(similarity * 100, 1), missing

if __name__ == "__main__":
    if len(sys.argv) != 3:
        sys.exit("Usage: python scorer.py resume.txt job.txt")
    resume, job = (open(p, encoding="utf-8").read() for p in sys.argv[1:3])
    pct, missing = score(resume, job)
    print(f"Match score: {pct}%")
    print("Keywords in the job description but missing from your resume:")
    print(", ".join(missing[:25]) or "none")
