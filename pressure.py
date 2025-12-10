#pressure.py
#this file was never used nor tested and may contain bugs.
#this file is used to find the pressure needed to attaign an initial velocity
import math
import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import least_squares

step = 0.001
end = 1

class SimPressureC:
    def __init__(self, a, f, p_0):
        self.x = np.zeros(int(end/step)) #position as a function of time step
        self.x[0] = 0
        self.a = a #acceleration function
        self.f = f #friction function
        self.p_0 = p_0 #initial pressure

    #euler method
    def simulate(self):
        v = 0
        for i in range(len(self.x)-1):
            v += self.a(self.x[i], v, self.f, self.p_0) * step
            self.x[i+1] = self.x[i] + v * step
        return v

def acceleration(x, v, f, p_0): #position, velocity, friction function, pressure at 0
    V_0 = 0.1   #volume at 0
    M = 0.1     #mass
    A = 0.5     #area of canon
    P_A = 1001  #atmospheric pressure
    G = 1.4     #adiabatic constant
    return (A*(p_0*(V_0/(V_0+A*x))**G - P_A) - f(v))/M

#difference in simulated and mesured velocity
def velocity_diff(parms, p_0, v_1): #parms are the friction constants
    friction = lambda v : parms[0]*abs(v)*v + parms[1]*v + parms[2]
    sim = SimPressureC(acceleration, friction, p_0)
    return sim.simulate() - v_1

#find the friction in the thrower as a function of velocity using leas squares
def find_friction(data): #data is a list of velocity  to pressure
    #find difference vector as function of parameters used
    def residuals(params):
        r = []
        for p_0, v_1 in data:
            r.append(velocity_diff(params, p_0, v_1))
        return r

    params0 = [0.1, 0.1, 0.1]   # initial guess
    result = least_squares(residuals, params0)
    return result.x

#testing function
def test():
    #matrix of mesurments pressure and velocity - fake data
    data = [
        (120000, 35.0),
        (140000, 42.5),
        (160000, 48.0),
    ]
    parms = find_friction(data)
    # simulate with final parameters
    friction = lambda v : parms[0]*abs(v)*v + parms[1]*v + parms[2]
    sim = SimPressureC(acceleration, friction, data[0][0])
    v = sim.simulate()
    print(v)
    print(parms)

