import math
import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import brentq
import simulation as sm

g = 9.81
m = 0.1

a_x = lambda v, c: -c/m*abs(v)*v
a_y = lambda v, c:-g-c/m*abs(v)*v

def dif(c, v0, x):
    xy = sm.simulation_xy(
        sm.SimC(a= lambda v : a_x(v,c), v_0 = v0),
        sm.SimC(a=lambda v : a_y(v,c), v_0 = v0)
    )
    return xy[0][-1] - x

def find_c_shell():
    print("Make sure your angle is 45°")
    quit = False
    while not quit:
        quit = True
        try:
            x_mesured = float(input("What is the distance mesured?: "))
            v_mesured = float(input("What is the velocity mesured?: "))
        except:
            print("Input must be a float")
            quit = False

    c_opt = brentq(lambda c: dif(c, v_mesured, x_mesured), 0, 20)
    xy_opt = sm.simulation_xy(
        sm.SimC(a=lambda v : a_x(v,c_opt), v_0 = v_mesured),
        sm.SimC(a=lambda v : a_y(v,c_opt), v_0 = v_mesured)
    )
    plt.figure()
    plt.plot(xy_opt[0],xy_opt[1])
    plt.xlabel("x [m]")
    plt.ylabel("y [m]")
    plt.legend()
    plt.show()

def find_v0_shell():
    print("Make sure your angle is 45°")
    quit = False
    while not quit:
        quit = True
        try:
            x_needed= float(input("What is the needed distance?: "))
        except:
            print("Input must be a float")
            quit = False

    c = 0.01
    v0_wanted = brentq(lambda v: dif(c, v, x_needed), 0, 50)
    xy_v0 = sm.simulation_xy(
        sm.SimC(a= lambda v : a_x(v,c), v_0 = v0_wanted),
        sm.SimC(a=lambda v : a_y(v,c), v_0 = v0_wanted)
    )
    plt.figure()
    plt.plot(xy_v0[0],xy_v0[1])
    plt.xlabel("x [m]")
    plt.ylabel("y [m]")
    plt.legend()
    plt.show()
