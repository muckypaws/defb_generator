"""
Helper functions for palette handling and JSON utilities.

This module provides reusable support routines such as:
- Loading JSON palette files
- Mapping logical INK values to RGB colour palettes
- Performing colour-related transformations used across systems
"""
import json
import os

def load_palette_json(path):
    """
    Load a CPC palette JSON file.

    Args:
        path (str): Path to JSON file

    Returns:
        dict: Colour palette {index: [R, G, B]}
    """
    if not os.path.exists(path):
        raise FileNotFoundError(f"Palette file not found: {path}")
    with open(path, "r") as f:
        return json.load(f)

def default_bw_palette():
    """
    Set black-and-white palette for Mode 2 (monochrome).

    Returns:
        dict: {"0": [0, 0, 0], "1": [255, 255, 255]}
    """
    return {
        "0": [0, 0, 0],
        "1": [255, 255, 255]
    }

def make_ink_palette(logical_to_ink, base_palette):
    """
    Remap logical colour indexes (0-3) to actual ink colours from CPC palette.

    Args:
        logical_to_ink (dict): Mapping of 0-3 to CPC ink values (0-26)
        base_palette (dict): Full CPC palette {index: [R,G,B]}

    Returns:
        dict: Palette with remapped ink RGBs
    """
    return {
        str(logical): base_palette.get(str(ink), [0, 0, 0])
        for logical, ink in logical_to_ink.items()
    }
