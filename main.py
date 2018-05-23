#! /usr/bin/env python3
# -*- coding: utf-8 -*-`
"""
Created on Mon Apr  9 10:50:06 2018

@author: melanie
"""
import sys
import numpy
import pandas
import os.path
import shutil

import courbe_rheo
import calcul_params
import affichage_resultats
import parametres
import log_infos

# lecture des parametres
NB_PORT = parametres.NB_PORT
NB_COURBES = parametres.NB_COURBES
TEMPS_MAX = parametres.TEMPS_MAX
NOM_DOSSIER = parametres.NOM_DOSSIER
NOM_DOSSIER_ENTREES = parametres.NOM_DOSSIER_ENTREES
NOM_DOSSIER_ENTREES_TRAITEES = parametres.NOM_DOSSIER_ENTREES_TRAITEES
NOM_DOSSIER_SORTIES = parametres.NOM_DOSSIER_SORTIES
NOM_DOSSIER_SORTIES_TEMP = parametres.NOM_DOSSIER_SORTIES_TEMP
NOM_DOSSIER_LOGS = parametres.NOM_DOSSIER_LOGS
NOM_FICHIER_SORTIE = parametres.NOM_FICHIER_SORTIE
NOM_FICHIER_RESULTATS = parametres.NOM_FICHIER_RESULTATS
NOM_FICHIER_TEMPERATURES = parametres.NOM_FICHIER_TEMPERATURES
NOM_FICHIER_COEFFICIENTS = parametres.NOM_FICHIER_COEFFICIENTS
NOM_METHODE_OPTIM = parametres.NOM_METHODE_OPTIM
LANCEMENT_APPLI = parametres.LANCEMENT_APPLI
LANCEMENT_OPTIM = parametres.LANCEMENT_OPTIM
OPTIM_DOUBLE = parametres.OPTIM_DOUBLE
logger = log_infos.logger
formatter = log_infos.formatter
file_handler = log_infos.file_handler
stream_handler = log_infos.stream_handler

