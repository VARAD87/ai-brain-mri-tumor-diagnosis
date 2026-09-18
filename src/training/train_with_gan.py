import torch
import torch.nn as nn
from torch.utils.data import DataLoader

from src.models.cnn_baseline import CNNBaseline
from src.training.augmented_dataset import AugmentedBrainDataset


def main():
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

    dataset = AugmentedBrainDataset(
        base_dir="data/raw/kaggle/training",
        gan_dir="data/augmented/glioma_fake"
    )

    loader = DataLoader(dataset, batch_size=32, shuffle=True)

    model = CNNBaseline(num_classes=4).to(device)

    criterion = nn.CrossEntropyLoss()
    optimizer = torch.optim.Adam(model.parameters(), lr=1e-4)

    epochs = 3

    for epoch in range(epochs):
        model.train()
        total_loss = 0

        for images, labels in loader:
            images, labels = images.to(device), labels.to(device)

            optimizer.zero_grad()
            outputs = model(images)
            loss = criterion(outputs, labels)

            loss.backward()
            optimizer.step()
            total_loss += loss.item()

        print(f"Epoch [{epoch+1}/{epochs}] Loss: {total_loss/len(loader):.4f}")

    torch.save(model.state_dict(), "saved_models/cnn_gan_augmented.pth")
    print(" GAN-Augmented CNN model saved!")


if __name__ == "__main__":
    main()
