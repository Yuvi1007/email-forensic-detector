import os
import pandas as pd
import joblib
import matplotlib.pyplot as plt

from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    classification_report,
    roc_curve,
    auc,
    precision_recall_curve
)

from data_loader.load_emails import load_dataset
from parser.header_parser import parse_email_header
from forensic_features.feature_engineering import engineer_features


def plot_roc_curve(fpr, tpr, roc_auc):
    """
    Generate and save ROC curve graph
    """
    plt.figure(figsize=(8, 6))

    plt.plot(fpr, tpr, color='darkorange', lw=2, label=f"ROC Curve (AUC = {roc_auc:.2f})")

    plt.plot([0, 1], [0, 1], color='navy', lw=2, linestyle="--", label="Random Classifier")

    plt.xlim([0.0, 1.0])
    plt.ylim([0.0, 1.05])

    plt.xlabel("False Positive Rate", fontsize=12)
    plt.ylabel("True Positive Rate", fontsize=12)
    plt.title("ROC Curve - Email Spam Detector", fontsize=14, fontweight='bold')

    plt.legend(loc="lower right", fontsize=11)

    plt.grid(alpha=0.3)

    os.makedirs("saved_model", exist_ok=True)

    plt.savefig("saved_model/roc_curve.png", dpi=300, bbox_inches='tight')
    print("ROC Curve saved to saved_model/roc_curve.png")

    plt.show()


def plot_precision_recall_curve(precision, recall, pr_auc):
    """
    Generate and save Precision-Recall curve graph
    """
    plt.figure(figsize=(8, 6))

    plt.plot(recall, precision, color='green', lw=2, label=f"Precision-Recall Curve (AUC = {pr_auc:.2f})")

    plt.axhline(y=0.5, color='red', lw=2, linestyle="--", label="Baseline")

    plt.xlim([0.0, 1.0])
    plt.ylim([0.0, 1.05])

    plt.xlabel("Recall", fontsize=12)
    plt.ylabel("Precision", fontsize=12)
    plt.title("Precision-Recall Curve - Email Spam Detector", fontsize=14, fontweight='bold')

    plt.legend(loc="best", fontsize=11)

    plt.grid(alpha=0.3)

    os.makedirs("saved_model", exist_ok=True)

    plt.savefig("saved_model/precision_recall_curve.png", dpi=300, bbox_inches='tight')
    print("Precision-Recall Curve saved to saved_model/precision_recall_curve.png")

    plt.show()


def prepare_dataset(dataset_path):

    raw_data = load_dataset(dataset_path)

    features_list = []
    labels = []

    for email_content, label in raw_data:

        header = parse_email_header(email_content)

        features = engineer_features(header, email_content)

        features_list.append(features)

        labels.append(label)

    df = pd.DataFrame(features_list)
    df["label"] = labels

    return df


def train_model(dataset_path):

    df = prepare_dataset(dataset_path)

    X = df.drop("label", axis=1)
    y = df["label"]

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    model = RandomForestClassifier()

    model.fit(X_train, y_train)

    y_prob = model.predict_proba(X_test)[:, 1]

    precision, recall, _ = precision_recall_curve(y_test, y_prob)

    pr_auc = auc(recall, precision)

    plot_precision_recall_curve(precision, recall, pr_auc)

    # -------- 
    y_pred = model.predict(X_test)

    # -------- Evaluation Metrics --------

    accuracy = accuracy_score(y_test, y_pred)
    precision = precision_score(y_test, y_pred)
    recall = recall_score(y_test, y_pred)
    f1 = f1_score(y_test, y_pred)

    print("\nModel Evaluation Metrics")
    print("---------------------------")
    print("Accuracy :", accuracy)
    print("Precision:", precision)
    print("Recall   :", recall)
    print("F1 Score :", f1)

    print("\nClassification Report")
    print(classification_report(y_test, y_pred))

    # -------- ROC Curve --------

    y_prob = model.predict_proba(X_test)[:, 1]

    fpr, tpr, thresholds = roc_curve(y_test, y_prob)

    roc_auc = auc(fpr, tpr)

    plot_roc_curve(fpr, tpr, roc_auc)

    # -------- Save Model --------

    os.makedirs("saved_model", exist_ok=True)

    joblib.dump(model, "saved_model/model.pkl")

    print("\nModel saved to saved_model/model.pkl")


if __name__ == "__main__":
    train_model("dataset")