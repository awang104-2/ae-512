"""
This file is licensed under the MIT License.
Copyright (c) 2024 Marco Panesi, Center for Hypersonics and Entry Systems Studies (CHESS), University of Illinois.

The original project provided a framework with blank functions.
This file has been significantly modified and fully implemented by awang104-2 since 11-20-2024.

The full license text is available in the LICENSE file in the project root.
"""

import pandas as pd
import numpy as np
from scipy.interpolate import RBFInterpolator


def load_thermodynamic_data(filename):
    """
    Load thermodynamic data from the specified file.
    """
    # Load the data from the file
    df = pd.read_csv(filename, sep=r'\s+', comment='#', header=None,
                     names=['T', 'p', 'rho', 'MolarMass', 'Enthalpy', 'Entropy', 'SpeedOfSound'])  # Column names
    
    # Access variables from the dataset
    Enthalpy = df['Enthalpy'].values
    Entropy = df['Entropy'].values
    rho = df['rho'].values
    speed_of_sound = df['SpeedOfSound'].values  
    Temperature = df['T'].values
    Pressure = df['p'].values
    
    return df, Enthalpy, Entropy, rho, speed_of_sound, Pressure, Temperature


def construct_rbf_interpolators(Enthalpy, Entropy, rho, speed_of_sound, Pressure, Temperature):
    """
    Constructs RBF interpolators for density and speed of sound based on Enthalpy and Entropy.
    """
    # Prepare the data for RBF interpolation of density
    x = np.log(np.vstack((Entropy, Enthalpy))).T  # Input data: log of Entropy and Enthalpy

    y_rho = np.log(rho)  # Log of density
    rbf_interpolator_rho = RBFInterpolator(x, y_rho, kernel='quintic')

    # Prepare the data for RBF interpolation of speed of sound
    y_speed_of_sound = np.log(speed_of_sound)  # Log of speed of sound
    rbf_interpolator_speed = RBFInterpolator(x, y_speed_of_sound, kernel='quintic')

    # Prepare the data for RBF interpolation of temperature
    y_temperature = np.log(Temperature)
    rbf_interpolator_temperature = RBFInterpolator(x, y_temperature, kernel='quintic')

    # Prepare the data for RBF interpolation of pressure
    y_pressure = np.log(Pressure)
    rbf_interpolator_pressure = RBFInterpolator(x, y_pressure, kernel='quintic')

    return rbf_interpolator_rho, rbf_interpolator_speed, rbf_interpolator_pressure, rbf_interpolator_temperature



