import torch
import torch.nn as nn
from torch.utils.data import DataLoader

from src.segmentation.unet import UNet
from src.segmentation.dataset import MRISegmentationDataset


# Dice Score Metric
def dice_score(pred, target):
    smooth = 1.0
    pred = (pred > 0.5).float()

    intersection = (pred * target).sum()
    return (2. * intersection + smooth) / (pred.sum() + target.sum() + smooth)


def main():
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    print("Using device:", device)

   
    dataset = MRISegmentationDataset("data/processed/kaggle/training")
    loader = DataLoader(dataset, batch_size=4, shuffle=True)

   
    model = UNet().to(device)

  
    criterion = nn.BCELoss()
    optimizer = torch.optim.Adam(model.parameters(), lr=1e-4)

    epochs = 3

    for epoch in range(epochs):
        model.train()
        total_loss = 0
        total_dice = 0

        for images, masks in loader:
            images, masks = images.to(device), masks.to(device)

            optimizer.zero_grad()

            outputs = model(images)
            loss = criterion(outputs, masks)

            loss.backward()
            optimizer.step()

            total_loss += loss.item()
            total_dice += dice_score(outputs, masks).item()

        print(
            f"Epoch [{epoch+1}/{epochs}] "
            f"Loss: {total_loss/len(loader):.4f} "
            f"Dice: {total_dice/len(loader):.4f}"
        )

    # Save model
    torch.save(model.state_dict(), "saved_models/unet_segmentation.pth")
    print(" U-Net model saved to saved_models/unet_segmentation.pth")


if __name__ == "__main__":
    main()
