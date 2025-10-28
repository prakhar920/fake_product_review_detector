import pandas as pd
import joblib
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics import classification_report, accuracy_score
from sklearn.utils import resample
from xgboost import XGBClassifier

# -----------------------------
# 1️⃣ Load dataset
# -----------------------------
df = pd.read_csv("reviews_cleaned.csv")
print(f"✅ Dataset loaded: {df.shape}")

# Drop missing values
df = df.dropna(subset=["text", "label"])
df["text"] = df["text"].astype(str).str.strip()

# -----------------------------
# 2️⃣ Normalize and encode labels
# -----------------------------
# Convert CG → fake, OR → real
df["label"] = df["label"].replace({"CG": "fake", "OR": "real"}).str.lower()

# Encode to numbers (fake=0, real=1)
le = LabelEncoder()
df["label_encoded"] = le.fit_transform(df["label"])
print(f"⚙️ Label encoding: {dict(zip(le.classes_, le.transform(le.classes_)))}")

# -----------------------------
# 3️⃣ Balance dataset
# -----------------------------
real = df[df["label"] == "real"]
fake = df[df["label"] == "fake"]

if len(real) > 0 and len(fake) > 0:
    if len(real) > len(fake):
        fake = resample(fake, replace=True, n_samples=len(real), random_state=42)
    elif len(fake) > len(real):
        real = resample(real, replace=True, n_samples=len(fake), random_state=42)
    df_balanced = pd.concat([real, fake])
else:
    print("⚠️ Labels not found properly. Check your CSV ‘label’ column values.")
    df_balanced = df

print(f"⚖️ Balanced dataset: {df_balanced['label'].value_counts().to_dict()}")

# -----------------------------
# 4️⃣ Split data
# -----------------------------
X = df_balanced["text"]
y = df_balanced["label_encoded"]

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# -----------------------------
# 5️⃣ TF-IDF Vectorization
# -----------------------------
vectorizer = TfidfVectorizer(
    max_features=7000,
    ngram_range=(1, 2),
    stop_words='english'
)
X_train_vec = vectorizer.fit_transform(X_train)
X_test_vec = vectorizer.transform(X_test)

# -----------------------------
# 6️⃣ Train XGBoost Model
# -----------------------------
print("🚀 Training XGBoost model (takes 30–40 sec)...")
model = XGBClassifier(
    n_estimators=300,
    learning_rate=0.1,
    max_depth=6,
    subsample=0.8,
    colsample_bytree=0.8,
    eval_metric='logloss',
    use_label_encoder=False
)
model.fit(X_train_vec, y_train)

# -----------------------------
# 7️⃣ Evaluate Model
# -----------------------------
y_pred = model.predict(X_test_vec)
print("\n📊 Classification Report:\n")
print(classification_report(y_test, y_pred, target_names=le.classes_))
print(f"🎯 Accuracy: {accuracy_score(y_test, y_pred)*100:.2f}%")

# -----------------------------
# 8️⃣ Save model and vectorizer
# -----------------------------
joblib.dump(model, "model.pkl")
joblib.dump(vectorizer, "vectorizer.pkl")
joblib.dump(le, "label_encoder.pkl")

print("\n✅ Model, vectorizer, and encoder saved successfully!")
