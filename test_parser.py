from data_loader.load_emails import load_dataset
from parser.header_parser import parse_email_header

dataset_path = "dataset"
data = load_dataset(dataset_path)

email_content, label = data[0]

parsed_header = parse_email_header(email_content)

print("Parsed Header:")
for key, value in parsed_header.items():
    print(f"{key}: {value}")