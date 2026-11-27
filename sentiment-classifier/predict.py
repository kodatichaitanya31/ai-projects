"""Usage: python predict.py "your text here"  (or run with no args for a prompt)."""
import pickle
import sys

with open("model.pkl", "rb") as f:
    model = pickle.load(f)

def predict(text):
    p = model.predict_proba([text])[0]
    return ("positive" if p[1] >= 0.5 else "negative"), max(p)

if len(sys.argv) > 1:
    texts = [" ".join(sys.argv[1:])]
else:
    texts = [input("Enter text: ")]

for t in texts:
    label, conf = predict(t)
    print(f"{label} ({conf:.0%} confident)")
