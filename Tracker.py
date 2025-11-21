import math
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

class Mesure:
    
    def __init__(self,temps,x,y,vitesseX,vitesseY):
        self.temps = temps
        self.x = x
        self.y = y
        self.vitesseX = vitesseX
        self.vitesseY = vitesseY

class Tableau_de_mesure:
    def __init__(self):
        self.mesures=[]
        self.x = []
        self.y = []
        self.t = []
        
    def add_mesure(self,mesure):
        self.mesures.append(mesure)
        self.x.append(mesure.x)
        self.y.append(mesure.y)
        self.t.append(mesure.temps)
    
def read_tracker(file_name):
    #on va parcourir le fichier texte et stocker les mesures dans un tableau

    #on crée le tableau
    tableau_de_mesure=Tableau_de_mesure()

    # on lit le fichier CSV
    with open(file_name, "r",) as f:
        #skip csv parameters
        f.readline()
        #skip csv column names
        f.readline()
        for ligne in f:
            parts = ligne.split(",")
            #ici nous allons traiter chaque mesure donnée dans le fichier
            #on va stocker dans notre tableau de mesure les mesures
            mesure = Mesure(float(parts[0].strip()),float(parts[1].strip()),float(parts[2].strip()),0,0)
            tableau_de_mesure.add_mesure(mesure)

def plot_tracker(table):
    print("nombre de mesures : ", len(table.mesures))
    print(" les temps : " , table.t)
    print(" les y : " , table.y)
    #on veut tracer un graphique avec les mesures
    plt.figure(1)
    #on doit pouvoir récupérer les coordonnées
    plt.plot(table.t,table.y,
        label="",
        color="magenta")

    plt.xlabel("t [s]")
    plt.ylabel("y [m]")
    plt.legend(loc="upper right")
    plt.tight_layout()
    plt.show()
