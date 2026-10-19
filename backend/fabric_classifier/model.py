import torch
import torch.nn as nn
import torchvision.models as models

def get_model(num_classes=14, pretrained=True):
    """
    Initializes an EfficientNet-B0 model with a custom classifier head.
    """
    weights = models.EfficientNet_B0_Weights.IMAGENET1K_V1 if pretrained else None
    model = models.efficientnet_b0(weights=weights)

    # Replace the classifier head
    model.classifier = nn.Sequential(
        nn.Dropout(p=0.3),
        nn.Linear(1280, 256),
        nn.ReLU(),
        nn.Dropout(p=0.2),
        nn.Linear(256, num_classes)
    )
    
    return model
