# -*- coding: utf-8 -*-
"""
Created on Mon Apr  9 10:50:06 2018

@author: melanie
"""
import pandas

class CourbeRheo:
    """ Classe defissant une courbe rheometrique pour une temperature donneee """

    def __init__(self, dossier, fichier, nbColonnes, debLigne):
        """ methode init"""
        donnees = pandas.read_csv(dossier + fichier, sep=';', decimal=','\
		, header=0, names=['a', 'b', 'c', 'd', 'e', 'f'][:nbColonnes])
        self.xml = donnees['b'].values[debLigne]
        self.gamme = donnees['b'].values[debLigne+1]
        self.cmin = donnees['b'].values[debLigne+2]
        self.cmax = donnees['b'].values[debLigne+3]
        self.ts2 = donnees['b'].values[debLigne+4]
        self.t50 = donnees['b'].values[debLigne+5]
        self.t90 = donnees['b'].values[debLigne+6]
        self.courbe_s = donnees['b'].values[debLigne+7]
        self.nb_res = int(donnees['b'].values[debLigne+8].split('/')[1])
        self.donnees = pandas.DataFrame(donnees.values[debLigne+10:debLigne+self.nb_res-1])
        self.donnees[0] = self.donnees[0].astype(float, errors='ignore')
        self.donnees[1] = self.donnees[1].astype(float, errors='ignore')
        self.donnees[2] = self.donnees[2].astype(float, errors='ignore')

    def supp_points_decroissants(self):
        """ methode de suppression des points decroissants au debut de la courbe"""
        i = 0
        while self.donnees[2][i]-self.donnees[2][i+1] >= 0:
            i = i+1
        self.donnees = self.donnees.loc[self.donnees.index >= i]
        return self

    def supp_points_trop_loin(self, limite):
        """ methode de suppression des points dont le temps est superieur a une limite"""
        self.donnees = self.donnees.loc[self.donnees[0] <= limite]
        return self
	
    def calcul_derivee(self):
	    """ methode permettant de calculer la derivee en chaque point de la courbe """
	    derivee[0] = [0]
        for in len(range(self.donnees)) - 2:
            derivee.append((self.donneee[2][i+2]-donneee[2][i])/(self.donneee[0][i+2]-donneee[0][i])	    
        derivee.append(0)
	    return derivee
	
	def max_derivee(self):
	    """ methode qui retourne les infos du point de derivee max """
	    derivee = self.calcul_derivee()
	    return [self.donnees.iloc[derivee.index(max(derivee)], max(derivee)]
	
	def calcul_ti(self):
	    """ methode d'indentification des ti et de suppression des points avant le ti
        ti corresond au point d'inflexion de la courbe """
	    point_max = max_derivee(self)
		offset = point_max[0][2] - point_max[0][0] * point_max[1]
		ti = (min(self.donnees[2]) - offset) / point_max[1]
		return ti

    def supp_points_avant_ti(self):
        """ methode permettant de supprimer les points de la courbe 
		avant la valeur calculee de ti """
		self.donnees = self.donnees.loc[self.donnees[0] <= self.calcul_ti()]
        return self
		
