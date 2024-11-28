import matplotlib.pyplot as plt
import os


def plot_enthalpy(LTE, frozen):
    x_lte, enthalpy_lte = LTE
    x_fr, enthalpy_fr = frozen
    plt.figure()
    plt.plot(x_lte, enthalpy_lte)
    plt.plot(x_fr, enthalpy_fr, linestyle='--', linewidth=2)
    plt.title('Position (m) vs. Enthalpy (J/kg)')
    plt.xlabel(r'Position $x$ along the nozzle (m)')
    plt.ylabel(r'Enthalpy $h$ (J/kg)')
    plt.legend(['LTE Indirect Method', 'Frozen Flow'])
    path = os.path.abspath('graphs/enthalpy_graph.png')
    plt.savefig(path)


def plot_area(x, area):
    plt.figure()
    plt.plot(x, area)
    plt.title(r'Position (m) vs. Area ($m^2$)')
    plt.xlabel(r'Position $x$ along the nozzle (m)')
    plt.ylabel(r'Nozzle Area ($m^2$)')
    path = os.path.abspath('graphs/area_graph.png')
    plt.savefig(path)


def plot_velocity(LTE, frozen):
    x_lte, velocity_lte = LTE
    x_fr, velocity_fr = frozen
    plt.figure()
    plt.plot(x_lte, velocity_lte)
    plt.plot(x_fr, velocity_fr, linestyle='--', linewidth=2)
    plt.title('Position (m) vs. Velocity (m/s)')
    plt.xlabel(r'Position $x$ along the nozzle (m)')
    plt.ylabel(r'Fluid Velocity $u$ (m/s)')
    plt.legend(['LTE Indirect Method', 'Frozen Flow'])
    path = os.path.abspath('graphs/velocity_graph.png')
    plt.savefig(path)


def plot_pressure(LTE, frozen):
    x_lte, pressure_lte = LTE
    x_fr, pressure_fr = frozen
    plt.figure()
    plt.plot(x_lte, pressure_lte)
    plt.plot(x_fr, pressure_fr, linestyle='--', linewidth=2)
    plt.title('Position (m) vs. Pressure (Pa)')
    plt.xlabel(r'Position $x$ along the nozzle (m)')
    plt.ylabel('Fluid Pressure $p$ (Pa)')
    plt.legend(['LTE Indirect Method', 'Frozen Flow'])
    path = os.path.abspath('graphs/pressure_graph.png')
    plt.savefig(path)


def plot_temperature(LTE, frozen):
    x_lte, temperature_lte = LTE
    x_fr, temperature_fr = frozen
    plt.figure()
    plt.plot(x_lte, temperature_lte)
    plt.plot(x_fr, temperature_fr, linestyle='--', linewidth=2)
    plt.title('Position (m) vs. Temperature (K)')
    plt.xlabel(r'Position $x$ along the nozzle (m)')
    plt.ylabel('Temperature $T$ (K)')
    plt.legend(['LTE Indirect Method', 'Frozen Flow'])
    path = os.path.abspath('graphs/temperature_graph.png')
    plt.savefig(path)


def plot_density(LTE, frozen):
    x_lte, density_lte = LTE
    x_fr, density_fr = frozen
    plt.figure()
    plt.plot(x_lte, density_lte)
    plt.plot(x_fr, density_fr, linestyle='--', linewidth=2)
    plt.title(r'Position (m) vs. Pressure (kg/$m^3$)')
    plt.xlabel(r'Position $x$ along the nozzle (m)')
    plt.ylabel(r'Density $rho$ (kg/$m^3$)')
    plt.legend(['LTE Indirect Method', 'Frozen Flow'])
    path = os.path.abspath('graphs/density_graph.png')
    plt.savefig(path)


def plot_mach_number(LTE, frozen):
    x_lte, mach_lte = LTE
    x_fr, mach_fr = frozen
    plt.figure()
    plt.plot(x_lte, mach_lte)
    plt.plot(x_fr, mach_fr, linestyle='--', linewidth=2)
    plt.title(r'Position (m) vs. Mach Number')
    plt.xlabel(r'Position $x$ along the nozzle (m)')
    plt.ylabel(r'Mach Number $M$')
    plt.legend(['LTE Indirect Method', 'Frozen Flow'])
    path = os.path.abspath('graphs/mach_graph.png')
    plt.savefig(path)




