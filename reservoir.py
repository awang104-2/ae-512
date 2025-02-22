"""
This file is licensed under the MIT License.
Copyright (c) 2024 Marco Panesi, Center for Hypersonics and Entry Systems Studies (CHESS), University of Illinois.

The original project provided a framework with blank functions.
This file has been significantly modified and fully implemented by awang104-2 since 11-20-2024.

The full license text is available in the LICENSE file in the project root.
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
