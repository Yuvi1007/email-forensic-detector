from data_loader.load_emails import load_dataset
from parser.header_parser import parse_email_header
from forensic_features.feature_engineering import engineer_features
from model.predict import predict_email
from report.generate_report import generate_forensic_report


dataset_path = "dataset"

data = load_dataset(dataset_path)

email_content, label = data[20]

# Parse header
header = parse_email_header(email_content)

# Feature extraction
features = engineer_features(header)

# Prediction
prediction = predict_email(email_content)

# Generate report
report = generate_forensic_report(header, features, prediction)

print("\nFORENSIC EMAIL ANALYSIS REPORT\n")

for section, content in report.items():
    print(f"\n--- {section} ---")
    print(content)

print("\nActual Label:", label)