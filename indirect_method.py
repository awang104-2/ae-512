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

from .nozzle_area import find_closest_index


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
    return enthalpy_values, velocity_values, density_values, pressure_values, temperature_values, mach_values, x_positions
