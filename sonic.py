import numpy as np

from scipy.optimize import fsolve
from thermo import *


def compute_hstar_sstar(s0, h0, rbf_interpolator_speed):
    # Define the function to solve for h_star
    def throat_condition(h_star):
        # Prepare log-transformed inputs for the interpolator
        log_inputs = np.log([s0, h_star[0]]).reshape(1, -1)  # Ensure 2D array

        # Use interpolator to find log(speed of sound), then exponentiate to get a
        log_a = rbf_interpolator_speed(log_inputs)  # Interpolator returns log(a)
        a = np.exp(log_a[0])  # Convert back to physical space

        # Compute velocity u from the energy equation
        u = (2 * (h0 - h_star)) ** 0.5

        # Return the difference for solving the throat condition u = a
        return u - a

    # Solve for h_star
    h_star = fsolve(throat_condition, h0 * 0.1)[0]
    s_star = s0  # Isentropic flow: s_star = s0
    return h_star, s_star


def compute_rho_star_astar_Fstar(s0, h_star, rbf_interpolator_rho, rbf_interpolator_speed):
    # Prepare log-transformed inputs
    log_inputs = np.log([s0, h_star])  # s0 and h_star are inputs

    # Interpolate in log space
    log_rho_star = rbf_interpolator_rho(log_inputs)  # Log of density
    log_a_star = rbf_interpolator_speed(log_inputs)  # Log of speed of sound

    # Convert back to physical space
    rho_star = np.exp(log_rho_star)
    a_star = np.exp(log_a_star)

    # Compute F = rho * a
    F_rho_star_a_star = rho_star * a_star

    return a_star, rho_star, F_rho_star_a_star

