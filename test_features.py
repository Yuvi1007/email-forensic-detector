from data_loader.load_emails import load_dataset
from parser.header_parser import parse_email_header
from forensic_features.feature_engineering import engineer_features

dataset_path = "dataset"
data = load_dataset(dataset_path)

email_content, label = data[0]

header = parse_email_header(email_content)
features = engineer_features(header)

print("Engineered Features:")
for key, value in features.items():
    print(f"{key}: {value}")

print("Label:", label)