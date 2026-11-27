"""Ask questions about the .txt files in ./docs using TF-IDF retrieval.

Usage: python qa.py "What is RAG?"      (or run with no args for interactive mode)
"""
import glob
import re
import sys
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def load_chunks(folder="docs"):
    chunks = []
    for path in sorted(glob.glob(f"{folder}/*.txt")):
        with open(path, encoding="utf-8") as f:
            for para in re.split(r"\n\s*\n", f.read()):
                para = para.strip()
                if para:
                    chunks.append((path, para))
    return chunks

chunks = load_chunks()
if not chunks:
    sys.exit("No .txt files found in ./docs")

vectorizer = TfidfVectorizer(stop_words="english")
matrix = vectorizer.fit_transform([c[1] for c in chunks])

def ask(question, k=2):
    scores = cosine_similarity(vectorizer.transform([question]), matrix)[0]
    top = scores.argsort()[::-1][:k]
    return [(chunks[i][0], chunks[i][1], scores[i]) for i in top if scores[i] > 0]

def show(question):
    results = ask(question)
    if not results:
        print("No relevant answer found in the documents.")
    for path, text, score in results:
        print(f"[{path} | relevance {score:.2f}]\n{text}\n")

if len(sys.argv) > 1:
    show(" ".join(sys.argv[1:]))
else:
    print("Ask a question (blank line to quit)")
    while (q := input("> ").strip()):
        show(q)
