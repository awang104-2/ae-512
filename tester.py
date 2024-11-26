import numpy as np
from scipy.interpolate import LinearNDInterpolator
import matplotlib.pyplot as plt
import os


def path_tester():
    file_path = "data/output.dat"

    # Get the absolute path of the file
    absolute_path = os.path.abspath(file_path)
    print("Absolute path:", absolute_path)

    # Get the directory containing the file
    directory = os.path.dirname(file_path)
    print("Directory:", directory)


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


if __name__ == '__main__':
    path_tester()