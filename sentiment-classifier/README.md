# Sentiment Classifier

A small text classifier (TF-IDF + Logistic Regression) that labels text positive or negative.

```bash
pip install scikit-learn
python train.py
python predict.py "I really loved this, great quality"
```

The built-in dataset is tiny and only for learning. For real use, swap in a larger
dataset such as IMDB reviews by editing the `POS`/`NEG` lists in `train.py`.
