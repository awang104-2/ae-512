import numpy as np

from scipy.optimize import fsolve
from thermo import *


def compute_hstar_sstar(s0, h0, rbf_interpolator_speed):
    p2 = p1 + rho1 * pow(u1, 2) * (1 - rho1 / rho2)
    h2 = h1 + pow(u1, 2) / 2 * (1 - pow((rho1 / rho2), 2))

    return h_star, s_star


def compute_rho_star_astar_Fstar(s0, h_star, rbf_interpolator_rho, rbf_interpolator_speed):

    return a_star, rho_star, F_rho_star_a_star

