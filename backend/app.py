from flask import Flask, request, jsonify
import joblib
from flask_cors import CORS  # ✅ Add this

app = Flask(__name__)
CORS(app)  # ✅ Allow requests from any origin (React frontend)

# Load your trained model + vectorizer
model = joblib.load("model.pkl")
vectorizer = joblib.load("vectorizer.pkl")

@app.route("/predict", methods=["POST"])
def predict():
    data = request.get_json()
    review_text = data["review"]

    # Convert review into features
    features = vectorizer.transform([review_text])
    prediction = model.predict(features)[0]

    label = "Fake" if prediction == "CG" else "Real"

    return jsonify({"prediction": label})

if __name__ == "__main__":
    app.run(debug=True)
