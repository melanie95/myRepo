#! /usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Apr  9 10:50:06 2018

@author: melanie
"""

NB_PORT = 8051
NB_COURBES = 3
TEMPS_MAX = 100000
R = 8.31
CELSIUS_TO_KELVIN = 273
NOM_DOSSIER = "C:\\Users\\a0h72502\\Documents\\projets\\bucole2\\"
NOM_FICHIER = "curv_s670146962.txt" #"curv_sMelanie.txt"
NOM_FICHIER_SORTIE = "res.csv"
NOM_FICHIER_RESULTATS = "resultats.csv"
NOM_FICHIER_TEMPERATURES = "temperatures.csv"
NOM_METHODE_OPTIM = "" # si vide : optimize.leastsq sinon optimize.minimize avec la methode choisie
LANCEMENT_APPLI = True
LANCEMENT_OPTIM = True
OPTIM_DOUBLE = False
X0 = [2, 15, 1e+05, 1e+9, 1e+13, 1e+05, 1e+05, 1e+05]
