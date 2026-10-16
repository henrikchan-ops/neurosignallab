import numpy as np
import torch

from .models import EEGNet


def get_device():
    if torch.backends.mps.is_available():
        return torch.device("mps")

    return torch.device("cpu")


def load_eegnet(checkpoint_path, device=None):
    if device is None:
        device = get_device()

    checkpoint = torch.load(
        checkpoint_path,
        map_location=device
    )

    model = EEGNet(
        n_channels=checkpoint["n_channels"],
        n_classes=checkpoint["n_classes"]
    )

    model.load_state_dict(
        checkpoint["model_state_dict"]
    )

    model = model.to(device)
    model.eval()

    return model, checkpoint, device

def predict_trial(
    model,
    trial,
    checkpoint,
    device
):
    expected_shape = (
        checkpoint["n_channels"],
        checkpoint["n_times"]
    )

    if trial.shape != expected_shape:
        raise ValueError(
            f"Expected trial shape {expected_shape}, "
            f"got {trial.shape}"
        )

    x = torch.tensor(
        trial,
        dtype=torch.float32
    )

    x = x * checkpoint["input_multiplier"]

    x = x.unsqueeze(0)
    x = x.unsqueeze(0)

    x = x.to(device)

    model.eval()

    with torch.inference_mode():
        logits = model(x)

        probabilities = torch.softmax(
            logits,
            dim=1
        )

        prediction = probabilities.argmax(
            dim=1
        ).item()
        predicted_class = checkpoint["class_names"][
            prediction
        ]

    result = {
        "prediction": prediction,
        "predicted_class": predicted_class,
        "probabilities": (
            probabilities
            .squeeze(0)
            .cpu()
            .numpy()
        ),
        "logits": (
            logits
            .squeeze(0)
            .cpu()
            .numpy()
        )
    }

    return result