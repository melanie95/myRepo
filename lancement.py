#! /usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon May  22 18:50:06 2018

@author: melanie
"""

import os
import subprocess

import parametres

NOM_DOSSIER = parametres.NOM_DOSSIER
NOM_DOSSIER_ENTREES = parametres.NOM_DOSSIER_ENTREES

for fichier in os.listdir(NOM_DOSSIER):
    subprocess.call(['C:\\Users\\a0h72502\\Documents\\projets\\bucole2\\main.py', fichier], shell=True)
