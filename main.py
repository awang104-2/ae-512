"""
This file is licensed under the MIT License.
Copyright (c) 2024 Marco Panesi, Center for Hypersonics and Entry Systems Studies (CHESS), University of Illinois.

The original project provided a framework with blank functions.
This file has been significantly modified and fully implemented by awang104-2 since 11-20-2024.

The full license text is available in the LICENSE file in the project root.
"""

import numpy as np
import os

import plots
import write_to_csv

# GIVEN
from nozzle_area import load_area_data, find_closest_index, find_astar
from thermo import load_thermodynamic_data, construct_rbf_interpolators

# IMPLEMENT
from reservoir import get_reservoir_h_and_s, create_reservoir_interpolator
from sonic import compute_hstar_sstar, compute_rho_star_astar_Fstar
from indirect_method import process_nozzle_indirect_method
from frozen import process_nozzle_perfect_gas
from plots import *

# Load thermodynamic data from a file (contains enthalpy, entropy, density, etc.)
output_data = 'data/output.dat'
file_path = os.path.abspath(output_data)
df, Enthalpy, Entropy, rho, speed_of_sound, Pressure, Temperature = load_thermodynamic_data(file_path)

# Load the area variation data: File containing the x and A(x) data
area_data = 'data/area.dat'
file_path = os.path.abspath(area_data)
Area = load_area_data(file_path)


# Create Radial Basis Function (RBF) interpolators for various thermodynamic properties
# These interpolators are used to estimate values like density and speed of sound at different states
rbf_interpolator_rho, rbf_interpolator_speed, rbf_interpolator_pressure, rbf_interpolator_temperature = construct_rbf_interpolators(Enthalpy, Entropy, rho, speed_of_sound, Pressure, Temperature)

# Compute reservoir conditions based on the provided pressure and temperature
# These conditions define the thermodynamic state at the reservoir (upstream of the nozzle)
enthalpy_interpolator, entropy_interpolator = create_reservoir_interpolator(df)

# Example reservoir conditions: given pressure p and temperature T, get h and s
p0 = 5000000
T0 = 4500
h0, s0 = get_reservoir_h_and_s(p0, T0, enthalpy_interpolator, entropy_interpolator)

# Find the nozzle throat location (x*) and the corresponding minimum area (A*)
x_star, A_star = find_astar(Area)
index_star = find_closest_index(Area['A'], A_star)

# Compute h* and s* at the throat using the speed of sound interpolator
h_star, s_star = compute_hstar_sstar(s0, h0, rbf_interpolator_speed)

# Compute a*, rho* and F(h0, s0)
sound_star, rho_star, F_rho_a_star = compute_rho_star_astar_Fstar(s_star, h_star,  rbf_interpolator_rho, rbf_interpolator_speed)

# Example 1D domain with known area variation A_x
A_x = Area['A']
result = process_nozzle_indirect_method(
    s0, h0, Area, A_x, A_star, F_rho_a_star, index_star,
    rbf_interpolator_rho, rbf_interpolator_speed, rbf_interpolator_pressure, rbf_interpolator_temperature
)
enthalpy_values, velocity_values, density_values, pressure_values, temperature_values, mach_values, x_positions = result

# Convert lists to arrays for further analysis or plotting
enthalpy_values = np.array(enthalpy_values)
velocity_values = np.array(velocity_values)
density_values = np.array(density_values)
mach_values = np.array(mach_values)
x_positions = np.array(x_positions)

# Output the results for verification
'''
print("Enthalpy values (J/kg):", enthalpy_values)
print("Velocity values (m/s):", velocity_values)
print("Density values (kg/m^3):", density_values)
print("Pressure (Pa):", pressure_values)
print("Temperature (K):", temperature_values)
print("Mach number values:", mach_values)
print("x positions (m):", x_positions)
'''

data = list(zip(x_positions, enthalpy_values, velocity_values, density_values, pressure_values, temperature_values, mach_values))
headers = ["x positions (m)", "Enthalpy values (J/kg)", "Velocity values (m/s)", "Density values (kg/m^3)", "Pressure (Pa)", "Temperature (K)", "Mach number values"]
filename = 'data/nozzle_thermo_properties.dat'

write_to_csv.write_to_csv(filename, data, headers)

R = 8.3144598 / 0.2672963120279829E-01
gamma = 0.1242430995249157E+01
result = process_nozzle_perfect_gas(gamma, R, p0, T0, Area, A_x, A_star, index_star)
enthalpy_values_fr, velocity_values_fr, density_values_fr, pressure_values_fr, temperature_values_fr, mach_values_fr, x_positions_fr = result


# Plotting position vs. enthalpy and area
plots.plot_enthalpy((x_positions, enthalpy_values), (x_positions_fr, enthalpy_values_fr))
plots.plot_area(Area['x'].values, A_x)

# Plotting u(x), p(x), T(x), rho(x), and M(x)
plots.plot_velocity((x_positions, velocity_values), (x_positions_fr, velocity_values_fr))
plots.plot_pressure((x_positions, pressure_values), (x_positions_fr, pressure_values_fr))
plots.plot_temperature((x_positions, temperature_values), (x_positions_fr, temperature_values_fr))
plots.plot_density((x_positions, density_values), (x_positions_fr, density_values_fr))
plots.plot_mach_number((x_positions, mach_values), (x_positions_fr, mach_values_fr))

print('Completed.')
