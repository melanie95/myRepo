#! /usr/bin/env python3
# -*- coding: utf-8 -*-`
"""
Created on Mon Apr  9 10:50:06 2018

@author: melanie
"""

import pandas

import courbe_rheo
import calcul_params
import AffichageResultats
import parametres

# lecture des parametres
NB_PORT = parametres.NB_PORT
NB_COURBES = parametres.NB_COURBES
TEMPS_MAX = parametres.TEMPS_MAX
NOM_DOSSIER = parametres.NOM_DOSSIER
NOM_FICHIER = parametres.NOM_FICHIER
NOM_FICHIER_SORTIE = parametres.NOM_FICHIER_SORTIE
NOM_FICHIER_RESULTATS = parametres.NOM_FICHIER_RESULTATS
NOM_FICHIER_TEMPERATURES = parametres.NOM_FICHIER_TEMPERATURES
NOM_METHODE_OPTIM = parametres.NOM_METHODE_OPTIM
LANCEMENT_APPLI = parametres.LANCEMENT_APPLI
LANCEMENT_OPTIM = parametres.LANCEMENT_OPTIM
OPTIM_DOUBLE = parametres.OPTIM_DOUBLE

def main():
    """ main """
    # lecture du fichier des courbes rheo
    donnees = pandas.read_csv(NOM_DOSSIER + NOM_FICHIER, sep=';', decimal=',', header=0)
    nb_colonnes_donnees = len(donnees.columns)
    donnees.columns = ['a', 'b', 'c', 'd', 'e', 'f'][:nb_colonnes_donnees]
    debut = donnees.index[donnees['a'] == 'XML']

    list_courbe_rheo = list()
    for i in range(0, NB_COURBES):
        list_courbe_rheo.append(courbe_rheo.CourbeRheo(\
		NOM_DOSSIER, NOM_FICHIER, nb_colonnes_donnees, debut[i])\
		.supp_points_decroissants().supp_points_trop_loin(TEMPS_MAX))

    # estimation des parametres du modele
    param = calcul_params.calcul_param(\
	list_courbe_rheo, LANCEMENT_OPTIM, NOM_METHODE_OPTIM, LANCEMENT_OPTIM & OPTIM_DOUBLE)
    if (NOM_METHODE_OPTIM != "") & (LANCEMENT_OPTIM is True):
        param = [param['x'], param['success']]
    print(param)

    # calcul des Sestimes
    liste_dataframe = []
    for i in range(len(list_courbe_rheo)):
        liste_dataframe.append(list_courbe_rheo[i].donnees)
    donnees_courbe_rheo = pandas.concat(liste_dataframe)
    donnees_courbe_rheo.columns = ['Temps', 'Temperature', 'S', 'd', 'e', 'f'][:nb_colonnes_donnees]
    donnees_courbe_rheo_estimees = []
    for i in range(len(list_courbe_rheo)):
        for j in range(len(liste_dataframe[i])):
            donnees_courbe_rheo_estimees.append(calcul_params.fun(\
			param[0], liste_dataframe[i][1].values[j], liste_dataframe[i][0].values[j], param[0][0]))
    donnees_courbe_rheo['Sestime'] = pandas.Series(donnees_courbe_rheo_estimees, \
	index=donnees_courbe_rheo.index)

    # evaluation du modele
    # ecarts en distance 1
    ecart_donnees_estimees1 = donnees_courbe_rheo['S']-donnees_courbe_rheo_estimees
    # ecarts en distance 2
    ecart_donnees_estimees2 = pow(donnees_courbe_rheo['S']-donnees_courbe_rheo_estimees, 2)

    # ecarts max
    ecart_min = min(ecart_donnees_estimees1)
    ecart_max = max(ecart_donnees_estimees1)

    # calcul des distances
    ecart_donnees_estimees1 = abs(ecart_donnees_estimees1)
    distance1 = sum(ecart_donnees_estimees1)/len(donnees_courbe_rheo_estimees)
    distance2 = pow(sum(ecart_donnees_estimees2), 0.5)/len(donnees_courbe_rheo_estimees)

    # ecriture des resultats dans un fichier csv
	# estimation de la qualite du modele
    res = pandas.DataFrame([(NOM_METHODE_OPTIM, ecart_min, ecart_max, distance1, distance2)], \
	columns=['Methode', 'ecartMin', 'ecartMax', 'distance1', 'distance2'])
    res = res.transpose()
    res.to_csv(NOM_DOSSIER + NOM_FICHIER_SORTIE, encoding='utf_8', header=False)
    # donnees a afficher
    donnees_courbe_rheo.to_csv(NOM_DOSSIER + NOM_FICHIER_RESULTATS, encoding='utf_8', index=False)
	# temperatures
    liste_temp = list()
    for i in range(len(list_courbe_rheo)):
        liste_temp.append(float(list_courbe_rheo[i].courbe_s))
    liste_temp = pandas.DataFrame(liste_temp)
    liste_temp.to_csv(NOM_DOSSIER + NOM_FICHIER_TEMPERATURES, \
	encoding='utf_8', index=False, header=False)

    #lancement de l'appli
    if LANCEMENT_APPLI is True:
        AffichageResultats.app.run_server(port=NB_PORT, debug=True)


if __name__ == "__main__":
    main()
