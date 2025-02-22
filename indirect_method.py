"""
This file is licensed under the MIT License.
Copyright (c) 2024 Marco Panesi, Center for Hypersonics and Entry Systems Studies (CHESS), University of Illinois.

The original project provided a framework with blank functions.
This file has been significantly modified and fully implemented by awang104-2 since 11-20-2024.

The full license text is available in the LICENSE file in the project root.
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
    # Initialize lists
    enthalpy_values = []
    velocity_values = []
    density_values = []
    pressure_values = []
    temperature_values = []
    mach_values = []
    x_positions = []

    h_inlet = h0 * 0.99  # "Inlet enthalpy" for graphical reasons
    h_values = np.linspace(h_inlet, 0.5 * h0, 500)  # Test enthalpy values

    # For each enthalpy value, finds the closest x value using the indirect LTE approach
    for h in h_values:
        if h <= h_inlet:  # Ignore enthalpies greater than inlet
            # Converted to log input for interpolator
            log_input = np.log([s0, h]).reshape(1, -1)

            # Finding thermodynamic properties
            rho = np.exp(rbf_interpolator_rho(log_input))[0]
            speed_of_sound = np.exp(rbf_interpolator_speed(log_input))[0]
            pressure = np.exp(rbf_interpolator_pressure(log_input))[0]
            temperature = np.exp(rbf_interpolator_temperature(log_input))[0]
            velocity = np.sqrt(2 * (h0 - h))
            mach = velocity / speed_of_sound
            area = (F_rho_a_star / (rho * velocity) * A_star)[0]

            # Checks regime
            if mach < 1:
                index = find_closest_index(A_x[:index_star], area)
            else:
                index = index_star + find_closest_index(A_x[index_star:], area)
            x = Area['x'][index]

            # Append the computed properties
            enthalpy_values.append(h)
            velocity_values.append(velocity)
            density_values.append(rho)
            pressure_values.append(pressure)
            temperature_values.append(temperature)
            mach_values.append(mach)
            x_positions.append(x)

    return enthalpy_values, velocity_values, density_values, pressure_values, temperature_values, mach_values, x_positions



