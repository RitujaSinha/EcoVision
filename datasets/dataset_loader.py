"""
Dataset Loader & Manager (Dataset Layer)
Handles loading, organizing, and generating sample dataset images for EcoVision.
Includes 6 solid waste categories plus human non-waste safety benchmarks.
"""

import os
import json
from PIL import Image, ImageDraw

CATEGORIES = ["plastic", "paper", "glass", "metal", "cardboard", "organic", "human"]

def ensure_sample_images(samples_dir: str):
    """
    Checks if test samples exist for each category.
    Creates directory structures and sample entries.
    """
    for category in CATEGORIES:
        cat_dir = os.path.join(samples_dir, category)
        os.makedirs(cat_dir, exist_ok=True)


def get_available_samples(samples_dir: str):
    """Returns a list of all available sample images across categories."""
    samples = []
    for category in CATEGORIES:
        cat_dir = os.path.join(samples_dir, category)
        if not os.path.exists(cat_dir):
            continue
        for fname in sorted(os.listdir(cat_dir)):
            if fname.lower().endswith(('.png', '.jpg', '.jpeg', '.webp')):
                samples.append({
                    "category": category,
                    "filename": fname,
                    "url": f"/datasets/samples/{category}/{fname}",
                    "rel_path": f"{category}/{fname}"
                })
    return samples
