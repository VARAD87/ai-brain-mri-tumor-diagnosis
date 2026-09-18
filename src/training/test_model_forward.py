import torch
from src.models.cnn_baseline import CNNBaseline
from src.training.kaggle_dataset import KaggleBrainMRIDataset
from torch.utils.data import DataLoader


def main():
    dataset = KaggleBrainMRIDataset(
        "data/processed/kaggle/training"
    )

    loader = DataLoader(
        dataset,
        batch_size=8,
        shuffle=True,
        num_workers=0
    )

    images, labels = next(iter(loader))

    model = CNNBaseline(num_classes=4)

    outputs = model(images)

    print("Input shape :", images.shape)
    print("Output shape:", outputs.shape)
    print("Sample logits:", outputs[0])


if __name__ == "__main__":
    main()
