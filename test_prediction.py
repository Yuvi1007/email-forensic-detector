from data_loader.load_emails import load_dataset
from model.predict import predict_email

dataset_path = "dataset"

data = load_dataset(dataset_path)

email_content, label = data[10]

result = predict_email(email_content)

print("Prediction Result:\n")

print("Prediction:", result["prediction"])
print("Confidence:", result["confidence"], "%")

print("\nExtracted Features:")

for k, v in result["features"].items():
    print(k, ":", v)

print("\nActual Label:", label)