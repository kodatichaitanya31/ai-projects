"""Train a tiny sentiment classifier and save it to model.pkl."""
import pickle
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.pipeline import make_pipeline
from sklearn.metrics import classification_report

POS = [
    "I love this product, it works great", "Absolutely fantastic experience",
    "Very happy with the quality", "Excellent service and fast delivery",
    "This is the best purchase I have made", "Amazing, would recommend to everyone",
    "Wonderful and easy to use", "Superb value for money",
    "I am delighted with the results", "Great movie, loved every minute",
    "The staff were friendly and helpful", "Brilliant design and performance",
    "Totally worth it", "Really impressed, five stars", "Smooth, quick and reliable",
]
NEG = [
    "I hate this product, it broke immediately", "Terrible experience overall",
    "Very disappointed with the quality", "Awful service and late delivery",
    "This is the worst purchase I have made", "Do not buy, complete waste of money",
    "Confusing and hard to use", "Overpriced and poorly made",
    "I am frustrated with the results", "Boring movie, I wanted to leave",
    "The staff were rude and unhelpful", "Ugly design and slow performance",
    "Totally not worth it", "Really let down, one star", "Buggy, slow and unreliable",
]

texts = POS + NEG
labels = [1] * len(POS) + [0] * len(NEG)

X_tr, X_te, y_tr, y_te = train_test_split(
    texts, labels, test_size=0.25, random_state=42, stratify=labels)

model = make_pipeline(
    TfidfVectorizer(ngram_range=(1, 2), lowercase=True),
    LogisticRegression(max_iter=1000),
)
model.fit(X_tr, y_tr)
print(classification_report(y_te, model.predict(X_te), target_names=["negative", "positive"]))

model.fit(texts, labels)  # refit on everything
with open("model.pkl", "wb") as f:
    pickle.dump(model, f)
print("Saved model.pkl")
