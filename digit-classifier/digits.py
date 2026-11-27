"""Handwritten digit classifier using scikit-learn's built-in 8x8 digits dataset.

Usage: python digits.py        (trains, prints accuracy, shows sample predictions)
"""
from sklearn.datasets import load_digits
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split
from sklearn.svm import SVC

digits = load_digits()
X_train, X_test, y_train, y_test = train_test_split(
    digits.data, digits.target, test_size=0.25, random_state=42)

model = SVC(gamma=0.001)
model.fit(X_train, y_train)
pred = model.predict(X_test)
print(f"Test accuracy: {accuracy_score(y_test, pred):.1%}")

for i in range(5):
    print(f"Sample {i}: predicted {pred[i]}, actual {y_test[i]}")
    print("\n".join("".join("#" if v > 8 else "." for v in row)
                    for row in X_test[i].reshape(8, 8)))
    print()
