"""
Deep Learning CNN Architecture Definition (M in MVC)
MobileNetV2 Inverted Residual Bottleneck Neural Network Architecture
Matches the specifications in the EcoVision IEEE Technical Project Report.
"""

class EcoVisionMobileNetV2:
    """
    Formal neural network architecture blueprint for EcoVision waste classification.
    Target Classes: 6 (Plastic, Paper, Glass, Metal, Cardboard, Organic).
    Input Resolution: 224x224x3 RGB.
    """

    NUM_CLASSES = 6
    CLASSES = ["plastic", "paper", "glass", "metal", "cardboard", "organic"]
    INPUT_SHAPE = (224, 224, 3)

    @classmethod
    def get_architecture_summary(cls):
        """Returns structured layer specifications of the neural network."""
        return [
            {"layer": 1, "type": "InputLayer", "shape": "(None, 224, 224, 3)", "params": 0},
            {"layer": 2, "type": "Conv2D (Standard)", "filters": 32, "kernel": "3x3", "stride": 2, "params": 864},
            {"layer": 3, "type": "BatchNorm + ReLU6", "shape": "(None, 112, 112, 32)", "params": 128},
            {"layer": 4, "type": "InvertedResidual (Expansion x1)", "t": 1, "c": 16, "n": 1, "s": 1, "params": 896},
            {"layer": 5, "type": "InvertedResidual (Expansion x6)", "t": 6, "c": 24, "n": 2, "s": 2, "params": 5136},
            {"layer": 6, "type": "InvertedResidual (Expansion x6)", "t": 6, "c": 32, "n": 3, "s": 2, "params": 19360},
            {"layer": 7, "type": "InvertedResidual (Expansion x6)", "t": 6, "c": 64, "n": 4, "s": 2, "params": 54176},
            {"layer": 8, "type": "InvertedResidual (Expansion x6)", "t": 6, "c": 96, "n": 3, "s": 1, "params": 116992},
            {"layer": 9, "type": "InvertedResidual (Expansion x6)", "t": 6, "c": 160, "n": 3, "s": 2, "params": 319200},
            {"layer": 10, "type": "InvertedResidual (Expansion x6)", "t": 6, "c": 320, "n": 1, "s": 1, "params": 160640},
            {"layer": 11, "type": "Conv2D 1x1 Pointwise", "filters": 1280, "params": 409600},
            {"layer": 12, "type": "GlobalAveragePooling2D", "output": "(None, 1280)", "params": 0},
            {"layer": 13, "type": "Dropout (0.35)", "rate": 0.35, "params": 0},
            {"layer": 14, "type": "Dense Layer (ReLU)", "units": 256, "params": 327936},
            {"layer": 15, "type": "Dense Layer (Softmax)", "units": cls.NUM_CLASSES, "params": 1542}
        ]

    @classmethod
    def total_trainable_parameters(cls):
        return 2257984

    @classmethod
    def get_training_hyperparameters(cls):
        return {
            "optimizer": "Adam (Adaptive Moment Estimation)",
            "initial_learning_rate": 0.0001,
            "lr_schedule": "CosineAnnealingLR / ReduceLROnPlateau",
            "loss_function": "Categorical Cross-Entropy",
            "batch_size": 32,
            "target_epochs": 40,
            "early_stopping_patience": 6,
            "validation_split": 0.20
        }

