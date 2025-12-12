#tracker.py
#analyze tracker data
import math
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import optimize
import simulation as sm

#one row of data
class Mesure:
    def __init__(self, row):
        self.temps = row[0]
        self.x = row[1]
        self.y = row[2]
        self.vitesseX = row[3]
        self.vitesseY = row[4]

#full data table
class Tableau_de_mesure:
    def __init__(self):
        self.x = []
        self.y = []
        self.t = []
        self.vx = []
        self.vy = []
    def add_mesure(self,mesure):
        self.x.append(mesure.x)
        self.y.append(mesure.y)
        self.t.append(mesure.temps)
        self.vx.append(mesure.vitesseX)
        self.vy.append(mesure.vitesseY)
    #make ground level 0, breaks if simulation does not end at ground
    def normalize(self):
        x0 = self.x[0]
        y0 = self.y[-1]  # ground at end of trajectory
        self.x = [x - x0 for x in self.x]
        self.y = [y - y0 for y in self.y]
        if self.x[-1] < 0:
            self.x = [-x for x in self.x]
            self.vx = [-vx for vx in self.vx]


#read data from file
def read_tracker(file_name):
    #on va parcourir le fichier texte et stocker les mesures dans un tableau

    #on crée le tableau
    table=Tableau_de_mesure()

    # on lit le fichier CSV
    with open(file_name, "r",) as f:
        #skip csv parameters
        f.readline()
        #skip firs ligne
        f.readline()
        for ligne in f:
            row = []
            try:
                for p in ligne.replace(",",".").split("\t"): #may be different in your file
                    row.append(float(p.strip()))
            except:
                break
            table.add_mesure(Mesure(row))
    table.normalize()
    return table 

#plot data
def plot_tracker(tables):
    plt.figure(1)
    #find the simulation
    t = tables[0]
    #find drag constant for ball. If multiple different balls are used in the same graph this will fail.
    c = optimize.find_c((t.vx[0] + t.vx[1])/2, (t.vy[0] + t.vy[1])/2, t.y[0], t.x[-1])
    i = 1
    for table in tables:
        plt.plot(table.x,table.y, label = "measurement " + str(i))
        sim = sm.simulation_xy(
            sm.SimC(a=lambda v : optimize.a_x(v,c), v_0 = (table.vx[0] + table.vx[1])/2),
            sm.SimC(a=lambda v : optimize.a_y(v,c), v_0 = (table.vy[0] + table.vy[1])/2, x_0 = table.y[0])
        )
        plt.plot(sim[0],sim[1], label = "simulation " + str(i))
        i += 1

    plt.xlabel("x [m]")
    plt.ylabel("y [m]")
    plt.legend()
    plt.show()

#shell helper
def tracker_shell():
    try:
        num = int(input("Number of files: "))
    except:
        print("input must be int")
        return
    tables = []
    for i in range(num):
        file_name = input("Enter filename: ")
        try:
            with open(file_name, "r"):
                pass
        except:
            print("unable to open file")
            return
        tables.append(read_tracker(file_name))

    plot_tracker(tables)
