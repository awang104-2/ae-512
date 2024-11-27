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

import numpy as np
from scipy.interpolate import LinearNDInterpolator


# Creates interpolators for thermodynamic properties for the reservoir
def create_reservoir_interpolator(df):
    temperature = df['T'].values
    pressure = df['p'].values
    enthalpy = df['Enthalpy'].values  # per unit mass
    entropy = df['Entropy'].values  # per unit mass

    points = np.column_stack((temperature, pressure))  # Combines T and P into an array of 2D coordinates

    enthalpy_interpolator = LinearNDInterpolator(points, enthalpy)  # Linear interpolation of enthalpy
    entropy_interpolator = LinearNDInterpolator(points, entropy)  # Linear interpolation of entropy

    return enthalpy_interpolator, entropy_interpolator


# Computes enthalpy and entropy from pressure and temperature
def get_reservoir_h_and_s(p, T, enthalpy_interpolator, entropy_interpolator):
    # Finding enthalpy and entropy using linear interpolation based on the thermodynamic state specified by p and T
    h = enthalpy_interpolator(T, p)
    s = entropy_interpolator(T, p)

    return h, s  # Returns enthalpy and entropy, per unit mass
