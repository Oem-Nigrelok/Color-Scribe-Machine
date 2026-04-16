Recommendation pour augmenter la vitesse d'éxécution : installer pypy comme interpréteur (ref: https://pypy.org/)


Importations / installations nécéssaires :

import tkinter as tk ------------------------- pip install tkinter

import ast ----------------------------------- installé de base

from PIL import Image, ImageFilter ----------- pip install pillow


Interface graphique Tkinter simpliste avec quelques outils:

  Gomme -------------------------------------- variation de la taille
  
  Crayon (couleurs choisissables) ------------ variation de la taille (recomandée : max 7 sans pypy) et gestion des performances
  
  Rectangle (couleurs choisissables)
  
  Rectangle remplit (couleurs choisissables)
  
  Ligne (couleurs choisissables)
  
  Bouton retour ------------------------------ prise en charge de tous les tracés sauf la gomme

  
Interface adaptable:

  Taille de la fenêtre
  
  Couleur fenêtre
  
  Zoom d'origine ----------------------------- adapté à un écran moyen

  
Format d'exportation multiple:
  
  .txt
  
  .gcode ------------------------------------- gestion des couleurs créées en différents fichiers
  
  Les résultats des mélanges seront aussi gérés par le logitiel. Aucune couleur en dehors de la palette rentrée par l'utilisateur ne sera demandée.


Outils intelligents (avec Pillow):

  Import d'image ----------------------------- réduction de couleur intégrée (5s à max 20 min en fonction de la palette et de l'image)
  
  Transformation d'une image en contour ------ noir (5s à max 20 min en fonction de l'image)
  
  Gestion de la pallette de couleur ---------- création de couleur par synthèse soustractive des couleurs tapées
  
  Les temps d'exécution maximaux sont calculés par admition d'un calcul / ms
