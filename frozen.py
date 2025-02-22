"""
This file is licensed under the MIT License.
Copyright (c) 2024 Marco Panesi, Center for Hypersonics and Entry Systems Studies (CHESS), University of Illinois.

The original project provided a framework with blank functions.
This file has been significantly modified and fully implemented by awang104-2 since 11-20-2024.

The full license text is available in the LICENSE file in the project root.
"""
import numpy as np


def process_nozzle_perfect_gas(gamma, R, p0, T0, Area, A_x, A_star, index_star):

    """
    Routine to compute flow properties in a nozzle for a perfect gas using the area-Mach number relation.

    Args:
    - gamma: Specific heat ratio (Cp/Cv).
    - R: Gas constant (J/kg·K).
    - p0: Total (stagnation) pressure (Pa).
    - T0: Total (stagnation) temperature (K).
    - Area: DataFrame with area and position information.
    - A_x: List or array of area values along the nozzle.
    - A_star: Throat area (minimum area).
    - index_star: Index of the throat in A_x.

    Returns:
    - Lists of enthalpy, velocity, density, pressure, temperature, Mach number, and x positions.
    """

    # Initialize empty lists of the function's returns
    enthalpy_values = []
    velocity_values = []
    density_values = []
    pressure_values = []
    temperature_values = []
    mach_values = []
    x_positions = []

    for i, A_i in enumerate(A_x):
        # Finds the corresponding Mach number using Newton's method
        iterations = 50  # Number of Newton's method iterations
        M = 0  # Test Mach number
        if i < index_star:  # subsonic regime
            M = 0.5  # Initial guess
        else:
            M = 2  # Initial guess
        for k in range(iterations):
            exponent = ((gamma + 1) / (2 * (gamma - 1)))
            f = (1 / M) * (2 / (gamma + 1))**exponent * (1 + (gamma - 1) / 2 * M**2)**exponent - (A_i / A_star)
            Df = (2 * M**2 - 2) * (((gamma - 1) * M**2 + 2) / (gamma + 1))**exponent / ((gamma - 1) * M**4 + 2 * M**2)
            M = M - f / Df

        # Finding thermodynamic properties
        T = T0 * 1 / (1 + (gamma - 1) / 2 * M**2)
        p = p0 * (T / T0)**(gamma / (gamma - 1))
        rho = p / (R * T)
        a = np.sqrt(gamma * R * T)
        u = M * a
        h = gamma * R / (gamma - 1) * T
        x = Area['x'][i]

        # Adding thermodynamic properties to lists
        enthalpy_values.append(h)
        velocity_values.append(u)
        density_values.append(rho)
        pressure_values.append(p)
        temperature_values.append(T)
        mach_values.append(M)
        x_positions.append(x)

    return enthalpy_values, velocity_values, density_values, pressure_values, temperature_values, mach_values, x_positions
