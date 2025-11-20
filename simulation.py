import math
import matplotlib.pyplot as plt
import numpy as np

end = 3
step = 0.001

class SimC:
    def __init__(self, x_0 = 0, v_0=10, a = lambda v: 0):
        self.x = np.zeros(int(end/step))
        self.x[0] = x_0
        self.v_0 = v_0
        self.a = a

    def simulate(self):
        v = self.v_0
        for i in range(len(self.x)-1):
            v += self.a(v) * step
            self.x[i+1] = self.x[i] + v * step

def simulation_xy(sim_x=None, sim_y=None):
    if sim_x is None:
        sim_x = SimC()
    if sim_y is None:
        sim_y = SimC()

    sim_x.simulate()
    sim_y.simulate()

    index = len(sim_y.x)
    for i in range(1, len(sim_y.x)):
        if sim_y.x[i] < 0 and  (sim_y.x[i-1] - sim_y.x[i]) > 0:
            index = i
            break

    return (sim_x.x[:index], sim_y.x[:index])

def sims():
    m = 0.1
    k = 0.1
    c = 0.01
    g = 9.81
    plt.figure(1)

# simultations
    sim_no_drag = simulation_xy(
        SimC(a=lambda v: 0),
        SimC(a=lambda v: -g )
    )
    sim_linear_drag = simulation_xy(
        SimC(a=lambda v: -k/m*v),
        SimC(a=lambda v: -g -k/m*v)
    )
    sim_quadratic_drag = simulation_xy(
        SimC(a=lambda v: -c/m*abs(v)*v),
        SimC(a=lambda v: -g -c/m*abs(v)*v)
    )

    plt.subplot(3,1,1)
    plt.plot(sim_no_drag[0], sim_no_drag[1], label="simulation sans frottement")
    plt.plot(sim_linear_drag[0], sim_linear_drag[1], label="simulation forttement v")
    plt.plot(sim_quadratic_drag[0], sim_quadratic_drag[1], label="simulation frottement v^2")

# analytique 
    x_0 = 0
    y_0 = 0
    v_x_0 = 10
    v_y_0 = 10
    t = np.arange(0, end, step)

    plt.plot(
        x_0 + v_x_0 * t,
        np.maximum(y_0 + v_y_0 * t - 0.5 * g * t**2,0),
        "--", label="analitique sans frottement")
    plt.plot(
        x_0 + (m*v_x_0/k) * (1 - np.exp(-k/m * t)),
        np.maximum(y_0 + (m/k)*(v_y_0 + m*g/k)*(1 - np.exp(-k/m * t)) - (m*g/k)*t, 0),
        "--", label="analitique frottement v")

    plt.xlabel("x [m]")
    plt.ylabel("y [m]")
    plt.legend()

# energie
    x_0_l = 1 # initial lenght of air column
    x_max_l = 10
    x = np.arange(x_0_l, x_max_l, step)
    a_l = 1 # area of air column
    p_0_l = 100 # initial presure
    p = 10 # air pressure
    gamma = 1.4 # adiabatic constant

    plt.subplot(3,1,3)
    e_k = (p_0_l * a_l*(x_0_l**gamma) /(1 - gamma))  * (x**(1 -gamma) - x_0_l ** (1 - gamma))
    e_p = p_0_l*a_l*(x_0_l**gamma)/ (gamma - 1)* (x**(1 - gamma))
    plt.plot(x, e_k, label="energie kinetique")
    plt.plot(x, e_p, label="energie potentielle")
    plt.plot(x, e_p + e_k, label="energie totale")
    plt.xlabel("x [m]")
    plt.ylabel("E[J]")
    plt.legend()
    plt.show()
