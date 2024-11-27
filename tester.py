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


def zip_tester():
    a = [1, 2, 3, 4, 5]
    b = [21, 22, 23, 24, 25]
    c = zip(a, b)
    print(list(c))


def main_tester():
    import os
    import write_to_csv

    # GIVEN
    from nozzle_area import load_area_data, find_closest_index, find_astar
    from thermo import load_thermodynamic_data, construct_rbf_interpolators

    # IMPLEMENT
    from reservoir import get_reservoir_h_and_s, create_reservoir_interpolator
    from sonic import compute_hstar_sstar, compute_rho_star_astar_Fstar
    from indirect_method import process_nozzle_indirect_method
    from frozen import process_nozzle_perfect_gas

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
    rbf_interpolator_rho, rbf_interpolator_speed, rbf_interpolator_pressure, rbf_interpolator_temperature = construct_rbf_interpolators(
        Enthalpy, Entropy, rho, speed_of_sound, Pressure, Temperature)

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
    sound_star, rho_star, F_rho_a_star = compute_rho_star_astar_Fstar(s_star, h_star, rbf_interpolator_rho,
                                                                      rbf_interpolator_speed)

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

    def bisection_search(index):
        # Finding the inlet velocity
        # Defining parameters for the bisection method
        high = h0  # Right boundary of the search interval
        low = 0  # Left boundary of the search interval
        max_iterations = int(1e7)  # Maximum iterations for bisection search
        precision = 1e-6  # Tolerance for the difference between expected and approximated values

        # Bisection method search
        for i in range(max_iterations):
            # Parameters
            mid = (low + high) / 2  # Middle of the interval
            h = mid  # Guess for h is the middle of the interval
            log_key = np.log([s0, h]).reshape(1, -1)  # Setting the log input for interpolators
            u = np.sqrt(2 * (h0 - h))  # Inlet velocity (guess)
            rho = np.exp(rbf_interpolator_rho(log_key)[0])  # Inlet density (guess)
            A_guess = (F_rho_a_star / (rho * u)) * A_star  # Inlet area (guess)
            error = A_guess - A_x[index]  # Finding the difference between actual inlet area and guessed inlet area

            # Adjusting the search via the bisection method
            if error > precision:
                low = mid
            elif error < -precision:
                high = mid
            else:
                break
        h_inlet = (low + high) / 2
        print(Area['x'][index], h_inlet)

    bisection_search(0)
    bisection_search(1)
    bisection_search(2)
    bisection_search(3)


if __name__ == '__main__':
    main_tester()