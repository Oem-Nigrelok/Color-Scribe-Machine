Recommendation pour augmenter la vitesse d'éxécution : installer pypy comme interpréteur (fichier python.exe)(ref: https://pypy.org/)

ATTENTION COLOR SCRIBE MACHINE GROUP VOUS RECOMMANDE VIVEMENT DE PLACER DANS LE FICHIER VOTRE PALETTE DE COULEUR QUOTIDIENNE POUR NE PAS AVOIR A LA REECRIRE. ELLE RESTERA DANS CE FICHIER TANT QUE CE FICHIER EXISTE.
-----> liste_de_couleurs_utilisables_de_base = [(0, 255, 255), (255, 255, 0), (255, 0, 255)]
# A modifier (sous format : (r, g, b), (r, g, b), ...)

Importations / installations nécéssaires :

import tkinter as tk ------------------------- pip install tkinter

import ast ----------------------------------- installé de base

from PIL import Image, ImageFilter ----------- pip install pillow


Interface graphique Tkinter simpliste avec quelques outils:

  Gomme -------------------------------------- variation de la taille
  
  Crayon (couleurs choisissables) ------------ variation de la taille (recomandée : max 7 sans pypy) et gestion des performances
  
  Rectangle (couleurs choisissables)
  
  Rectangle remplit (couleurs choisissables)
  
  Ligne (couleurs choisissables) ------------ variation de la taille
  
  Bouton retour ------------------------------ prise en charge de tous les tracés sauf la gomme

  
Interface adaptable:

  Taille de la fenêtre
  
  Couleur fenêtre
  
  Zoom d'origine ----------------------------- adapté à un écran moyen

  
Format d'exportation multiple:
  
  .txt
  
  .gcode ------------------------------------- gestion des couleurs créées en différents fichiers
  
  Les résultats des mélanges seront aussi gérés par le logitiel. Aucune couleur en dehors de la palette rentrée par l'utilisateur ne sera demandée.


Outils intelligents:

  Import d'image ----------------------------- réduction de couleur intégrée (5s à max 20 min en fonction de la palette et de l'image)
  
  Transformation d'une image en contour ------ noir (5s à max 20 min en fonction de l'image)
  
  Gestion de la pallette de couleur ---------- création de couleur par synthèse soustractive des couleurs tapées

  Combiner les tracés proches (Gcode) -------- (5s à max 20 min en fonction des tracés fait)

  Type de configuration ---------------------- De base ou personnalisée

  Dessiner avec la palette ------------------- Ajout de couleurs possible pendant le dessin

  Viewer de la couleur actuelle

  Voir la palette de couleur
  
  Les temps d'exécution maximaux sont calculés par admition d'un calcul par mseconde, sans pypy


Racourcis clavier:

"<z>" ---------------------------------------- retour()

"<Z>" ---------------------------------------- retour()

"<r>" ---------------------------------------- rouge()

"<R>" ---------------------------------------- rouge()

"<t>" ---------------------------------------- rectangle()

"<T>" ---------------------------------------- rectangle()

"<y>" ---------------------------------------- cyan()

"<Y>" ---------------------------------------- cyan()

"<u>" ---------------------------------------- changement_de_type_de_performance()

"<U>" ---------------------------------------- changement_de_type_de_performance()

"<i>" ---------------------------------------- image_en_couleur()

"<I>" ---------------------------------------- image_en_couleur()

"<o>" ---------------------------------------- image_en_contour()

"<O>" ---------------------------------------- image_en_contour()

"<p>" ---------------------------------------- maj_palette_de_couleur()

"<P>" ---------------------------------------- maj_palette_de_couleur()

"<q>" ---------------------------------------- augmenter_taille()

"<Q>" ---------------------------------------- augmenter_taille()

"<s>" ---------------------------------------- diminuer_taille()

"<S>" ---------------------------------------- diminuer_taille()

"<g>" ---------------------------------------- gomme()

"<G>" ---------------------------------------- gomme()

"<h>" ---------------------------------------- remplissage_rectangulaire()

"<H>" ---------------------------------------- remplissage_rectangulaire()

"<j>" ---------------------------------------- jaune()

"<J>" ---------------------------------------- jaune()

"<k>" ---------------------------------------- bleu()

"<K>" ---------------------------------------- bleu()

"<l>" ---------------------------------------- ligne()

"<L>" ---------------------------------------- ligne()

"<m>" ---------------------------------------- magenta()

"<M>" ---------------------------------------- magenta()

"<w>" ---------------------------------------- générer_le_fichier_Gcode()

"<W>" ---------------------------------------- générer_le_fichier_Gcode()

"<x>" ---------------------------------------- autre_couleur_choix()

"<X>" ---------------------------------------- autre_couleur_choix()

"<v>" ---------------------------------------- vert()

"<V>" ---------------------------------------- vert()

"<n>" ---------------------------------------- noir()

"<N>" ---------------------------------------- noir()

Flèche haut ---------------------------------- utiliser_couleur_palette_suivante()

Flèche bas ---------------------------------- utiliser_couleur_palette_précédente()

Gauche -------------------------------------- ajouter_couleur_à_la_palette()

Droite -------------------------------------- afficher_la_palette()
