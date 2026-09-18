import torch.nn as nn


# =====================================================================
# DEEP CONVOLUTIONAL GENERATIVE ADVERSARIAL NETWORK (DCGAN)
# =====================================================================
# Goal: Synthesize realistic brain MRI slices to augment training datasets.
# Consists of two models training against each other:
# 1. Generator: Learns to create highly realistic synthetic scans.
# 2. Discriminator: Learns to classify scans as Real (from dataset) vs Fake (generated).
# =====================================================================

# ---------------- Generator ----------------
# Role: Maps a low-dimensional random latent vector (z_dim) to a 2D image (64x64).
# Algorithm: Fractional-strided convolutions (transposed convolutions) to upscale features.
class Generator(nn.Module):
    def __init__(self, z_dim=100):
        super().__init__()

        self.net = nn.Sequential(
            # Input: Latent vector z of shape (batch, z_dim, 1, 1)
            # Project and upscale to spatial dimension 8x8
            nn.ConvTranspose2d(z_dim, 256, 8, 1, 0),
            nn.BatchNorm2d(256),
            nn.ReLU(True),

            # Upscale spatial dimensions to 16x16
            nn.ConvTranspose2d(256, 128, 4, 2, 1),
            nn.BatchNorm2d(128),
            nn.ReLU(True),

            # Upscale spatial dimensions to 32x32
            nn.ConvTranspose2d(128, 64, 4, 2, 1),
            nn.BatchNorm2d(64),
            nn.ReLU(True),

            # Upscale to final synthetic MRI size 64x64, single-channel (grayscale)
            # Tanh activation bounds pixels between [-1.0, 1.0] for stable training
            nn.ConvTranspose2d(64, 1, 4, 2, 1),
            nn.Tanh()
        )

    def forward(self, z):
        return self.net(z)


# ---------------- Discriminator ----------------
# Role: A binary classification network that evaluates whether an input MRI image is real or fake.
# Algorithm: Standard 2D convolutions downsampling space, outputting a probability score [0.0, 1.0].
class Discriminator(nn.Module):
    def __init__(self):
        super().__init__()

        self.net = nn.Sequential(
            # Input: Grayscale scan of size 64x64. Downsample to 32x32
            nn.Conv2d(1, 64, 4, 2, 1),
            nn.LeakyReLU(0.2),

            # Downsample to 16x16
            nn.Conv2d(64, 128, 4, 2, 1),
            nn.BatchNorm2d(128),
            nn.LeakyReLU(0.2),

            # Flatten feature maps to vector of shape (batch, 128 * 16 * 16)
            nn.Flatten(),
            
            # Linear fully connected decision layer mapping features to single score
            # Sigmoid activation output acts as binary probability (Real = 1, Fake = 0)
            nn.Linear(128 * 16 * 16, 1),
            nn.Sigmoid()
        )

    def forward(self, x):
        return self.net(x)
