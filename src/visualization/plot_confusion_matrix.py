import os
import torch
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from torch.utils.data import DataLoader
from sklearn.metrics import confusion_matrix

from src.models.cnn_baseline import CNNBaseline
from src.training.kaggle_dataset import KaggleBrainMRIDataset


CLASS_NAMES = ["Glioma", "Meningioma", "No Tumor", "Pituitary"]


def main():
    # ---- DEBUG: show where Python is running from ----
    print("Current working directory:", os.getcwd())

    # ---- ENSURE output directory exists ----
    output_dir = os.path.join("reports", "figures")
    os.makedirs(output_dir, exist_ok=True)

    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    print("Using device:", device)

    test_dataset = KaggleBrainMRIDataset(
        "data/processed/kaggle/testing"
    )
    test_loader = DataLoader(test_dataset, batch_size=32, shuffle=False)

    model = CNNBaseline(num_classes=4)
    model.load_state_dict(
        torch.load("saved_models/cnn_baseline.pth", map_location=device)
    )
    model.to(device)
    model.eval()

    all_preds = []
    all_labels = []

    with torch.no_grad():
        for images, labels in test_loader:
            images = images.to(device)
            outputs = model(images)
            _, preds = torch.max(outputs, 1)

            all_preds.extend(preds.cpu().numpy())
            all_labels.extend(labels.numpy())

    cm = confusion_matrix(all_labels, all_preds)

    # ---- PLOT ----
    plt.figure(figsize=(8, 6))
    sns.heatmap(
        cm,
        annot=True,
        fmt="d",
        cmap="Blues",
        xticklabels=CLASS_NAMES,
        yticklabels=CLASS_NAMES,
    )
    plt.xlabel("Predicted Label")
    plt.ylabel("True Label")
    plt.title("Confusion Matrix — CNN Baseline")

    plt.tight_layout()

    save_path = os.path.join(output_dir, "confusion_matrix.png")
    plt.savefig(save_path, dpi=300)
    print(f" Confusion matrix saved to: {save_path}")

    plt.show()


if __name__ == "__main__":
    main()
