#optimize.py
#find parameters using the euler method
import math
import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import brentq
import simulation as sm

g = 9.81

#acceleration functions
a_x = lambda v, c: -c*abs(v)*v
a_y = lambda v, c:-g-c*abs(v)*v

#difference from simulaed and actual distance
def dif(c, v0, x, angle):
    xy = sm.simulation_xy(
        sm.SimC(a = lambda v : a_x(v,c), v_0 = v0 * math.cos(angle)),
        sm.SimC(a = lambda v : a_y(v,c), v_0 = v0 * math.sin(angle))
    )
    return xy[0][-1] - x

# find the drag coefficient wich describes compleately the ball - size and mass included
def find_c_shell():
    quit = False
    while not quit:
        quit = True
        try:
            angle = float(input("What is the angle?: "))/180*math.pi
            x_mesured = float(input("What is the distance mesured?: "))
            v_mesured = float(input("What is the velocity mesured?: "))
        except:
            print("Input must be a float")
            quit = False

    # use brenteq to find zeros of a function (here the difference in distance as a function of coefficient)
    c_opt = brentq(lambda c: dif(c, v_mesured, x_mesured, angle), 0, 20)
    print("The balls drag coefficient is: " + str(c_opt))
    xy_opt = sm.simulation_xy(
        sm.SimC(a=lambda v : a_x(v,c_opt), v_0 = v_mesured * math.cos(angle)),
        sm.SimC(a=lambda v : a_y(v,c_opt), v_0 = v_mesured * math.sin(angle))
    )
    plt.figure()
    plt.plot(xy_opt[0],xy_opt[1])
    plt.xlabel("x [m]")
    plt.ylabel("y [m]")
    plt.show()

# find v0 to attaign a distance
def find_v0_shell():
    quit = False
    while not quit:
        quit = True
        try:
            angle = float(input("What is the angle?: "))/180*math.pi
            c = float(input("What is the c of the ball?: "))
            x_needed= float(input("What is the needed distance?: "))
        except:
            print("Input must be a float")
            quit = False

    v0_wanted = brentq(lambda v: dif(c, v, x_needed, angle), 0, 100)
    print("the velocity you need is: " + str(v0_wanted))
    xy_v0 = sm.simulation_xy(
        sm.SimC(a= lambda v : a_x(v,c), v_0 = v0_wanted * math.cos(angle)),
        sm.SimC(a=lambda v : a_y(v,c), v_0 = v0_wanted * math.sin(angle))
    )
    plt.figure()
    plt.plot(xy_v0[0],xy_v0[1])
    plt.xlabel("x [m]")
    plt.ylabel("y [m]")
    plt.show()
