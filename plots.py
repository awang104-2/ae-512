import matplotlib.pyplot as plt
import numpy as np
import os


def plot_LTE_enthalpy(x, enthalpy):
    plt.figure()
    plt.plot(x, enthalpy)
    plt.title('Position (m) vs. Enthalpy (J/kg)')
    plt.xlabel('Position (m)')
    plt.ylabel('Enthalpy (J/kg)')
    path = os.path.abspath('graphs/enthalpy_graph.png')
    plt.savefig(path)


def plot_LTE_area(x, area):
    zipped = list(zip(x, area))
    zipped = np.array(sorted(zipped, key=lambda k: k[0])).T
    x = zipped[0]
    area = zipped[1]

    plt.figure()
    plt.plot(x, area)
    path = os.path.abspath('graphs/area_graph.png')
    plt.savefig(path)


def plot_LTE_density(x, density):
    zipped = list(zip(x, density))
    zipped = np.array(sorted(zipped, key=lambda k: k[0])).T
    x = zipped[0]
    density = zipped[1]

    plt.figure()
    plt.plot(x, density)
    path = os.path.abspath('graphs/density_graph.png')
    plt.savefig(path)


def plot_LTE_velocity(x, velocity):
    zipped = list(zip(x, velocity))
    zipped = np.array(sorted(zipped, key=lambda k: k[0])).T
    x = zipped[0]
    velocity = zipped[1]

    plt.figure()
    plt.plot(x, velocity)
    path = os.path.abspath('graphs/velocity_graph.png')
    plt.savefig(path)


