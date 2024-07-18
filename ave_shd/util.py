# util.py
import numpy as np

def calculate_mean_coords(coords):
    """计算坐标列表的均值"""
    if coords and len(coords) > 0:
        return np.mean(coords, axis=0)
    return None
