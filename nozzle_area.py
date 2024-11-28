"""
MIT License

Copyright (c) 2024 

Marco Panesi, 
Center for Hypersonics and Entry Systems Studies (CHESS), 
University of Illinois.

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

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
