import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
import joblib

# Load your dataset
df = pd.read_csv("reviews.csv")

# Features and labels
X = df["text_"]
y = df["label"].map({"CG": "fake", "OR": "real"})  # ✅ Map to fake/real

# Split data
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# TF-IDF vectorizer
tfidf = TfidfVectorizer()
X_train_tfidf = tfidf.fit_transform(X_train)
X_test_tfidf = tfidf.transform(X_test)

# Train model
model = LogisticRegression()
model.fit(X_train_tfidf, y_train)

# Accuracy
print("Accuracy:", model.score(X_test_tfidf, y_test))

# Save model and vectorizer
joblib.dump(model, "model.joblib")
joblib.dump(tfidf, "tfidf.joblib")
print("✅ Model trained and saved with your dataset!")
