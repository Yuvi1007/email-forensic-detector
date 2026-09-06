from data_loader.load_emails import load_dataset

dataset_path = "dataset"

data = load_dataset(dataset_path)

print("Total emails loaded:", len(data))
print("Sample entry:")
print(data[0][0][:500])  # first 500 characters
print("Label:", data[0][1])