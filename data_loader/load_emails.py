import os 
def load_emails_from_folder(folder_path, label):
    emails = []
    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)
        if os.path.isfile(file_path):
            try:
                with open(file_path, "r", encoding="latin-1") as f:
                    content = f.read()
                    emails.append((content, label))
            except Exception as e:
                print(f"Error reading file {file_path}: {e}")
    return emails
def load_dataset(base_path):
    dataset = []
    easy_ham_path = os.path.join(base_path, "easy_ham")
    hard_ham_path = os.path.join(base_path, "hard_ham")
    spam_path = os.path.join(base_path, "spam")
    dataset.extend(load_emails_from_folder(easy_ham_path, 0))
    dataset.extend(load_emails_from_folder(hard_ham_path, 0))
    dataset.extend(load_emails_from_folder(spam_path, 1))   
    return dataset        