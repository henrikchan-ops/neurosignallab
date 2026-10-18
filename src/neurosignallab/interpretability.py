import numpy as np
import torch

from .inference import predict_trial


def compute_saliency(model, trial, checkpoint, device, target_class):
    x = torch.tensor(trial, dtype=torch.float32)
    x = x * checkpoint["input_multiplier"]
    x = x.unsqueeze(0)
    x = x.unsqueeze(0)
    x = x.to(device)

    x.requires_grad_(True)

    model.zero_grad()
    logits = model(x)
    target_logit = logits[0, target_class]

    target_logit.backward()

    gradients = x.grad.detach()
    gradients = gradients.squeeze(0)
    gradients = gradients.squeeze(0)
    gradients = gradients.cpu().numpy()

    saliency = np.abs(gradients)

    return saliency


def compute_channel_occlusion(model, trial, checkpoint, device, target_class):
    
    original_result = predict_trial(model, trial, checkpoint, device)

    original_logit = original_result["logits"][target_class]

    effects = np.zeros(trial.shape[0])

    for channel_index in range(trial.shape[0]):
        
        occluded_trial = trial.copy()

        occluded_trial[channel_index] = 0.0

        occluded_result = predict_trial(model, occluded_trial, checkpoint, device)

        occluded_logit = occluded_result["logits"][target_class]

        effects[channel_index] = (original_logit - occluded_logit)

    return effects


def compute_temporal_occlusion(model,trial,checkpoint,device,target_class,window_size=40):

    original_result = predict_trial(model, trial, checkpoint, device)

    original_logit = original_result["logits"][target_class]

    effects = []
    times = []

    for start in range(0,trial.shape[1],window_size):
        
        end = min(start + window_size,trial.shape[1])

        occluded_trial = trial.copy()

        occluded_trial[:,start:end] = 0.0

        occluded_result = predict_trial(model, occluded_trial, checkpoint, device)

        occluded_logit = occluded_result["logits"][target_class]

        effect = (original_logit - occluded_logit)

        effects.append(effect)

        center_sample = (start + end) / 2

        center_time = (center_sample/ checkpoint["sampling_rate_hz"] + 1.0)

        times.append(center_time)

    return (np.array(effects), np.array(times))

