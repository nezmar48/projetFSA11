import math
import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import minimize

step = 0.001
end = 3.0

def simulation(a, v0, x0):
    x = np.arange(0, end, step)
    x[0] = x0
    v = v0
    for i in range(len(x)-1):
        v += a(v)*step
        x[i+1] = x[i] + v * step
        if i > 1 and x[i] <= 0:
            x[i+1] = 0
    return x

g = 9.81
x_0 = 0
y_0 = 0
v_x_0 = 10
v_y_0 = 10
m = 0.5
k = 0.1 #linear drag
c = 0.05 #quadrartic drag

def sims():
    plt.figure(1)

# symultations
    plt.subplot(3,1,1)
    plt.plot(
        simulation(lambda v: 0, v_x_0, x_0),
        simulation(lambda v: -g, v_y_0, y_0),
        label="simulation sans frottement")
    plt.plot(
        simulation(lambda v: -k/m*v, v_x_0, x_0),
        simulation(lambda v: -g-k/m*v, v_y_0, y_0),
        label="simulation forttement v")
    plt.plot(
        simulation(lambda v: -c/m*abs(v)*v, v_x_0, x_0),
        simulation(lambda v: -g - c/m*abs(v)*v, v_y_0, y_0),
        label="simulation frottement v^2")

# analytique 
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

# figure for x vs t
    plt.subplot(3,1,2)
    plt.plot(
        t,
        simulation(lambda v: 0, v_x_0, x_0),
        label="simulation sans frottement")
    plt.plot(
        t,
        simulation(lambda v: -k/m*v, v_x_0, x_0), 
        label="simulation frottement v")
    plt.plot(
        t,
        simulation(lambda v: -c/m*abs(v)*v, v_x_0, x_0),
        label="simulation frottement v^2")

# figure for y vs t
    plt.plot(
        t,
        simulation(lambda v: -g, v_y_0, y_0),
        label="simulation sans frottement")
    plt.plot(
        t,
        simulation(lambda v: -g - k/m*v, v_y_0, y_0),
        label="simulation frottement v")
    plt.plot(
        t,
        simulation(lambda v: -g - c/m*abs(v)*v, v_y_0, y_0),
        label="simulation frottement v^2")
    plt.xlabel("t [s]")
    plt.ylabel("dist [m]")
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


x_mesured = 10

plt.figure(1)
plt.plot(
        simulation(lambda v: -k/m*v, v_x_0, x_0),
        simulation(lambda v: -g-k/m*v, v_y_0, y_0),
        label="simulation forttement v")

k = minimize(lambda c: abs(simulation(lambda v: -c/m*v, v_x_0, x_0)[simulation(lambda v: -g-c/m*v, v_y_0, y_0) != 0][-1] - x_mesured), x0=[k]).x
print(k)
plt.plot(
        simulation(lambda v: -k/m*v, v_x_0, x_0),
        simulation(lambda v: -g-k/m*v, v_y_0, y_0),
        label="simulation forttement v")
plt.xlabel("x [m]")
plt.ylabel("y [m]")
plt.legend()

plt.show()

# sims()
