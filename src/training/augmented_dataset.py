import os
import cv2
import torch
import numpy as np
from torch.utils.data import Dataset


CLASS_MAP = {
    "glioma": 0,
    "meningioma": 1,
    "notumor": 2,
    "pituitary": 3
}


class AugmentedBrainDataset(Dataset):
    def __init__(self, base_dir, gan_dir=None, img_size=224):
        self.img_size = img_size
        self.samples = []

        # Load real Kaggle training images
        for cls in CLASS_MAP.keys():
            folder = os.path.join(base_dir, cls)
            for file in os.listdir(folder):
                self.samples.append((os.path.join(folder, file), CLASS_MAP[cls]))

        # Load GAN-generated images (only glioma)
        if gan_dir:
            for file in os.listdir(gan_dir):
                self.samples.append((os.path.join(gan_dir, file), 0))

        print(" Total samples with GAN augmentation:", len(self.samples))

    def __len__(self):
        return len(self.samples)

    def __getitem__(self, idx):
        img_path, label = self.samples[idx]

        img = cv2.imread(img_path)
        img = cv2.resize(img, (self.img_size, self.img_size))
        img = img.astype(np.float32) / 255.0

        img = torch.tensor(img).permute(2, 0, 1)
        label = torch.tensor(label)

        return img, label
