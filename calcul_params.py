# -*- coding: utf-8 -*-
"""
Created on Mon Apr  9 14:47:40 2018

@author: melanie
"""

import scipy.optimize as optimize
import numpy
import pandas

import parametres

R = parametres.R
CELSIUS_TO_KELVIN = parametres.CELSIUS_TO_KELVIN
X0 = parametres.X0

def fun(serie_x, serie_temp, serie_time, gamma_0):
    """ fonction bucole2 """
    return (serie_x[1] - gamma_0) * serie_x[2] \
	* numpy.exp(-1*serie_x[5]/R/(serie_temp+CELSIUS_TO_KELVIN)) \
	/ (serie_x[2]*numpy.exp(-1*serie_x[5]/R/(serie_temp+CELSIUS_TO_KELVIN))+serie_x[3]\
	* numpy.exp(-1*serie_x[6]/R/(serie_temp+CELSIUS_TO_KELVIN))) \
	* (1-numpy.exp(-1*(serie_x[2] * numpy.exp(-1*serie_x[5]/R/(serie_temp+CELSIUS_TO_KELVIN)) \
	+ serie_x[3] * numpy.exp(-1*serie_x[6]/R/(serie_temp+CELSIUS_TO_KELVIN)))*serie_time)) \
	+ (serie_x[1]-gamma_0)*serie_x[3]*numpy.exp(-1*serie_x[6]/R/(serie_temp+CELSIUS_TO_KELVIN))\
	/(serie_x[2] * numpy.exp(-1*serie_x[5]/R/(serie_temp+CELSIUS_TO_KELVIN))+serie_x[3] \
	* numpy.exp(-1*serie_x[6]/R/(serie_temp+CELSIUS_TO_KELVIN)) \
	-serie_x[4] * numpy.exp(-1*serie_x[7]/R/(serie_temp+CELSIUS_TO_KELVIN))) \
	*(numpy.exp(-1*serie_x[4]*numpy.exp(-1*serie_x[7]/R\
	/(serie_temp+CELSIUS_TO_KELVIN))*serie_time) \
	-numpy.exp(-1*(serie_x[2]*numpy.exp(-1*serie_x[5]/R\
	/(serie_temp+CELSIUS_TO_KELVIN))+serie_x[3] \
	* numpy.exp(-1*serie_x[6]/R/(serie_temp+CELSIUS_TO_KELVIN)))*serie_time)) + gamma_0

def error_func(serie_x, serie_temp, serie_time, gamma_0, serie_y):
    """ calcul de l'ecart entre les points mesures (vecteur y) et
	les points calcules par la fonction fun """
    return serie_y - fun(serie_x, serie_temp, serie_time, gamma_0)

def min_residual(serie_x, serie_temp, serie_time, gamma_0, serie_y):
    """ calcul du carre des ecarts entre points mesures y
    et points estimes par la fonction fun """
    return sum(error_func(serie_x, serie_temp, serie_time, gamma_0, serie_y)**2)

def calcul_param(list_courbe_rheo, lancement_optim, nom_methode_optim, optim_double=False):
    """ A partir d 'une liste de courbes rheometriques, renvoie les parametres optimises
    pour ajuster la fonction fun aux donnees
	lancement_optim : si false la fonction renvoie le vecteur initial comme resultat
	nom_methode_optim : si vide, utilisation de la fonction leastsq,
	sinon utilisation de la fonction minimize avec la methode choisie"""
    # Calcul de gamma_0 et initiation de gamma_m
    gamma_0 = 0
    gamma_m = 0
    for i in range(len(list_courbe_rheo)):
        gamma_0 = gamma_0 + pandas.DataFrame.min(list_courbe_rheo[i].donnees[2], skipna=True)
        gamma_m = gamma_m + pandas.DataFrame.max(list_courbe_rheo[i].donnees[2], skipna=True)
    gamma_0 = gamma_0 / len(list_courbe_rheo)
    gamma_m = gamma_m / len(list_courbe_rheo)

    # initialisation du vecteur resultat
    X0[0] = gamma_0
    X0[1] = gamma_m

    # agregation des dataframes donnees de chaque temperature
    if lancement_optim is True:
        liste_dataframe = []
        for i in range(len(list_courbe_rheo)):
            liste_dataframe.append(list_courbe_rheo[i].donnees)
        donnees_courbe_rheo = pandas.concat(liste_dataframe)

        if optim_double is False:
            if nom_methode_optim == '':
                return optimize.leastsq(error_func, X0, \
				args=(donnees_courbe_rheo[1], donnees_courbe_rheo[0], \
				gamma_0, donnees_courbe_rheo[2]))

            return optimize.minimize(min_residual, X0, method=nom_methode_optim, \
		    args=(donnees_courbe_rheo[1], donnees_courbe_rheo[0], \
			gamma_0, donnees_courbe_rheo[2]))

        else:
            if nom_methode_optim == '':
                return optimize.leastsq(error_func, \
				optimize.leastsq(error_func, X0, \
				args=(donnees_courbe_rheo[1], donnees_courbe_rheo[0], \
				gamma_0, donnees_courbe_rheo[2]))[0], \
				args=(donnees_courbe_rheo[1], donnees_courbe_rheo[0], \
				gamma_0, donnees_courbe_rheo[2]))

            return optimize.minimize(min_residual, \
			optimize.minimize(min_residual, X0, method=nom_methode_optim, \
			args=(donnees_courbe_rheo[1], donnees_courbe_rheo[0], \
			gamma_0, donnees_courbe_rheo[2]))['param'], \
			method=nom_methode_optim, args=(donnees_courbe_rheo[1], donnees_courbe_rheo[0], \
			gamma_0, donnees_courbe_rheo[2]))

    return [X0, 1]
