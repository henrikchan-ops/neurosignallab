import torch
import torch.nn as nn


class EEGNet(nn.Module):
    def __init__(
        self,
        n_channels=64,
        n_classes=2,
        F1=8,
        D=2,
        F2=16,
        temporal_kernel=40,
        separable_kernel=16,
        dropout_p=0.5
    ):
        super().__init__()

        self.block1 = nn.Sequential(
            nn.Conv2d(
                1,
                F1,
                (1, temporal_kernel),
                padding="same",
                bias=False
            ),
            nn.BatchNorm2d(F1),

            nn.Conv2d(
                F1,
                F1 * D,
                (n_channels, 1),
                groups=F1,
                bias=False
            ),
            nn.BatchNorm2d(F1 * D),

            nn.ELU(),
            nn.AvgPool2d((1, 4)),
            nn.Dropout(dropout_p)
        )

        self.block2 = nn.Sequential(
            nn.Conv2d(
                F1 * D,
                F1 * D,
                (1, separable_kernel),
                padding="same",
                groups=F1 * D,
                bias=False
            ),

            nn.Conv2d(
                F1 * D,
                F2,
                (1, 1),
                bias=False
            ),

            nn.BatchNorm2d(F2),
            nn.ELU(),
            nn.AvgPool2d((1, 8)),
            nn.Dropout(dropout_p)
        )

        self.classifier = nn.Linear(
            F2 * 15,
            n_classes
        )

    def forward(self, x):
        x = self.block1(x)
        x = self.block2(x)

        x = torch.flatten(
            x,
            start_dim=1
        )

        return self.classifier(x)
