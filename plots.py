import matplotlib.pyplot as plt
import numpy as np
import os


def plot_LTE_enthalpy(x, enthalpy):
    zipped = list(zip(x, enthalpy))
    zipped = np.array(sorted(zipped, key=lambda k: k[0])).T
    x = zipped[0]
    enthalpy = zipped[1]

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

