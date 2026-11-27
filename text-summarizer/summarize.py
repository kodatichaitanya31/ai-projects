"""Extractive text summarizer (no external libraries).

Usage: python summarize.py article.txt [number_of_sentences]
"""
import re
import sys
from collections import Counter

STOP = set("a an the and or but if of to in on for with is are was were be it this that as at by from "
           "i you he she we they his her their our my not no so than then".split())

def summarize(text, n=3):
    sentences = re.split(r"(?<=[.!?])\s+", text.strip())
    if len(sentences) <= n:
        return text.strip()
    freq = Counter(w for w in re.findall(r"[a-z']+", text.lower()) if w not in STOP)
    def score(s):
        tokens = re.findall(r"[a-z']+", s.lower())
        return sum(freq[t] for t in tokens) / (len(tokens) or 1)
    top = sorted(range(len(sentences)), key=lambda i: score(sentences[i]), reverse=True)[:n]
    return " ".join(sentences[i] for i in sorted(top))  # keep original order

if __name__ == "__main__":
    if len(sys.argv) < 2:
        sys.exit("Usage: python summarize.py article.txt [sentences]")
    n = int(sys.argv[2]) if len(sys.argv) > 2 else 3
    print(summarize(open(sys.argv[1], encoding="utf-8").read(), n))
