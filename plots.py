import matplotlib.pyplot as plt
import numpy as np
import os


def plot_enthalpy(x, enthalpy):
    x, enthalpy = sort_list(x, enthalpy)
    plt.figure()
    plt.plot(x, enthalpy)
    plt.title('Position (m) vs. Enthalpy (J/kg)')
    plt.xlabel(r'Position $x$ along the nozzle (m)')
    plt.ylabel(r'Enthalpy $h$ (J/kg)')
    plt.legend(['LTE Indirect Method', 'Frozen Flow'])
    path = os.path.abspath('graphs/enthalpy_graph.png')
    plt.savefig(path)


def plot_area(x, area):
    x, area = sort_list(x, area)
    plt.figure()
    plt.plot(x, area)
    plt.title(r'Position (m) vs. Area ($m^2$)')
    plt.xlabel(r'Position $x$ along the nozzle (m)')
    plt.ylabel(r'Nozzle Area ($m^2$)')
    path = os.path.abspath('graphs/area_graph.png')
    plt.savefig(path)


def plot_velocity(x, velocity):
    x, velocity = sort_list(x, velocity)
    plt.figure()
    plt.plot(x, velocity)
    plt.title('Position (m) vs. Velocity (m/s)')
    plt.xlabel(r'Position $x$ along the nozzle (m)')
    plt.ylabel(r'Fluid Velocity $u$ (m/s)')
    plt.legend(['LTE Indirect Method', 'Frozen Flow'])
    path = os.path.abspath('graphs/velocity_graph.png')
    plt.savefig(path)


def plot_pressure(x, pressure):
    x, pressure = sort_list(x, pressure)
    plt.figure()
    plt.plot(x, pressure)
    plt.title('Position (m) vs. Pressure (Pa)')
    plt.xlabel(r'Position $x$ along the nozzle (m)')
    plt.ylabel('Fluid Pressure $p$ (Pa)')
    plt.legend(['LTE Indirect Method', 'Frozen Flow'])
    path = os.path.abspath('graphs/pressure_graph.png')
    plt.savefig(path)


def plot_temperature(x, temperature):
    x, pressure = sort_list(x, temperature)
    plt.figure()
    plt.plot(x, pressure)
    plt.title('Position (m) vs. Temperature (K)')
    plt.xlabel(r'Position $x$ along the nozzle (m)')
    plt.ylabel('Temperature $T$ (K)')
    plt.legend(['LTE Indirect Method', 'Frozen Flow'])
    path = os.path.abspath('graphs/temperature_graph.png')
    plt.savefig(path)


def plot_density(x, density):
    x, density = sort_list(x, density)
    plt.figure()
    plt.plot(x, density)
    plt.title(r'Position (m) vs. Pressure (kg/$m^3$)')
    plt.xlabel(r'Position $x$ along the nozzle (m)')
    plt.ylabel(r'Density $rho$ (kg/$m^3$)')
    plt.legend(['LTE Indirect Method', 'Frozen Flow'])
    path = os.path.abspath('graphs/density_graph.png')
    plt.savefig(path)


def plot_mach_number(x, mach_number):
    x, mach_number = sort_list(x, mach_number)
    plt.figure()
    plt.plot(x, mach_number)
    plt.title(r'Position (m) vs. Mach Number')
    plt.xlabel(r'Position $x$ along the nozzle (m)')
    plt.ylabel(r'Mach Number $M$')
    plt.legend(['LTE Indirect Method', 'Frozen Flow'])
    path = os.path.abspath('graphs/mach_graph.png')
    plt.savefig(path)


def sort_list(l1, l2, column=0):
    zipped = list(zip(l1, l2))
    zipped = np.array(sorted(zipped, key=lambda k: k[column])).T
    return zipped




