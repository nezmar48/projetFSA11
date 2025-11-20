import math
import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import brentq

g = 9.81
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

m = 0.1
x_mesured = 5
a_x = lambda v, c: -c/m*abs(v)*v
a_y = lambda v, c:-g-c/m*abs(v)*v

def find_c(c):
    xy = simulation_xy(SimC(a= lambda v : a_x(v,c)), SimC(a=lambda v : a_y(v,c)))
    return xy[0][-1] - x_mesured

x_wanted = 7
def find_v0(v0):
    xy = simulation_xy(SimC(a=lambda v : a_x(v,c_opt), v_0 = v0), SimC(a=lambda v : a_y(v,c_opt), v_0 = v0))
    return (xy[0][-1] - x_wanted)

c = 0.01
xy = simulation_xy(SimC(a=lambda v : a_x(v,c)), SimC(a=lambda v : a_y(v,c)))

c_opt = brentq(find_c, 0, 10)
xy_opt = simulation_xy(SimC(a=lambda v : a_x(v,c_opt)), SimC(a=lambda v : a_y(v,c_opt)))

v0_wanted = brentq(find_v0, 0, 50)
xy_v0 = simulation_xy(SimC(a= lambda v : a_x(v,c_opt), v_0 = v0_wanted), SimC(a=lambda v : a_y(v,c_opt), v_0 = v0_wanted))

plt.figure()
plt.plot(xy[0],xy[1], label="c")
plt.plot(xy_opt[0],xy_opt[1], label="c_opt")
plt.plot(xy_v0[0],xy_v0[1], label="x=7")
plt.legend()
plt.show()
