"""
This file is licensed under the MIT License.
Copyright (c) 2024 Marco Panesi, Center for Hypersonics and Entry Systems Studies (CHESS), University of Illinois.

The original project provided a framework with blank functions.
This file has been significantly modified and fully implemented by awang104-2 since 11-20-2024.

The full license text is available in the LICENSE file in the project root.
"""

import pandas as pd
import numpy as np


def load_area_data(file_path):
    # Load the area variation data from file
    area = pd.read_csv(file_path, sep='\\s+', header=None, names=['x', 'A'])
    return area


def find_astar(df):
    # Find the location and value of A*
    idx_min = df['A'].idxmin()
    x_star = df['x'].iloc[idx_min]
    A_star = df['A'].iloc[idx_min]
    return x_star, A_star


def find_closest_index(array, value):
    """
    Find the index of the entry in 'array' that is closest to the 'value'.
    
    Args:
    - array: numpy array or list of real numbers.
    - value: scalar, the target value to find the closest match for.
    
    Returns:
    - index: integer, the index of the closest entry in the array.
    """
    array = np.asarray(array)  # Ensure input is converted to a numpy array
    index = np.argmin(np.abs(array - value))  # Find the index of the smallest difference
    return index
