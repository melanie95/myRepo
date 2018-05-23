#!/usr/bin/env python
# -*- coding: utf-8 -*-
 
import logging 
from logging.handlers import RotatingFileHandler
import datetime

import parametres

NOM_DOSSIER = parametres.NOM_DOSSIER
NOM_DOSSIER_LOGS = parametres.NOM_DOSSIER_LOGS
NIVEAU_DEBUG = parametres.NIVEAU_DEBUG

# création de l'objet logger qui va nous servir à écrire dans les logs
logger = logging.getLogger()
# on met le niveau du logger à DEBUG ou INFO
if NIVEAU_DEBUG == 'debug':
    logger.setLevel(logging.DEBUG)
else:
    logger.setLevel(logging.INFO)

# création d'un formateur qui va ajouter le temps, le niveau
# de chaque message quand on écrira un message dans le log
formatter = logging.Formatter('%(asctime)s :: %(levelname)s :: %(message)s')

# création d'un handler qui va rediriger une écriture du log vers
# un fichier en mode 'append', avec 1 backup et une taille max de 1Mo
file_handler = RotatingFileHandler(NOM_DOSSIER + NOM_DOSSIER_LOGS + datetime.datetime.now().strftime("%Y%m%d%H%M%S") + '.log', 'a', 1000000, 1)

# on lui met le niveau de debug voulu, on lui dit qu'il doit utiliser le formateur
# créé précédement et on ajoute ce handler au logger
file_handler.setLevel(logging.INFO)
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)
 
# création d'un second handler qui va rediriger chaque écriture de log
# sur la console
stream_handler = logging.StreamHandler()
stream_handler.setLevel(logging.DEBUG)
logger.addHandler(stream_handler)