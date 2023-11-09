import torch
from . import MNISTModel

def model_loader():
    checkpoint = torch.load('model.pth')
    model = MNISTModel.Model()
    model.load_state_dict(checkpoint['model'])
    return model, checkpoint['loss']
