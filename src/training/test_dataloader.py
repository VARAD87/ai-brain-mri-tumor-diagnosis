from torch.utils.data import DataLoader
from src.training.kaggle_dataset import KaggleBrainMRIDataset


def main():
    train_dataset = KaggleBrainMRIDataset(
        "data/processed/kaggle/training"
    )

    test_dataset = KaggleBrainMRIDataset(
        "data/processed/kaggle/testing"
    )

    train_loader = DataLoader(
        train_dataset,
        batch_size=32,
        shuffle=True,
        num_workers=0
    )

    test_loader = DataLoader(
        test_dataset,
        batch_size=32,
        shuffle=False,
        num_workers=0
    )

    # Test one batch
    images, labels = next(iter(train_loader))

    print("Batch images shape:", images.shape)
    print("Batch labels shape:", labels.shape)
    print("Labels:", labels[:10])


if __name__ == "__main__":
    main()
