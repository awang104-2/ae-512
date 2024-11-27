import numpy as np
from scipy.interpolate import LinearNDInterpolator
import matplotlib.pyplot as plt
import os
import thermo, sonic, reservoir


def path_tester():
    file_path = "data/output.dat"

    # Get the absolute path of the file
    absolute_path = os.path.abspath(file_path)
    print("Absolute path:", absolute_path)

    # Get the directory containing the file
    directory = os.path.dirname(file_path)
    print("Directory:", directory)

    return absolute_path


def interpolator_tester():
    # Generate some random data points
    rng = np.random.default_rng()
    x = rng.random(10) - 0.5
    y = rng.random(10) - 0.5
    z = np.hypot(x, y)

    # Create the interpolator
    interp = LinearNDInterpolator(list(zip(x, y)), z)

    # Generate a grid of points for interpolation
    X = np.linspace(min(x), max(x))
    Y = np.linspace(min(y), max(y))
    X, Y = np.meshgrid(X, Y)

    # Interpolate values at the grid points
    Z = interp(X, Y)

    # Plot the results
    plt.pcolormesh(X, Y, Z, shading='auto')
    plt.plot(x, y, "ok", label="input point")
    plt.legend()
    plt.colorbar()
    plt.axis("equal")
    plt.show()


def thermo_tester():
    file_path = path_tester()
    df, Enthalpy, Entropy, rho, speed_of_sound, Pressure, Temperature = thermo.load_thermodynamic_data(file_path)
    rbf_interpolator_rho, rbf_interpolator_speed, rbf_interpolator_pressure, rbf_interpolator_temperature = thermo.construct_rbf_interpolators(Enthalpy, Entropy, rho, speed_of_sound, Pressure, Temperature)
    h = np.log(0.3019409035292074e7)
    s = np.log(0.9337903799336349e4)
    rho = np.exp(rbf_interpolator_rho([[s, h]])[0])
    print('Density', rho)
    print('Expected Density', 0.1383229745292957)
    print('Fractional Error', np.abs(rho - 0.1383229745292957) / 0.1383229745292957)
    return df, rbf_interpolator_rho, rbf_interpolator_speed, rbf_interpolator_pressure, rbf_interpolator_temperature


def sonic_tester():
    p0 = 5000000
    T0 = 4500
    df, rbf_interpolator_rho, rbf_interpolator_speed, rbf_interpolator_pressure, rbf_interpolator_temperature = thermo_tester()
    enthalpy_interpolator, entropy_interpolator = reservoir.create_reservoir_interpolator(df)
    h0, s0 = reservoir.get_reservoir_h_and_s(p0, T0, enthalpy_interpolator, entropy_interpolator)
    rho_ratio = sonic.__iterate_rho(h0, s0, rbf_interpolator_rho, rbf_interpolator_speed)
    print('Final Result', rho_ratio)


if __name__ == '__main__':
    a = [1, 2, 3, 4, 5]
    b = [21, 22, 23, 24, 25]
    c = zip(a, b)
    print(list(c))
