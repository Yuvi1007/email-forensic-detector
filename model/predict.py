import joblib
import pandas as pd

from parser.header_parser import parse_email_header
from forensic_features.feature_engineering import engineer_features


model = joblib.load("saved_model/model.pkl")


def predict_email(email_content):

    header = parse_email_header(email_content)

    features = engineer_features(header, email_content)

    feature_df = pd.DataFrame([features])

    prediction = model.predict(feature_df)[0]

    probability = model.predict_proba(feature_df)[0]

    confidence = max(probability)

    result = {
        "prediction": "Spam" if prediction == 1 else "Ham",
        "confidence": round(confidence * 100, 2),
        "features": features
    }

    return result