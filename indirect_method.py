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

This code simulates steady quasi-one-dimensional adiabatic flow through a converging-diverging nozzle,
assuming supercritical flow, thermodynamic equilibrium, and non-perfect gas behavior. It calculates
the nozzle flow properties such as velocity, Mach number, and thermodynamic state variables (enthalpy, 
density, pressure, etc.) based on area distribution and reservoir conditions.
"""

import numpy as np
from nozzle_area import find_closest_index


def process_nozzle_indirect_method(s0, h0, Area, A_x, A_star, F_rho_a_star, index_star, rbf_interpolator_rho,
                                   rbf_interpolator_speed, rbf_interpolator_pressure, rbf_interpolator_temperature):
    """
    Routine to compute the inlet velocity using the bisection method,
    and calculate thermodynamic properties along the nozzle.

    Args:
    - s0: Initial entropy value.
    - h0: Reservoir enthalpy value.
    - Area: DataFrame with area and position information.
    - A_x: List or array of area values along the nozzle.
    - A_star: Throat area (minimum area).
    - F_rho_a_star: Mass flow rate divided by A_star (rho_star * a_star).
    - index_star: Index of the throat in A_x.
    - rbf_interpolator_*: Interpolators for thermodynamic properties.

    Returns:
    - Lists of enthalpy, velocity, density, pressure, temperature, Mach number, and x positions.
    """
    # Initialize result lists
    enthalpy_values = []
    velocity_values = []
    density_values = []
    pressure_values = []
    temperature_values = []
    mach_values = []
    x_positions = []

    # Finding the inlet velocity
    # Defining parameters for the bisection method
    high = h0  # Right boundary of the search interval
    low = 0  # Left boundary of the search interval
    max_iterations = int(1e7)  # Maximum iterations for bisection search
    precision = 1e-5  # Tolerance for the difference between expected and approximated values

    # Bisection method search
    for i in range(max_iterations):
        # Parameters
        mid = (low + high) / 2  # Middle of the interval
        h = mid  # Guess for h is the middle of the interval
        log_key = np.log([s0, h]).reshape(1, -1)  # Setting the log input for interpolators
        u = np.sqrt(2 * (h0 - h))  # Inlet velocity (guess)
        rho = np.exp(rbf_interpolator_rho(log_key)[0])  # Inlet density (guess)
        A_guess = (F_rho_a_star / (rho * u)) * A_star  # Inlet area (guess)
        error = A_guess - A_x[0]  # Finding the difference between actual inlet area and guessed inlet area

        # Adjusting the search via the bisection method
        if error > precision:
            low = mid
        elif error < -precision:
            high = mid
        else:
            break

    # Approximated inlet enthalpy
    h_inlet = (low + high) / 2

    # Finding the thermodynamic properties of the rest of the nozzle
    h_values = np.linspace(h_inlet, h_inlet * 0.1, len(A_x))  #
    for h in h_values:
        # Converting to log inputs
        log_key = np.log([s0, h]).reshape(1, -1)

        # Finding thermodynamic properties
        u = np.sqrt(2 * (h0 - h))  # Velocity
        rho = np.exp(rbf_interpolator_rho(log_key)[0])  # Density
        a = np.exp(rbf_interpolator_speed(log_key)[0])  # Speed of sound
        p = np.exp(rbf_interpolator_pressure(log_key)[0])  # Pressure
        T = np.exp(rbf_interpolator_temperature(log_key)[0])  # Temperature
        M = u / a  # Mach number
        A = (F_rho_a_star / (rho * u)) * A_star  # Area
        n = find_closest_index(A_x, A)  # Index with closest indexed area
        x = Area['x'][n]  # Position along the nozzle

        enthalpy_values.append(h)
        velocity_values.append(u)
        density_values.append(rho)
        pressure_values.append(p)
        temperature_values.append(T)
        mach_values.append(M)
        x_positions.append(x)

    return enthalpy_values, velocity_values, density_values, pressure_values, temperature_values, mach_values, x_positions