def main():
    """ main
    passer le nom du fichier en parametre du main
    format : chemin depuis le dossier NOM_DOSSIER_ENTREES """
    logger.info('Lancement du programme de calcul des parametres')

    # log des parametres
    logger.info('PARAMETRES DE LANCEMENT:')
    logger.info('Nombre de courbes : ' + str(NB_COURBES))
    logger.info('Lancement de l\'optimisation : ' + str(LANCEMENT_OPTIM))
    logger.info('Methode d\'optimisation utilisee : ' + NOM_METHODE_OPTIM)

    # verification de l'existance des dossiers
    # creation des fichiers resultats et logs si pas existants
    try:
        os.stat(NOM_DOSSIER)
    except:
        logger.error("Dossier global non existant")
        sys.exit()

    try:
        os.stat(NOM_DOSSIER + NOM_DOSSIER_ENTREES)
    except:
        logger.error("Dossier des fichiers d'entree non existant")
        sys.exit()

    try:
        os.stat(NOM_DOSSIER + NOM_DOSSIER_ENTREES_TRAITEES)
    except:
        os.mkdir(NOM_DOSSIER + NOM_DOSSIER_ENTREES_TRAITEES)
        logger.warning("creation du dossier des entrees traitees :" + NOM_DOSSIER + NOM_DOSSIER_ENTREES_TRAITEES)

    try:
        os.stat(NOM_DOSSIER + NOM_DOSSIER_SORTIES)
    except:
        os.mkdir(NOM_DOSSIER + NOM_DOSSIER_SORTIES)
        logger.warning("creation du dossier des sorties :" + NOM_DOSSIER + NOM_DOSSIER_SORTIES)

    try:
        os.stat(NOM_DOSSIER + NOM_DOSSIER_SORTIES_TEMP)
    except:
        os.mkdir(NOM_DOSSIER + NOM_DOSSIER_SORTIES_TEMP)
        logger.warning("creation du dossier des sorties temporaires :" + NOM_DOSSIER + NOM_DOSSIER_SORTIES_TEMP)

    try:
        os.stat(NOM_DOSSIER + NOM_DOSSIER_LOGS)
    except:
        os.mkdir(NOM_DOSSIER + NOM_DOSSIER_LOGS)
        logger.warning("creation du dossier des logs :" + NOM_DOSSIER + NOM_DOSSIER_LOGS)


    # lecture du fichier des courbes rheo
    nom_fichier = sys.argv[1]
    if isinstance(nom_fichier, str) is False:
        logger.error('Nom de fichier (' + nom_fichier + ') incorrect, mauvais format')
        sys.exit()
    if nom_fichier == "":
        logger.error('Pas de nom de fichier en parametre')
        sys.exit()
    if os.path.isfile(NOM_DOSSIER + NOM_DOSSIER_ENTREES + nom_fichier) is False:
        logger.error('Fichier ' + NOM_DOSSIER + NOM_DOSSIER_ENTREES + nom_fichier + ' non existant')
        sys.exit()
    
    logger.info('Fichier correct')
	
    logger.info('Lecture fichier')
	
    try:
        with open(NOM_DOSSIER + NOM_DOSSIER_ENTREES + nom_fichier, encoding="ISO-8859-1") as f:
            donnees = f.readlines()
    except:
        logger.error('Lecture fichier en echec')
        sys.exit()

    # mise en forme des donnees de courbes rheo
    logger.info('Mise en forme des courbes')
    try:
        donnees = pandas.DataFrame([x.replace("\n", "").replace("\"","").replace("'","").split(";") for x in donnees])
    except:
        logger.error('Probleme dans le format du fichier')
        sys.exit()

    nb_colonnes_donnees = len(donnees.columns)
    logger.debug(donnees.head(3))
    logger.debug('Nombre de colonnes du fichier : ' + str(nb_colonnes_donnees))
    donnees.columns = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h'][:nb_colonnes_donnees]
    try:
        debut = donnees.index[donnees['a'] == 'XML']
    except:
        logger.error('ligne de debut (XML) introuvable')
        sys.exit()

    logger.info('Creation des courbes rheo')
    try:
        list_courbe_rheo = list()
        for i in range(0, NB_COURBES):
            list_courbe_rheo.append(courbe_rheo.CourbeRheo(\
		    NOM_DOSSIER + NOM_DOSSIER_ENTREES, nom_fichier, nb_colonnes_donnees, debut[i])\
		    .supp_points_avant_ti())
    except:
        logger.error('Probleme a la creation des courbes rheo')
        sys.exit()

    # estimation des parametres du modele
    logger.info('Estimation des parametres du modele')
    try:
        param = calcul_params.calcul_param(\
	    list_courbe_rheo, LANCEMENT_OPTIM, NOM_METHODE_OPTIM, LANCEMENT_OPTIM & OPTIM_DOUBLE)
        if (NOM_METHODE_OPTIM != "") & (LANCEMENT_OPTIM is True):
            param = [param['x'], param['success']]
    except:
        logger.error('Echec de l\'optimisation du modele')
        sys.exit()

    # calcul des Sestimes
    logger.info('Calcul des S estimes')
    liste_dataframe = []
    for i in range(len(list_courbe_rheo)):
        liste_dataframe.append(list_courbe_rheo[i].donnees)
    donnees_courbe_rheo = pandas.concat(liste_dataframe)
    logger.debug('Format des donnees de courbes rheo :' + str(donnees_courbe_rheo.shape[0]) + ', ' + str(donnees_courbe_rheo.shape[1]))
    donnees_courbe_rheo.columns = ['Temps', 'Temperature', 'S', 'Temperature Courbe', 'd', 'e', 'f', 'g', 'h', 'i', 'j'][:donnees_courbe_rheo.shape[1]]
    donnees_courbe_rheo_estimees = []
    try:
        for i in range(len(list_courbe_rheo)):
            for j in range(len(liste_dataframe[i])):
                donnees_courbe_rheo_estimees.append(calcul_params.fun(\
			    param[0], liste_dataframe[i][1].values[j], liste_dataframe[i][0].values[j], param[0][0]))
        donnees_courbe_rheo['Sestime'] = pandas.Series(donnees_courbe_rheo_estimees, \
	    index=donnees_courbe_rheo.index)
    except:
        logger.error('Probleme dans l\'estimation des S')
        sys.exit()

    # evaluation du modele
    logger.info('Evaluation du modele')
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
    logger.info('Ecriture des resultats dans les fichiers')
	# estimation de la qualite du modele
    res = pandas.DataFrame([(NOM_METHODE_OPTIM, nom_fichier, ecart_min, ecart_max, distance1, distance2)], \
	columns=['Methode', 'Nom fichier', 'ecart min', 'ecart max', 'distance 1', 'distance 2'])
    res = res.transpose()
    res.to_csv(NOM_DOSSIER + NOM_DOSSIER_SORTIES + nom_fichier + "_" + NOM_FICHIER_SORTIE, encoding='utf_8', header=False)
    # donnees a afficher
    donnees_courbe_rheo.to_csv(NOM_DOSSIER + NOM_DOSSIER_SORTIES_TEMP + nom_fichier + "_" + NOM_FICHIER_RESULTATS, encoding='utf_8', index=False)
	# temperatures
    liste_temp = list()
    for i in range(len(list_courbe_rheo)):
        liste_temp.append(float(list_courbe_rheo[i].courbe_s))
    liste_temp = pandas.DataFrame(liste_temp)
    liste_temp.to_csv(NOM_DOSSIER + NOM_DOSSIER_SORTIES_TEMP + nom_fichier + "_" + NOM_FICHIER_TEMPERATURES, \
	encoding='utf_8', index=False, header=False)
    # coefficients
    pandas.DataFrame(param[0]).to_csv(NOM_DOSSIER + NOM_DOSSIER_SORTIES + nom_fichier + "_" + NOM_FICHIER_COEFFICIENTS, encoding='utf_8', index=False)

    # deplacement du fichier traite
    #shutil.move(NOM_DOSSIER + NOM_DOSSIER_ENTREES + nom_fichier, NOM_DOSSIER + NOM_DOSSIER_ENTREES_TRAITEES + nom_fichier)
    logger.info('Fin du lancement du programme de calcul des parametres')
	
    # lancement de l'appli
    if LANCEMENT_APPLI is True:
        logger.info('Lancement de l\'appli')
        affichage_resultats.app.run_server(port=NB_PORT, debug=True)

    sys.exit()

if __name__ == "__main__":
    main()
