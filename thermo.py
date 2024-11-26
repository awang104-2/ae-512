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



