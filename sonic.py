import numpy as np

from scipy.optimize import fsolve
from thermo import *


# Computes enthalpy h_star and entropy s_star at the throat
def compute_hstar_sstar(s0, h0, rbf_interpolator_speed):
    # Defines the equation/function representing the constraints at the throat of the nozzle
    def throat_condition(h_star):
        # Converting to natural log entropy-enthalpy inputs
        log_inputs = np.log([s0, h_star[0]]).reshape(1, -1)  # 2D array

        # Finding the speed of sound associated with the enthalpy and entropy
        log_a = rbf_interpolator_speed(log_inputs)  # Interpolator returns log(a)
        a = np.exp(log_a[0])  # Convert back to physical values

        # Computing the velocity according to the energy condition
        u = (2 * (h0 - h_star[0])) ** 0.5

        # Returns the difference between speed of sound and velocity of the fluid
        # The difference is 0 if it satisfies the throat condition (and is at the throat of the nozzle)
        return u - a

    # Solving for the enthalpy and entropy at the throat
    guess = np.array([h0 * 0.05])  # Initial guess for h_star
    h_star = fsolve(throat_condition, guess)[0]  # Solving the throat condition to find the enthalpy at the throat
    s_star = s0  # Isentropic flow condition
    return h_star, s_star


# Computes a_star, rho_star, and F_star = a_star * rho_star at the throat
def compute_rho_star_astar_Fstar(s0, h_star, rbf_interpolator_rho, rbf_interpolator_speed):
    # Converting to natural log entropy-enthalpy inputs
    log_inputs = np.log([s0, h_star]).reshape(1, -1)  # 2D array

    # Using interpolation to find the density and speed of sound at the nozzle throat
    log_rho_star = rbf_interpolator_rho(log_inputs)  # Log of density
    log_a_star = rbf_interpolator_speed(log_inputs)  # Log of speed of sound

    # Converting back to physical values
    rho_star = np.exp(log_rho_star)
    a_star = np.exp(log_a_star)

    # Computing F_star
    F_rho_star_a_star = rho_star * a_star

    return a_star, rho_star, F_rho_star_a_star

