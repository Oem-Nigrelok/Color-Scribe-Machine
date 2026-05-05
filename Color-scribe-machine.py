# Importations
import tkinter as tk
from tkinter import simpledialog
import ast
from PIL import Image, ImageFilter


# Variables utilitaires (utilisées dans les global)
color = "black"

taille_du_crayon = 0
taille_de_la_gomme = 1

nombre_de_fichiers_générés = 0
activité = 0

entrée_texte_couleur = None

bouton_valider_le_choix_autre_couleur = None
bouton_gomme = None
bouton_ligne = None
bouton_rectangle = None
bouton_remplissage_rectangulaire = None

clic_x, clic_y = None, None
point_de_départ_x, point_de_départ_y = None, None

composants_actifs = [True, False, False, False, False]
# [dessin levé, gomme, ligne droite, rectangle, remplissage rectangulaire]
tracé = []
liste_des_tracés = []
liste_des_tracés_gcode = []

liste_de_couleurs_utilisables = []
liste_de_couleurs_utilisables_de_base = []
liste_de_couleurs_utilisables_ajoutées = []

identifiant_ligne_droite_temporaire = None
identifiant_rectangle_temporaire = None


# Fenêtre principale
fenêtre = tk.Tk()
fenêtre.withdraw()


# Mode config
mode_config_rapide = simpledialog.askstring("Mode config rapide","Voulez vous passez la configuration ? (0 pour non)")
if mode_config_rapide == "0":
    # Couleur fenêtre
    couleur_fenêtre = simpledialog.askstring("Couleur de la fenêtre","Tapez la couleur souhaité (0 pour blanc)")
    if couleur_fenêtre is None or couleur_fenêtre == "0":
        couleur_fenêtre = "#FFFFFF"


    # Taille fenêtre
    taille_de_la_feuille_choix = simpledialog.askstring("Taille", "Taille de la feuille (A3, A4, A5 ou 'LargeurxHauteur') :")
    if taille_de_la_feuille_choix == "max":
        taille_de_la_feuille_x = 230
        taille_de_la_feuille_y = 450
    elif taille_de_la_feuille_choix == "A4":
        taille_de_la_feuille_x = 210
        taille_de_la_feuille_y = 297
    elif taille_de_la_feuille_choix == "A5":
        taille_de_la_feuille_x = 148
        taille_de_la_feuille_y = 210
    else:
        try:
            taille_de_la_feuille_x, taille_de_la_feuille_y = map(int, taille_de_la_feuille_choix.split('x'))
        except Exception:
            try:
                taille_de_la_feuille_x, taille_de_la_feuille_y = map(int, taille_de_la_feuille_choix.split('*'))
            except Exception:
                try:
                    taille_de_la_feuille_x = int(taille_de_la_feuille_choix)
                    taille_de_la_feuille_y = int(simpledialog.askstring("Taille y", "taille de la feuille y : "))
                except Exception:
                    try:
                        taille_de_la_feuille_x = int(simpledialog.askstring("Taille x", "taille de la feuille x : "))
                        taille_de_la_feuille_y = int(simpledialog.askstring("Taille y", "taille de la feuille y : "))
                    except Exception:
                        taille_de_la_feuille_x = 210
                        taille_de_la_feuille_y = 297
    if taille_de_la_feuille_x > 230:
        taille_de_la_feuille_x = 230
        print("Taille de la feuille x ramenée à 230mm pour raison de limitation matérielle")
    if taille_de_la_feuille_y > 450:
        taille_de_la_feuille_y = 450
        print("Taille de la feuille y ramenée à 450mm pour raison de limitation matérielle")


    # Multiplicateur fenêtre
    taille_du_multiplicateur_choix = simpledialog.askstring("Multiplicateur", "Entrez le multiplicateur")
    try:
        taille_du_multiplicateur_choix = round(float(taille_du_multiplicateur_choix), 2)
    except Exception:
        taille_du_multiplicateur_choix = round(float(358 / taille_de_la_feuille_x), 2)
    if taille_du_multiplicateur_choix <= 0:
        taille_du_multiplicateur_choix = round(float(358 / taille_de_la_feuille_x), 2)
    print(f"Le multiplicateur est de {taille_du_multiplicateur_choix}. Si ce n'est pas celui que vous avez rentré, il est possible qu'il ai été adapté pour la taille de votre écran")
    taille_de_la_feuille_x *= taille_du_multiplicateur_choix
    taille_de_la_feuille_y *= taille_du_multiplicateur_choix
    
    
    # Réglages Gcode
    type_du_fichier_d_exportation = simpledialog.askstring("Type du fichier","Tapez 1 pour .txt, 2 pour .gcode")
    nom_du_fichier_d_exportation = simpledialog.askstring("Nom du fichier","Tapez le nom du fichier Gcode d'exportation")

    # Réglages Performances
    type_de_performance = simpledialog.askstring("Type du fichier","Tapez 1 pour graphique fast, 2 pour graphique précis")
    if type_de_performance == "1":
        type_de_performance = True
    else:
        type_de_performance = False


    # Création de la zone de dessin
    try:
        zone_de_dessin = tk.Canvas(fenêtre, bg = couleur_fenêtre, width = taille_de_la_feuille_x, height = taille_de_la_feuille_y)
    except Exception:
        zone_de_dessin = tk.Canvas(fenêtre, bg = "white", width = taille_de_la_feuille_x, height = taille_de_la_feuille_y)
    zone_de_dessin.place(x = 1, y = 1)
    
else:
    couleur_fenêtre = "#FFFFFF"
    taille_de_la_feuille_x = 210
    taille_de_la_feuille_y = 297
    taille_du_multiplicateur_choix = round(float(358 / taille_de_la_feuille_x), 2)
    taille_de_la_feuille_x *= taille_du_multiplicateur_choix
    taille_de_la_feuille_y *= taille_du_multiplicateur_choix
    type_du_fichier_d_exportation = None
    nom_du_fichier_d_exportation = None
    type_de_performance = False
    zone_de_dessin = tk.Canvas(fenêtre, bg = "white", width = taille_de_la_feuille_x, height = taille_de_la_feuille_y)
    zone_de_dessin.place(x = 1, y = 1)
    

# Affichage de la fenêtre
fenêtre.title("Interface de dessin")
fenêtre.deiconify()


# Protection pour ne pas dépasser de la feuille
def clip_to_zone_de_dessin(x, y):
    global taille_de_la_feuille_x, taille_de_la_feuille_y
    if x < 0:
        x = 0
    elif x > taille_de_la_feuille_x:
        x = round(taille_de_la_feuille_x)
    if y < 0:
        y = 0
    elif y > taille_de_la_feuille_y:
        y = round(taille_de_la_feuille_y)
    return x, y


# Bouton performance
def changement_de_type_de_performance():
    global type_de_performance, activité
    if activité == 1:
        return
    type_de_performance = not type_de_performance
    if type_de_performance == True:
        bouton_changement_de_type_de_performance.config(text = "Performance : Précis")
    else:
        bouton_changement_de_type_de_performance.config(text = "Performance : Fast")


# Couleurs
def noir():
    global color
    if activité == 1:
        return
    color = "#000000"
    
def bleu():
    global color
    if activité == 1:
        return
    color = "#0000ff"
    
def rouge():
    global color
    if activité == 1:
        return
    color = "#ff0000"
    
def vert():
    global color
    if activité == 1:
        return
    color = "#00ff00"
    
def cyan():
    global color
    if activité == 1:
        return
    color = "#00ffff"
    
def jaune():
    global color
    if activité == 1:
        return
    color = "#ffff00"
    
def magenta():
    global color
    if activité == 1:
        return
    color = "#ff00ff"
    
def autre_couleur_choix():
    global entrée_texte_couleur, bouton_valider_le_choix_autre_couleur
    if activité == 1:
        return
    if entrée_texte_couleur is not None:
        fermer_le_choix_autre_couleur()
        return
    entrée_texte_couleur = tk.Entry(fenêtre, bg = "lightgrey")
    bouton_valider_le_choix_autre_couleur = tk.Button(fenêtre, text = "ok", command = fermer_le_choix_autre_couleur)
    entrée_texte_couleur.place(x = taille_de_la_feuille_x + 110, y = 28)
    bouton_valider_le_choix_autre_couleur.place(x = taille_de_la_feuille_x + 87, y = 28)

def fermer_le_choix_autre_couleur():
    global color, entrée_texte_couleur, bouton_valider_le_choix_autre_couleur
    if activité == 1:
        return
    try:
        color = entrée_texte_couleur.get()
        entrée_texte_couleur.place_forget()
        bouton_valider_le_choix_autre_couleur.place_forget()
        entrée_texte_couleur = None
    except Exception:
        entrée_texte_couleur.place_forget()
        bouton_valider_le_choix_autre_couleur.place_forget()
        entrée_texte_couleur = None


# Mise à jour de la palette de couleur
def maj_palette_de_couleur():
    global liste_de_couleurs_utilisables_de_base, liste_de_couleurs_utilisables_ajoutées, liste_de_couleurs_utilisables
    if activité != 1:
        liste_de_couleurs_utilisables = []
        liste_de_couleurs_utilisables_de_base = []
        liste_de_couleurs_utilisables_ajoutées = []
        try:
            couleurs_disponibles = simpledialog.askstring("Couleurs disponibles", "Entrez : (r,g,b), (r,g,b)...")
            if couleurs_disponibles is None:
                return
            base = [tuple(c) for c in ast.literal_eval(f"[{couleurs_disponibles}]")]
            if set(base) == {(0, 0, 0), (255, 255, 255)}:
                liste_de_couleurs_utilisables_de_base = list(base)
                liste_de_couleurs_utilisables = list(base)
                return image_en_couleur_suite() 
            liste_de_couleurs_utilisables_de_base = [c for c in base if c != (0, 0, 0) and c != (255, 255, 255)]  
        except Exception:
            liste_de_couleurs_utilisables_de_base = [(0, 255, 255), (255, 255, 0), (255, 0, 255)]
        if not liste_de_couleurs_utilisables_de_base:
            liste_de_couleurs_utilisables_de_base = [(0, 255, 255), (255, 255, 0), (255, 0, 255)]   
        liste_de_couleurs_utilisables.extend(liste_de_couleurs_utilisables_de_base)
        for i in range(len(liste_de_couleurs_utilisables_de_base)):
            for j in range(i + 1, len(liste_de_couleurs_utilisables_de_base)):
                melange = (round((1 - ((1 - liste_de_couleurs_utilisables_de_base[i][0] / 255) + (1 - liste_de_couleurs_utilisables_de_base[j][0] / 255)) / 2) * 255), round((1 - ((1 - liste_de_couleurs_utilisables_de_base[i][1] / 255) + (1 - liste_de_couleurs_utilisables_de_base[j][1] / 255)) / 2) * 255), round((1 - ((1 - liste_de_couleurs_utilisables_de_base[i][2] / 255) + (1 - liste_de_couleurs_utilisables_de_base[j][2] / 255)) / 2) * 255))
                liste_de_couleurs_utilisables_ajoutées.append((melange, liste_de_couleurs_utilisables_de_base[i], liste_de_couleurs_utilisables_de_base[j])) 
                liste_de_couleurs_utilisables.append(melange)       
        liste_de_couleurs_utilisables_de_base.append((0, 0, 0))
        liste_de_couleurs_utilisables_de_base.append((255, 255, 255))
        liste_de_couleurs_utilisables.append((0, 0, 0))
        liste_de_couleurs_utilisables.append((255, 255, 255))
    print(liste_de_couleurs_utilisables_de_base)
    print(liste_de_couleurs_utilisables)
    print(liste_de_couleurs_utilisables_ajoutées)


# Taille du crayon
def rafraichir_taille_du_crayon(valeur_renvoyée_du_slideur):
    global taille_du_crayon
    if activité != 1:
        taille_du_crayon = int(valeur_renvoyée_du_slideur) - 1

    
# Gomme
def gomme():
    global composants_actifs
    if activité == 1:
        return
    if composants_actifs[1] == True:
        composants_actifs = [True, False, False, False, False]
        bouton_gomme.config(text = "Gomme OFF")
        bouton_ligne.config(text = "Ligne OFF")
        bouton_rectangle.config(text = "Rectangle OFF")
        bouton_remplissage_rectangulaire.config(text = "Remplissage rectangulaire OFF")
    else:
        composants_actifs = [False, True, False, False, False]
        bouton_gomme.config(text = "Gomme ON")
        bouton_ligne.config(text = "Ligne OFF")
        bouton_rectangle.config(text = "Rectangle OFF")
        bouton_remplissage_rectangulaire.config(text = "Remplissage rectangulaire OFF")


# Taille de la gomme
def rafraichir_taille_de_la_gomme(valeur_renvoyée_du_slideur):
    global taille_de_la_gomme
    if activité == 1:
        return
    taille_de_la_gomme = int(valeur_renvoyée_du_slideur)
    
    
# Augmenter les tailles de slideurs    
def augmenter_taille():
    global taille_de_la_gomme, taille_du_crayon, slideur_taille_de_la_gomme, slideur_taille_du_crayon, activité
    if activité == 1:
        return
    if taille_du_crayon + 1 <= 20:
        taille_du_crayon += 1
        slideur_taille_du_crayon.set(taille_du_crayon)
    if taille_de_la_gomme + 1 <= 20:
        taille_de_la_gomme += 1
        slideur_taille_de_la_gomme.set(taille_de_la_gomme)
        
        
# Diminuer les tailles de slideurs    
def diminuer_taille():
    global taille_de_la_gomme, taille_du_crayon, slideur_taille_de_la_gomme, slideur_taille_du_crayon
    if activité == 1:
        return
    if taille_du_crayon - 1 >= 0:
        taille_du_crayon -= 1
        slideur_taille_du_crayon.set(taille_du_crayon)
    if taille_de_la_gomme - 1 >= 1:
        taille_de_la_gomme -= 1
        slideur_taille_de_la_gomme.set(taille_de_la_gomme)
        
    
# Ligne
def ligne():
    global composants_actifs
    if activité == 1:
        return
    if composants_actifs[2] == True:
        composants_actifs = [True, False, False, False, False]
        bouton_gomme.config(text = "Gomme OFF")
        bouton_ligne.config(text = "Ligne OFF")
        bouton_rectangle.config(text = "Rectangle OFF")
        bouton_remplissage_rectangulaire.config(text = "Remplissage rectangulaire OFF")
    else:
        composants_actifs = [False, False, True, False, False]
        bouton_gomme.config(text = "Gomme OFF")
        bouton_ligne.config(text = "Ligne ON")
        bouton_rectangle.config(text = "Rectangle OFF")
        bouton_remplissage_rectangulaire.config(text = "Remplissage rectangulaire OFF")


# Rectangle
def rectangle():
    global composants_actifs
    if activité == 1:
        return
    if composants_actifs[3] == True:
        composants_actifs = [True, False, False, False, False]
        bouton_gomme.config(text = "Gomme OFF")
        bouton_ligne.config(text = "Ligne OFF")
        bouton_rectangle.config(text = "Rectangle OFF")
        bouton_remplissage_rectangulaire.config(text = "Remplissage rectangulaire OFF")
    else:
        composants_actifs = [False, False, False, True, False]
        bouton_gomme.config(text = "Gomme OFF")
        bouton_ligne.config(text = "Ligne OFF")
        bouton_rectangle.config(text = "Rectangle ON")
        bouton_remplissage_rectangulaire.config(text = "Remplissage rectangulaire OFF")


# Remplissage rectangulaire
def remplissage_rectangulaire():
    global composants_actifs
    if activité == 1:
        return
    if composants_actifs[4] == True:
        composants_actifs = [True, False, False, False, False]
        bouton_gomme.config(text = "Gomme OFF")
        bouton_ligne.config(text = "Ligne OFF")
        bouton_rectangle.config(text = "Rectangle OFF")
        bouton_remplissage_rectangulaire.config(text = "Remplissage rectangulaire OFF")
    else:
        composants_actifs = [False, False, False, False, True]
        bouton_gomme.config(text = "Gomme OFF")
        bouton_ligne.config(text = "Ligne OFF")
        bouton_rectangle.config(text = "Rectangle OFF")
        bouton_remplissage_rectangulaire.config(text = "Remplissage rectangulaire ON")
        
        
# Retour
def retour():
    global liste_des_tracés
    if liste_des_tracés == []:
        return
    for tracé in liste_des_tracés[len(liste_des_tracés) - 1][:]:
        zone_de_dessin.delete(tracé[0])
    liste_des_tracés.remove(liste_des_tracés[len(liste_des_tracés) - 1])


# Dessin
# Que faire quand on clique
def premier_point(event):
    global clic_x, clic_y, point_de_départ_x, point_de_départ_y, color, composants_actifs, tracé, liste_des_tracés, activité, identifiant_ligne_droite_temporaire, identifiant_rectangle_temporaire
    activité = 1
    try:
        zone_de_dessin.delete(identifiant_ligne_droite_temporaire)
        zone_de_dessin.delete(identifiant_rectangle_temporaire)
        clic_x, clic_y = clip_to_zone_de_dessin(event.x, event.y)
    except Exception:
        clic_x, clic_y = clip_to_zone_de_dessin(event.x, event.y)
    
    # Rajout si variation de la taille du stylo
    points = []
    if taille_du_crayon > 0 and composants_actifs[0] == True: 
        for (identifiant_tracé, points_tracé, couleur) in tracé[:]:
            if (clic_x - taille_du_crayon <= points_tracé[0][0] <= clic_x + taille_du_crayon and clic_y - taille_du_crayon <= points_tracé[0][1] <= clic_y + taille_du_crayon) and (clic_x - taille_du_crayon <= points_tracé[1][0] <= clic_x + taille_du_crayon and clic_y - taille_du_crayon <= points_tracé[1][1] <= clic_y + taille_du_crayon):
                tracé.remove((identifiant_tracé, points_tracé, couleur))
                zone_de_dessin.delete(identifiant_tracé)
        for liste in liste_des_tracés[:]:
            for (identifiant_tracé, points_tracé, couleur) in liste[:]:
                if (clic_x - taille_du_crayon <= points_tracé[0][0] <= clic_x + taille_du_crayon and clic_y - taille_du_crayon <= points_tracé[0][1] <= clic_y + taille_du_crayon) and (clic_x - taille_du_crayon <= points_tracé[1][0] <= clic_x + taille_du_crayon and clic_y - taille_du_crayon <= points_tracé[1][1] <= clic_y + taille_du_crayon):
                    liste_des_tracés.remove(liste)
                    liste.remove((identifiant_tracé, points_tracé, couleur))
                    zone_de_dessin.delete(identifiant_tracé)
                    if liste != []:
                        liste_des_tracés.append(liste)
        for delta_coté_x in range(2 * taille_du_crayon + 1):
            for delta_coté_y in range(2 * taille_du_crayon + 1):
                points.append((clip_to_zone_de_dessin(clic_x - taille_du_crayon + delta_coté_x, clic_y - taille_du_crayon + delta_coté_y), clip_to_zone_de_dessin(clic_x - taille_du_crayon + delta_coté_x + 1, clic_y - taille_du_crayon + delta_coté_y + 1)))
        for delta_points in points[:]:
            identifiant_de_la_ligne = zone_de_dessin.create_line(delta_points[0][0], delta_points[0][1], delta_points[1][0], delta_points[1][1], fill = color, width = 1)
            tracé.append((identifiant_de_la_ligne, delta_points, color))
    
    # Gomme
    elif composants_actifs[1] == True:
        for (identifiant_tracé, points_tracé, couleur) in tracé[:]:
            if (clic_x - taille_de_la_gomme <= points_tracé[0][0] <= clic_x + taille_de_la_gomme and clic_y - taille_de_la_gomme <= points_tracé[0][1] <= clic_y + taille_de_la_gomme) or (clic_x - taille_de_la_gomme <= points_tracé[1][0] <= clic_x + taille_de_la_gomme and clic_y - taille_de_la_gomme <= points_tracé[1][1] <= clic_y + taille_de_la_gomme):
                tracé.remove((identifiant_tracé, points_tracé, couleur))
                zone_de_dessin.delete(identifiant_tracé)
        for liste in liste_des_tracés[:]:
            for (identifiant_tracé, points_tracé, couleur) in liste:
                if (clic_x - taille_de_la_gomme <= points_tracé[0][0] <= clic_x + taille_de_la_gomme and clic_y - taille_de_la_gomme <= points_tracé[0][1] <= clic_y + taille_de_la_gomme) or (clic_x - taille_de_la_gomme <= points_tracé[1][0] <= clic_x + taille_de_la_gomme and clic_y - taille_de_la_gomme <= points_tracé[1][1] <= clic_y + taille_de_la_gomme):
                    liste_des_tracés.remove(liste)
                    liste.remove((identifiant_tracé, points_tracé, couleur))
                    zone_de_dessin.delete(identifiant_tracé)
                    if liste != []:
                        liste_des_tracés.append(liste)
                        
    # Ligne droite, Rectangle, Remplissage rectangulaire
    elif composants_actifs[2] == True or composants_actifs[3] == True or composants_actifs[4] == True:
        point_de_départ_x, point_de_départ_y = clic_x, clic_y
        
    
# Que faire quand on drag
def en_train_de_dessiner(event):
    global clic_x, clic_y, color, tracé, liste_des_tracés, taille_du_crayon, point_de_départ_x, point_de_départ_y, identifiant_ligne_droite_temporaire, identifiant_rectangle_temporaire, delta_x, delta_y, type_de_performance
    delta_x, delta_y = clip_to_zone_de_dessin(event.x, event.y)
    
    if composants_actifs[0] == True:
        # Cas sans variation de la taille du stylo
        if taille_du_crayon == 0:
            if (clic_x, clic_y) != (delta_x, delta_y):
                points = [(clic_x, clic_y), (delta_x, delta_y)]
                for (identifiant_tracé, points_tracé, couleur) in tracé[:]:
                    if points_tracé in points:
                        tracé.remove((identifiant_tracé, points_tracé, couleur))
                        zone_de_dessin.delete(identifiant_tracé)
                for liste in liste_des_tracés[:]:
                    for (identifiant_tracé, points_tracé, couleur) in liste[:]:
                        if points_tracé in points:
                            liste_des_tracés.remove(liste)
                            liste.remove((identifiant_tracé, points_tracé, couleur))
                            zone_de_dessin.delete(identifiant_tracé)
                            if liste != []:
                                liste_des_tracés.append(liste)
                identifiant_de_la_ligne = zone_de_dessin.create_line(clic_x, clic_y, delta_x, delta_y, fill = color, width = 1)
                tracé.append((identifiant_de_la_ligne, points, color))
        # Cas avec 
        elif type_de_performance == True:
            points = []
            for (identifiant_tracé, points_tracé, couleur) in tracé[:]:
                if (clic_x - taille_du_crayon <= points_tracé[0][0] <= clic_x + taille_du_crayon and clic_y - taille_du_crayon <= points_tracé[0][1] <= clic_y + taille_du_crayon) and (clic_x - taille_du_crayon <= points_tracé[1][0] <= clic_x + taille_du_crayon and clic_y - taille_du_crayon <= points_tracé[1][1] <= clic_y + taille_du_crayon):
                    tracé.remove((identifiant_tracé, points_tracé, couleur))
                    zone_de_dessin.delete(identifiant_tracé)
            for liste in liste_des_tracés[:]:
                for (identifiant_tracé, points_tracé, couleur) in liste[:]:
                    if (clic_x - taille_du_crayon <= points_tracé[0][0] <= clic_x + taille_du_crayon and clic_y - taille_du_crayon <= points_tracé[0][1] <= clic_y + taille_du_crayon) and (clic_x - taille_du_crayon <= points_tracé[1][0] <= clic_x + taille_du_crayon and clic_y - taille_du_crayon <= points_tracé[1][1] <= clic_y + taille_du_crayon):
                        liste_des_tracés.remove(liste)
                        liste.remove((identifiant_tracé, points_tracé, couleur))
                        zone_de_dessin.delete(identifiant_tracé)
                        if liste != []:
                            liste_des_tracés.append(liste)
            for delta_coté_x in range(2 * taille_du_crayon + 1):
                for delta_coté_y in range(2 * taille_du_crayon + 1):
                    points.append((clip_to_zone_de_dessin(clic_x - taille_du_crayon + delta_coté_x, clic_y - taille_du_crayon + delta_coté_y), clip_to_zone_de_dessin(clic_x - taille_du_crayon + delta_coté_x + 1, clic_y - taille_du_crayon + delta_coté_y + 1)))
            for delta_points in points[:]:
                identifiant_de_la_ligne = zone_de_dessin.create_line(delta_points[0][0], delta_points[0][1], delta_points[1][0], delta_points[1][1], fill = color, width = 1)
                tracé.append((identifiant_de_la_ligne, delta_points, color))
        elif type_de_performance == False:
            points = []
            for delta_coté_x in range(2 * taille_du_crayon): 
                points.append((clip_to_zone_de_dessin(clic_x - taille_du_crayon + delta_coté_x, clic_y + taille_du_crayon), clip_to_zone_de_dessin(clic_x - taille_du_crayon + delta_coté_x - 1, clic_y + taille_du_crayon)))
            for delta_coté_y in range(2 * taille_du_crayon):
                points.append((clip_to_zone_de_dessin(clic_x + taille_du_crayon, clic_y + taille_du_crayon - delta_coté_y), clip_to_zone_de_dessin(clic_x + taille_du_crayon, clic_y + taille_du_crayon - delta_coté_y - 1)))
            for delta_coté_x in range(2 * taille_du_crayon): 
                points.append((clip_to_zone_de_dessin(clic_x + taille_du_crayon - delta_coté_x, clic_y - taille_du_crayon), clip_to_zone_de_dessin(clic_x + taille_du_crayon - delta_coté_x - 1, clic_y - taille_du_crayon)))
            for delta_coté_y in range(2 * taille_du_crayon):
                points.append((clip_to_zone_de_dessin(clic_x - taille_du_crayon, clic_y - taille_du_crayon + delta_coté_y), clip_to_zone_de_dessin(clic_x - taille_du_crayon, clic_y - taille_du_crayon + delta_coté_y - 1)))
            for (identifiant_tracé, points_tracé, couleur) in tracé[:]:
                if (clic_x - taille_du_crayon <= points_tracé[0][0] <= clic_x + taille_du_crayon and clic_y - taille_du_crayon <= points_tracé[0][1] <= clic_y + taille_du_crayon) and (clic_x - taille_du_crayon <= points_tracé[1][0] <= clic_x + taille_du_crayon and clic_y - taille_du_crayon <= points_tracé[1][1] <= clic_y + taille_du_crayon):
                    tracé.remove((identifiant_tracé, points_tracé, couleur))
                    zone_de_dessin.delete(identifiant_tracé)
            for liste in liste_des_tracés[:]:
                for (identifiant_tracé, points_tracé, couleur) in liste[:]:
                    if (clic_x - taille_du_crayon <= points_tracé[0][0] <= clic_x + taille_du_crayon and clic_y - taille_du_crayon <= points_tracé[0][1] <= clic_y + taille_du_crayon) and (clic_x - taille_du_crayon <= points_tracé[1][0] <= clic_x + taille_du_crayon and clic_y - taille_du_crayon <= points_tracé[1][1] <= clic_y + taille_du_crayon):
                        liste_des_tracés.remove(liste)
                        liste.remove((identifiant_tracé, points_tracé, couleur))
                        zone_de_dessin.delete(identifiant_tracé)
                        if liste != []:
                            liste_des_tracés.append(liste)
            for delta_points in points[:]:
                identifiant_de_la_ligne = zone_de_dessin.create_line(delta_points[0][0], delta_points[0][1], delta_points[1][0], delta_points[1][1], fill = color, width = 1)
                tracé.append((identifiant_de_la_ligne, delta_points, color))
                     
    # Gomme            
    elif composants_actifs[1] == True:
        for (identifiant_tracé, points_tracé, couleur) in tracé[:]:
            if (clic_x - taille_de_la_gomme <= points_tracé[0][0] <= clic_x + taille_de_la_gomme and clic_y - taille_de_la_gomme <= points_tracé[0][1] <= clic_y + taille_de_la_gomme) or (clic_x - taille_de_la_gomme <= points_tracé[1][0] <= clic_x + taille_de_la_gomme and clic_y - taille_de_la_gomme <= points_tracé[1][1] <= clic_y + taille_de_la_gomme):
                tracé.remove((identifiant_tracé, points_tracé, couleur))
                zone_de_dessin.delete(identifiant_tracé)
        for liste in liste_des_tracés[:]:
            for (identifiant_tracé, points_tracé, couleur) in liste[:]:
                if (clic_x - taille_de_la_gomme <= points_tracé[0][0] <= clic_x + taille_de_la_gomme and clic_y - taille_de_la_gomme <= points_tracé[0][1] <= clic_y + taille_de_la_gomme) or (clic_x - taille_de_la_gomme <= points_tracé[1][0] <= clic_x + taille_de_la_gomme and clic_y - taille_de_la_gomme <= points_tracé[1][1] <= clic_y + taille_de_la_gomme):
                    liste_des_tracés.remove(liste)
                    liste.remove((identifiant_tracé, points_tracé, couleur))
                    zone_de_dessin.delete(identifiant_tracé)
                    if liste != []:
                        liste_des_tracés.append(liste)
                        
    # Ligne droite
    elif composants_actifs[2] == True:
        zone_de_dessin.delete(identifiant_ligne_droite_temporaire)
        identifiant_ligne_droite_temporaire = zone_de_dessin.create_line(point_de_départ_x, point_de_départ_y, delta_x, delta_y, fill = color, width = 2 * (taille_du_crayon + 1), dash = (1,1))
        
        
    # Rectangle, Remplissage rectangulaire
    elif composants_actifs[3] == True or composants_actifs[4] == True:
        zone_de_dessin.delete(identifiant_rectangle_temporaire)
        identifiant_rectangle_temporaire = zone_de_dessin.create_rectangle(point_de_départ_x, point_de_départ_y, delta_x, delta_y, outline = color, width = 1, dash = (1,1))
        
    clic_x, clic_y = clip_to_zone_de_dessin(event.x, event.y)
    

# Que faire quand on arrête de cliquer
def stop_dessiner(event):
    global point_de_départ_x, color, point_de_départ_y, tracé, liste_des_tracés, taille_du_crayon, composants_actifs, identifiant_ligne_droite_temporaire, identifiant_rectangle_temporaire, activité
    clic_x, clic_y = clip_to_zone_de_dessin(event.x, event.y)
    
    # Rajout si variation de la taille du stylo
    points = []
    if taille_du_crayon > 0 and composants_actifs[0] == True: 
        for (identifiant_tracé, points_tracé, couleur) in tracé[:]:
            if (clic_x - taille_du_crayon <= points_tracé[0][0] <= clic_x + taille_du_crayon and clic_y - taille_du_crayon <= points_tracé[0][1] <= clic_y + taille_du_crayon) and (clic_x - taille_du_crayon <= points_tracé[1][0] <= clic_x + taille_du_crayon and clic_y - taille_du_crayon <= points_tracé[1][1] <= clic_y + taille_du_crayon):
                tracé.remove((identifiant_tracé, points_tracé, couleur))
                zone_de_dessin.delete(identifiant_tracé)
        for liste in liste_des_tracés[:]:
            for (identifiant_tracé, points_tracé, couleur) in liste[:]:
                if (clic_x - taille_du_crayon <= points_tracé[0][0] <= clic_x + taille_du_crayon and clic_y - taille_du_crayon <= points_tracé[0][1] <= clic_y + taille_du_crayon) and (clic_x - taille_du_crayon <= points_tracé[1][0] <= clic_x + taille_du_crayon and clic_y - taille_du_crayon <= points_tracé[1][1] <= clic_y + taille_du_crayon):
                    liste_des_tracés.remove(liste)
                    liste.remove((identifiant_tracé, points_tracé, couleur))
                    zone_de_dessin.delete(identifiant_tracé)
                    if liste != []:
                        liste_des_tracés.append(liste)
        for delta_coté_x in range(2 * taille_du_crayon + 1):
            for delta_coté_y in range(2 * taille_du_crayon + 1):
                points.append((clip_to_zone_de_dessin(clic_x - taille_du_crayon + delta_coté_x, clic_y - taille_du_crayon + delta_coté_y), clip_to_zone_de_dessin(clic_x - taille_du_crayon + delta_coté_x + 1, clic_y - taille_du_crayon + delta_coté_y + 1)))
        for delta_points in points[:]:
            identifiant_de_la_ligne = zone_de_dessin.create_line(delta_points[0][0], delta_points[0][1], delta_points[1][0], delta_points[1][1], fill = color, width = 1)
            tracé.append((identifiant_de_la_ligne, delta_points, color))
    
    # Ligne droite
    elif composants_actifs[2] == True and clip_to_zone_de_dessin(clic_x - point_de_départ_x, clic_y - point_de_départ_y) != (0, 0):
        # Cas sans variation de la taille du stylo
        if taille_du_crayon == 0:
            zone_de_dessin.delete(identifiant_ligne_droite_temporaire)
            points = []
            for delta_points in range(max(abs(clic_x - point_de_départ_x), abs(clic_y - point_de_départ_y))):
                points.append((clip_to_zone_de_dessin(point_de_départ_x + ((clic_x - point_de_départ_x) * delta_points / max(abs(clic_x - point_de_départ_x), abs(clic_y - point_de_départ_y))), point_de_départ_y + ((clic_y - point_de_départ_y) * delta_points / max(abs(clic_x - point_de_départ_x), abs(clic_y - point_de_départ_y)))), clip_to_zone_de_dessin(point_de_départ_x + ((clic_x - point_de_départ_x) * (delta_points + 1) / max(abs(clic_x - point_de_départ_x), abs(clic_y - point_de_départ_y))), point_de_départ_y + ((clic_y - point_de_départ_y) * (delta_points + 1) / max(abs(clic_x - point_de_départ_x), abs(clic_y - point_de_départ_y))))))
            for (identifiant_tracé, points_tracé, couleur) in tracé[:]:
                if points_tracé in points:
                    tracé.remove((identifiant_tracé, points_tracé, couleur))
                    zone_de_dessin.delete(identifiant_tracé)
            for liste in liste_des_tracés[:]:
                for (identifiant_tracé, points_tracé, couleur) in liste[:]:
                    if points_tracé in points:
                        liste_des_tracés.remove(liste)
                        liste.remove((identifiant_tracé, points_tracé, couleur))
                        zone_de_dessin.delete(identifiant_tracé)
                        if liste != []:
                            liste_des_tracés.append(liste)
            for delta_points in points:
                id_ligne = zone_de_dessin.create_line(delta_points[0][0], delta_points[0][1], delta_points[1][0], delta_points[1][1], fill = color, width = 1)
                tracé.append((id_ligne, delta_points, color))
        # Cas avec
        else:
            zone_de_dessin.delete(identifiant_ligne_droite_temporaire)
            points_de_construction = []
            points = []
            for delta_points in range(max(abs(clic_x - point_de_départ_x), abs(clic_y - point_de_départ_y))):
                points_de_construction.append((clip_to_zone_de_dessin(point_de_départ_x + ((clic_x - point_de_départ_x) * delta_points / max(abs(clic_x - point_de_départ_x), abs(clic_y - point_de_départ_y))), point_de_départ_y + ((clic_y - point_de_départ_y) * delta_points / max(abs(clic_x - point_de_départ_x), abs(clic_y - point_de_départ_y)))), clip_to_zone_de_dessin(point_de_départ_x + ((clic_x - point_de_départ_x) * (delta_points + 1) / max(abs(clic_x - point_de_départ_x), abs(clic_y - point_de_départ_y))), point_de_départ_y + ((clic_y - point_de_départ_y) * (delta_points + 1) / max(abs(clic_x - point_de_départ_x), abs(clic_y - point_de_départ_y))))))
            for position_1, position_2 in points_de_construction:
                for delta_coté_x in range(2 * taille_du_crayon): 
                    points.append((clip_to_zone_de_dessin(position_1[0] - taille_du_crayon + delta_coté_x, position_1[1] + taille_du_crayon), clip_to_zone_de_dessin(position_2[0] - taille_du_crayon + delta_coté_x - 1, position_2[1] + taille_du_crayon)))
                for delta_coté_y in range(2 * taille_du_crayon):
                    points.append((clip_to_zone_de_dessin(position_1[0] + taille_du_crayon, position_1[1] + taille_du_crayon - delta_coté_y), clip_to_zone_de_dessin(position_2[0] + taille_du_crayon, position_2[1] + taille_du_crayon - delta_coté_y - 1)))
                for delta_coté_x in range(2 * taille_du_crayon): 
                    points.append((clip_to_zone_de_dessin(position_1[0] + taille_du_crayon - delta_coté_x, position_1[1] - taille_du_crayon), clip_to_zone_de_dessin(position_2[0] + taille_du_crayon - delta_coté_x - 1, position_2[1] - taille_du_crayon)))
                for delta_coté_y in range(2 * taille_du_crayon):
                    points.append((clip_to_zone_de_dessin(position_1[0] - taille_du_crayon, position_1[1] - taille_du_crayon + delta_coté_y), clip_to_zone_de_dessin(position_2[0] - taille_du_crayon, position_2[1] - taille_du_crayon + delta_coté_y - 1)))
                for (identifiant_tracé, points_tracé, couleur) in tracé[:]:
                    if (position_1[0] - taille_du_crayon <= points_tracé[0][0] <= position_1[0] + taille_du_crayon and position_1[1] - taille_du_crayon <= points_tracé[0][1] <= position_1[1] + taille_du_crayon) and (position_2[0] - taille_du_crayon <= points_tracé[1][0] <= position_2[0] + taille_du_crayon and position_2[1] - taille_du_crayon <= points_tracé[1][1] <= position_2[1] + taille_du_crayon):
                        tracé.remove((identifiant_tracé, points_tracé, couleur))
                        zone_de_dessin.delete(identifiant_tracé)
                for liste in liste_des_tracés[:]:
                    for (identifiant_tracé, points_tracé, couleur) in liste[:]:
                        if (position_1[0] - taille_du_crayon <= points_tracé[0][0] <= position_1[0] + taille_du_crayon and position_1[1] - taille_du_crayon <= points_tracé[0][1] <= position_1[1] + taille_du_crayon) and (position_2[0] - taille_du_crayon <= points_tracé[1][0] <= position_2[0] + taille_du_crayon and position_2[1] - taille_du_crayon <= points_tracé[1][1] <= position_2[1] + taille_du_crayon):
                            liste_des_tracés.remove(liste)
                            liste.remove((identifiant_tracé, points_tracé, couleur))
                            zone_de_dessin.delete(identifiant_tracé)
                            if liste != []:
                                liste_des_tracés.append(liste)
            for (identifiant_tracé, points_tracé, couleur) in tracé[:]:
                if (position_1[0] - taille_du_crayon <= points_tracé[0][0] <= position_1[0] + taille_du_crayon and position_1[1] - taille_du_crayon <= points_tracé[0][1] <= position_1[1] + taille_du_crayon) and (position_2[0] - taille_du_crayon <= points_tracé[1][0] <= position_2[0] + taille_du_crayon and position_2[1] - taille_du_crayon <= points_tracé[1][1] <= position_2[1] + taille_du_crayon):
                    tracé.remove((identifiant_tracé, points_tracé, couleur))
                    zone_de_dessin.delete(identifiant_tracé)
            for liste in liste_des_tracés[:]:
                for (identifiant_tracé, points_tracé, couleur) in liste[:]:
                    if (position_1[0] - taille_du_crayon <= points_tracé[0][0] <= position_1[0] + taille_du_crayon and position_1[1] - taille_du_crayon <= points_tracé[0][1] <= position_1[1] + taille_du_crayon) and (position_2[0] - taille_du_crayon <= points_tracé[1][0] <= position_2[0] + taille_du_crayon and position_2[1] - taille_du_crayon <= points_tracé[1][1] <= position_2[1] + taille_du_crayon):
                        liste_des_tracés.remove(liste)
                        liste.remove((identifiant_tracé, points_tracé, couleur))
                        zone_de_dessin.delete(identifiant_tracé)
                        if liste != []:
                            liste_des_tracés.append(liste)
            for delta_coté_x in range(2 * taille_du_crayon + 1):
                for delta_coté_y in range(2 * taille_du_crayon + 1):
                    points.append((clip_to_zone_de_dessin(points_de_construction[0][0][0] - taille_du_crayon + delta_coté_x, points_de_construction[0][0][1] - taille_du_crayon + delta_coté_y), clip_to_zone_de_dessin(points_de_construction[0][1][0] - taille_du_crayon + delta_coté_x + 1, points_de_construction[0][1][1] - taille_du_crayon + delta_coté_y + 1)))
            for delta_points in points:
                id_ligne = zone_de_dessin.create_line(delta_points[0][0], delta_points[0][1], delta_points[1][0], delta_points[1][1], fill = color, width = 1)
                tracé.append((id_ligne, delta_points, color))
                
    # Rectangle
    elif composants_actifs[3] == True and clip_to_zone_de_dessin(clic_x - point_de_départ_x, clic_y - point_de_départ_y) != (0, 0):
        zone_de_dessin.delete(identifiant_rectangle_temporaire)
        points = []
        for delta_coté_x in range(abs(clic_x - point_de_départ_x)):
            if clic_x - point_de_départ_x < 0:
                points.append((clip_to_zone_de_dessin(point_de_départ_x - delta_coté_x, clic_y), clip_to_zone_de_dessin(point_de_départ_x - delta_coté_x - 1, clic_y)))
            else:
                points.append((clip_to_zone_de_dessin(point_de_départ_x + delta_coté_x, clic_y), clip_to_zone_de_dessin(point_de_départ_x + delta_coté_x - 1, clic_y)))
        for delta_coté_y in range(abs(clic_y - point_de_départ_y)):
            if clic_y - point_de_départ_y < 0:
                points.append((clip_to_zone_de_dessin(clic_x, clic_y + delta_coté_y), clip_to_zone_de_dessin(clic_x, clic_y + delta_coté_y - 1)))
            else:
                points.append((clip_to_zone_de_dessin(clic_x, clic_y - delta_coté_y), clip_to_zone_de_dessin(clic_x, clic_y - delta_coté_y - 1)))
        for delta_coté_x in range(abs(clic_x - point_de_départ_x)):
            if clic_x - point_de_départ_x < 0:
                points.append((clip_to_zone_de_dessin(clic_x + delta_coté_x, point_de_départ_y), clip_to_zone_de_dessin(clic_x + delta_coté_x - 1, point_de_départ_y)))
            else:
                points.append((clip_to_zone_de_dessin(clic_x - delta_coté_x, point_de_départ_y), clip_to_zone_de_dessin(clic_x - delta_coté_x - 1, point_de_départ_y)))
        for delta_coté_y in range(abs(clic_y - point_de_départ_y)):
            if clic_y - point_de_départ_y < 0:
                points.append((clip_to_zone_de_dessin(point_de_départ_x, point_de_départ_y - delta_coté_y), clip_to_zone_de_dessin(point_de_départ_x, point_de_départ_y - delta_coté_y - 1)))
            else:
                points.append((clip_to_zone_de_dessin(point_de_départ_x, point_de_départ_y + delta_coté_y), clip_to_zone_de_dessin(point_de_départ_x, point_de_départ_y + delta_coté_y - 1)))
        for (identifiant_tracé, points_tracé, couleur) in tracé[:]:
            if points_tracé in points:
                tracé.remove((identifiant_tracé, points_tracé, couleur))
                zone_de_dessin.delete(identifiant_tracé)
        for liste in liste_des_tracés[:]:
            for (identifiant_tracé, points_tracé, couleur) in liste[:]:
                if points_tracé in points:
                    liste_des_tracés.remove(liste)
                    liste.remove((identifiant_tracé, points_tracé, couleur))
                    zone_de_dessin.delete(identifiant_tracé)
                    if liste != []:
                        liste_des_tracés.append(liste)
        for delta_points in points[:]:
            identifiant_de_la_ligne = zone_de_dessin.create_line(delta_points[0][0], delta_points[0][1], delta_points[1][0], delta_points[1][1], fill = color, width = 1)
            tracé.append((identifiant_de_la_ligne, delta_points, color))
            
    # Remplissage rectangulaire
    elif composants_actifs[4] == True and clip_to_zone_de_dessin(clic_x - point_de_départ_x, clic_y - point_de_départ_y) != (0, 0):
        zone_de_dessin.delete(identifiant_rectangle_temporaire)
        points = []
        for delta_coté_x in range(abs(clic_x - point_de_départ_x)):
            for delta_coté_y in range(abs(clic_y - point_de_départ_y)):
                if clic_x - point_de_départ_x > 0 and clic_y - point_de_départ_y > 0:
                    points.append((clip_to_zone_de_dessin(clic_x - delta_coté_x, clic_y - delta_coté_y), clip_to_zone_de_dessin(clic_x - delta_coté_x - 1, clic_y - delta_coté_y - 1)))
                elif clic_x - point_de_départ_x > 0 and clic_y - point_de_départ_y < 0:
                    points.append((clip_to_zone_de_dessin(clic_x - delta_coté_x, clic_y + delta_coté_y), clip_to_zone_de_dessin(clic_x - delta_coté_x - 1, clic_y + delta_coté_y + 1)))
                elif clic_x - point_de_départ_x < 0 and clic_y - point_de_départ_y > 0:
                    points.append((clip_to_zone_de_dessin(clic_x + delta_coté_x, clic_y - delta_coté_y), clip_to_zone_de_dessin(clic_x + delta_coté_x + 1, clic_y - delta_coté_y - 1)))
                else:
                    points.append((clip_to_zone_de_dessin(clic_x + delta_coté_x, clic_y + delta_coté_y), clip_to_zone_de_dessin(clic_x + delta_coté_x + 1, clic_y + delta_coté_y + 1)))
        for (identifiant_tracé, points_tracé, couleur) in tracé[:]:
            if points_tracé in points:
                tracé.remove((identifiant_tracé, points_tracé, couleur))
                zone_de_dessin.delete(identifiant_tracé)
        for liste in liste_des_tracés[:]:
            for (identifiant_tracé, points_tracé, couleur) in liste[:]:
                if points_tracé in points:
                    liste_des_tracés.remove(liste)
                    liste.remove((identifiant_tracé, points_tracé, couleur))
                    zone_de_dessin.delete(identifiant_tracé)
                    if liste != []:
                        liste_des_tracés.append(liste)
        for delta_points in points[:]:
            identifiant_de_la_ligne = zone_de_dessin.create_line(delta_points[0][0], delta_points[0][1], delta_points[1][0], delta_points[1][1], fill = color, width = 1)
            tracé.append((identifiant_de_la_ligne, delta_points, color))
    
    if composants_actifs[1] != True and len(tracé) != 0:
        liste_des_tracés.append(tracé)
    tracé = []
    activité = 0
    points_de_construction = []
    points = []
    

# Image en couleur
def image_en_couleur():
    global liste_de_couleurs_utilisables_de_base, liste_de_couleurs_utilisables_ajoutées, liste_de_couleurs_utilisables
    if not liste_de_couleurs_utilisables_de_base:
        liste_de_couleurs_utilisables = []
        liste_de_couleurs_utilisables_de_base = []
        liste_de_couleurs_utilisables_ajoutées = []
        try:
            couleurs_disponibles = simpledialog.askstring("Couleurs disponibles", "Entrez : (r,g,b), (r,g,b)...")
            if couleurs_disponibles is None:
                return
            base = [tuple(c) for c in ast.literal_eval(f"[{couleurs_disponibles}]")]
            if set(base) == {(0, 0, 0), (255, 255, 255)}:
                liste_de_couleurs_utilisables_de_base = list(base)
                liste_de_couleurs_utilisables = list(base)
                return image_en_couleur_suite() 
            liste_de_couleurs_utilisables_de_base = [c for c in base if c != (0, 0, 0) and c != (255, 255, 255)]  
        except Exception:
            liste_de_couleurs_utilisables_de_base = [(0, 255, 255), (255, 255, 0), (255, 0, 255)]
        if not liste_de_couleurs_utilisables_de_base:
            liste_de_couleurs_utilisables_de_base = [(0, 255, 255), (255, 255, 0), (255, 0, 255)]   
        liste_de_couleurs_utilisables.extend(liste_de_couleurs_utilisables_de_base)
        for i in range(len(liste_de_couleurs_utilisables_de_base)):
            for j in range(i + 1, len(liste_de_couleurs_utilisables_de_base)):
                melange = (round((1 - ((1 - liste_de_couleurs_utilisables_de_base[i][0] / 255) + (1 - liste_de_couleurs_utilisables_de_base[j][0] / 255)) / 2) * 255), round((1 - ((1 - liste_de_couleurs_utilisables_de_base[i][1] / 255) + (1 - liste_de_couleurs_utilisables_de_base[j][1] / 255)) / 2) * 255), round((1 - ((1 - liste_de_couleurs_utilisables_de_base[i][2] / 255) + (1 - liste_de_couleurs_utilisables_de_base[j][2] / 255)) / 2) * 255))
                liste_de_couleurs_utilisables_ajoutées.append((melange, liste_de_couleurs_utilisables_de_base[i], liste_de_couleurs_utilisables_de_base[j])) 
                liste_de_couleurs_utilisables.append(melange)       
        liste_de_couleurs_utilisables_de_base.append((0, 0, 0))
        liste_de_couleurs_utilisables_de_base.append((255, 255, 255))
        liste_de_couleurs_utilisables.append((0, 0, 0))
        liste_de_couleurs_utilisables.append((255, 255, 255))
    print(liste_de_couleurs_utilisables_de_base)
    print(liste_de_couleurs_utilisables)
    print(liste_de_couleurs_utilisables_ajoutées)
    image_en_couleur_suite()
    
    
def image_en_couleur_suite():
    global liste_des_tracés, taille_de_la_feuille_x, taille_de_la_feuille_y
    fichier = simpledialog.askstring("Fichier image","Tapez le fichier image de référence")
    try:
        img_de_base = Image.open(fichier).convert('RGB')
    except Exception as e:
            print(f"Erreur lors de l'ouverture du fichier : {e}")
            return
    if img_de_base.size[0] > img_de_base.size[1]:
        img_de_base = img_de_base.rotate(90, expand = 1, fillcolor='white')
    img_de_base.thumbnail((taille_de_la_feuille_x - 2, taille_de_la_feuille_y - 2))
    img = Image.new('RGB', (img_de_base.size))
    for x in range(img_de_base.size[0]):
        for y in range(img_de_base.size[1]):
            pixel = img_de_base.getpixel((x, y))
            résultat_de_la_variance = (1000000, None)
            for couleur in liste_de_couleurs_utilisables:
                dist = sum((p - c) ** 2 for p, c in zip(pixel, couleur))
                if dist < résultat_de_la_variance[0]:
                    résultat_de_la_variance = [dist, couleur]
            img.putpixel((x, y), résultat_de_la_variance[1])
    for liste in liste_des_tracés[:]:
        for (identifiant_tracé, points_tracé, couleur) in liste[:]:
            zone_de_dessin.delete(identifiant_tracé)
    tracé = []
    liste_des_tracés = []
    for x in range(img.size[0]):
        for y in range(img.size[1]):
            pixel = img.getpixel((x, y))
            if pixel != (255, 255, 255):
                identifiant_de_la_ligne = zone_de_dessin.create_line(x + 1, y + 1, x + 2, y + 1, fill='#%02x%02x%02x' % pixel, width=1)
                tracé.append((identifiant_de_la_ligne, [(x + 1, y + 1), (x + 2, y + 1)], '#%02x%02x%02x' % pixel))
            try:
                pixel_suivant = img.getpixel((x + 1, y))
            except Exception:
                pixel_suivant = None
                if pixel_suivant != pixel:
                    if tracé:
                        liste_des_tracés.append(tracé)
                        tracé = []
            else:
                if tracé:
                    liste_des_tracés.append(tracé)
                    tracé = []
        if tracé:
            liste_des_tracés.append(tracé)
            tracé = []
            
# Image en contour
def image_en_contour():
    global liste_des_tracés, taille_de_la_feuille_x, taille_de_la_feuille_y
    fichier = simpledialog.askstring("Fichier image","Tapez le fichier image de référence")
    try:   
        img = Image.open(fichier).convert("RGB")
    except Exception as e:
            print(f"Erreur lors de l'ouverture du fichier : {e}")
            return
    if img.size[0] > img.size[1]:
        img = img.rotate(90, expand = 1, fillcolor='white')
    img.thumbnail((taille_de_la_feuille_x - 2, taille_de_la_feuille_y - 2))
    img = img.quantize(colors = 8, method = 1).convert("RGB")
    img = img.convert("L")
    img = img.filter(ImageFilter.FIND_EDGES)
    img = img.point(lambda x: 0 if x > 40 else 255)
    img = img.convert("RGB")
    for liste in liste_des_tracés[:]:
        for (identifiant_tracé, points_tracé, couleur) in liste[:]:
            zone_de_dessin.delete(identifiant_tracé)
    tracé = []
    liste_des_tracés = []
    for x in range(img.size[0]):
        for y in range(img.size[1]):
            pixel = img.getpixel((x, y))
            if pixel[0] <= 0:
                identifiant_de_la_ligne = zone_de_dessin.create_line(x + 1, y + 1, x + 2, y + 1, fill = '#%02x%02x%02x' % pixel, width = 1)
                tracé.append((identifiant_de_la_ligne, [(x + 1, y + 1), (x + 2, y + 1)], '#%02x%02x%02x' % pixel))
            else:
                if tracé != []:
                    liste_des_tracés.append(tracé)
                    tracé = []
        if tracé != []:
            liste_des_tracés.append(tracé)
            tracé = []
            
    
# Exportation en Gcode
def générer_le_fichier_Gcode():
    global type_du_fichier_d_exportation, activité, nom_du_fichier_d_exportation, liste_des_tracés_gcode, nombre_de_fichiers_générés, taille_de_la_feuille_x, taille_de_la_feuille_y, liste_des_tracés
    if activité == 1 or len(liste_des_tracés) == 0:
        return
    activité == 1
    liste_des_couleurs = []
    for tracé in liste_des_tracés[:]:
        for (mélange, couleur_1, couleur_2) in liste_de_couleurs_utilisables_ajoutées:
            if tuple(int(tracé[0][2].lstrip('#')[i : i + 2], 16) for i in (0, 2, 4)) == mélange:
                tracé_1 = []
                tracé_2 = []
                for (identifiant_tracé, points_tracé, couleur) in tracé:
                    tracé_1.append((identifiant_tracé, points_tracé, '#%02x%02x%02x' % couleur_1))
                    tracé_2.append((identifiant_tracé, points_tracé, '#%02x%02x%02x' % couleur_2))
                liste_des_tracés.remove(tracé)
                liste_des_tracés.append(tracé_1)
                liste_des_tracés.append(tracé_2)
    for tracé in liste_des_tracés:
        if tracé[0][2] not in liste_des_couleurs:
            liste_des_couleurs.append(tracé[0][2])
    liste_des_tracés_gcode = []
    for tracé in liste_des_tracés:
        nouveau_liste_tracé = []
        for (identifiant_tracé, points_tracé, couleur) in tracé:
            points = [(points_tracé[0][0], points_tracé[0][1]), (points_tracé[1][0], points_tracé[1][1])]
            nouveau_liste_tracé.append((identifiant_tracé, points, couleur))
        liste_des_tracés_gcode.append(nouveau_liste_tracé)
    liste_des_tracés = liste_des_tracés_gcode
    liste_des_tracés_gcode = []
    if type_de_performance != "1":
        fusionné = [False] * len(liste_des_tracés)
        for i, tracé_1 in enumerate(liste_des_tracés):
            if fusionné[i]:
                continue
            tracé_courant = tracé_1[:]
            ajout_trouvé = True
            while ajout_trouvé:
                ajout_trouvé = False
                for j, tracé_2 in enumerate(liste_des_tracés):
                    if i == j or fusionné[j]:
                        continue
                    fin = tracé_courant[-1][1][1]
                    début = tracé_2[0][1][0]
                    fin_2 = tracé_2[-1][1][1]
                    if abs(fin[0] - début[0]) <= 1 and abs(fin[1] - début[1]) <= 1 and tracé_courant[0][2] == tracé_2[0][2]:
                        tracé_courant += tracé_2
                        fusionné[j] = True
                        ajout_trouvé = True
                        break
                    elif abs(fin[0] - fin_2[0]) <= 1 and abs(fin[1] - fin_2[1]) <= 1 and tracé_courant[0][2] == tracé_2[0][2]:
                        tracé_courant += tracé_2[::-1]
                        fusionné[j] = True
                        ajout_trouvé = True
                        break
            liste_des_tracés_gcode.append(tracé_courant)
        liste_des_tracés = liste_des_tracés_gcode
        liste_des_tracés_gcode = []
    for tracé in liste_des_tracés:
        nouveau_liste_tracé = []
        répetition = 0
        while répetition < len(tracé):
            rang_départ = répetition
            if abs(tracé[répetition][1][0][0] - tracé[répetition][1][1][0]) == 1 and tracé[répetition][1][0][1] == tracé[répetition][1][1][1]:
                while (répetition < len(tracé) and abs(tracé[répetition][1][0][0] - tracé[répetition][1][1][0]) == 1 and tracé[répetition][1][0][1] == tracé[répetition][1][1][1] and (répetition == rang_départ or tracé[répetition][1][0] == tracé[répetition - 1][1][1])):
                    répetition += 1
                nouveau_liste_tracé.append(((tracé[rang_départ][1][0], tracé[répetition - 1][1][1]), tracé[rang_départ][2]))
            elif tracé[répetition][1][0][0] == tracé[répetition][1][1][0] and abs(tracé[répetition][1][0][1] - tracé[répetition][1][1][1]) == 1:
                while (répetition < len(tracé) and tracé[répetition][1][0][0] == tracé[répetition][1][1][0] and abs(tracé[répetition][1][0][1] - tracé[répetition][1][1][1]) == 1 and (répetition == rang_départ or tracé[répetition][1][0] == tracé[répetition - 1][1][1])):
                    répetition += 1
                nouveau_liste_tracé.append(((tracé[rang_départ][1][0], tracé[répetition - 1][1][1]),tracé[rang_départ][2]))
            else:
                nouveau_liste_tracé.append(((tracé[rang_départ][1][0], tracé[rang_départ][1][1]), tracé[rang_départ][2]))
                répetition += 1
        liste_des_tracés_gcode.append(nouveau_liste_tracé)          
    if len(nom_du_fichier_d_exportation) != 0:
        nom_base = nom_du_fichier_d_exportation
    else:
        nom_base = "export"
    if type_du_fichier_d_exportation == str(1):
        extension = ".txt"
    else:
        extension = ".gcode"
    for couleur in liste_des_couleurs:
        nom_du_fichier = f"{nom_base}({couleur})({nombre_de_fichiers_générés}){extension}"
        try:
            with open(nom_du_fichier, "w") as f:
                f.write("G21\n")
                f.write("G0 X0 Y0 Z10\n")
                f.write("G90\n")
                for tracé in liste_des_tracés_gcode:            
                    if tracé[0][1] == couleur:
                        f.write(f"G0 X{round(tracé[0][0][0][0] / taille_du_multiplicateur_choix, 2)} Y{round(tracé[0][0][0][1] / taille_du_multiplicateur_choix, 2)}\n")
                        f.write("G0 Z0\n")
                        for élément in tracé:
                            f.write(f"G0 X{round(élément[0][1][0] / taille_du_multiplicateur_choix, 2)} Y{round(élément[0][1][1] / taille_du_multiplicateur_choix, 2)}\n")
                        f.write("G0 Z10\n")
                f.write("G0 X0 Y0 Z0\n")
        except Exception as e:
            print(f"Erreur lors de l'écriture du fichier : {e}")
            return
        print("Fichier GCODE exporté sous :", nom_du_fichier)
    nombre_de_fichiers_générés += 1
    liste_des_tracés_gcode = []
    activité == 0
    
    
# Boutons utilitaires
tk.Button(fenêtre, text = "Noir", command = noir).place(x = taille_de_la_feuille_x + 99, y = 2)
tk.Button(fenêtre, text = "Bleu", command = bleu).place(x = taille_de_la_feuille_x + 133, y = 2)
tk.Button(fenêtre, text = "Vert", command = vert).place(x = taille_de_la_feuille_x + 167, y = 2)
tk.Button(fenêtre, text = "Rouge", command = rouge).place(x = taille_de_la_feuille_x + 2, y = 28)
tk.Button(fenêtre, text = "Cyan", command = cyan).place(x = taille_de_la_feuille_x + 199, y = 2)
tk.Button(fenêtre, text = "Jaune", command = jaune).place(x = taille_de_la_feuille_x + 237, y = 2)
tk.Button(fenêtre, text = "Magenta", command = magenta).place(x = taille_de_la_feuille_x + 278, y = 2)
tk.Button(fenêtre, text = "Autre", command = autre_couleur_choix).place(x = taille_de_la_feuille_x + 47, y = 28)
tk.Button(fenêtre, text = "Exporter GCODE", command = générer_le_fichier_Gcode).place(x = taille_de_la_feuille_x + 2, y = 2)
tk.Button(fenêtre, text = "⮐", command = retour).place(x = taille_de_la_feuille_x + 182, y = 54)
tk.Button(fenêtre, text = "Transformer image en couleur imprimables", command = image_en_couleur).place(x = taille_de_la_feuille_x + 2, y = 184)
tk.Button(fenêtre, text = "Transformer image en contour", command = image_en_contour).place(x = taille_de_la_feuille_x + 2, y = 210)
tk.Button(fenêtre, text = "Mise à jour de la palette de couleur", command = maj_palette_de_couleur).place(x = taille_de_la_feuille_x + 2, y = 236)


# Boutons utilitaires changeants
bouton_gomme = tk.Button(fenêtre, text = "Gomme OFF", command = gomme)
bouton_gomme.place(x = taille_de_la_feuille_x + 205, y = 54)
bouton_ligne = tk.Button(fenêtre, text = "Ligne OFF", command = ligne)
bouton_ligne.place(x = taille_de_la_feuille_x + 182, y = 80)
bouton_rectangle = tk.Button(fenêtre, text = "Rectangle OFF", command = rectangle)
bouton_rectangle.place(x = taille_de_la_feuille_x + 182, y = 106)
bouton_remplissage_rectangulaire = tk.Button(fenêtre, text = "Remplissage rectangulaire OFF", command = remplissage_rectangulaire)
bouton_remplissage_rectangulaire.place(x = taille_de_la_feuille_x + 182, y = 132)
if type_de_performance == "1":
    bouton_changement_de_type_de_performance = tk.Button(fenêtre, text = "Performance : Fast", command = changement_de_type_de_performance)
    bouton_changement_de_type_de_performance.place(x = taille_de_la_feuille_x + 2, y = 158)
else:
    bouton_changement_de_type_de_performance = tk.Button(fenêtre, text = "Performance : Précis", command = changement_de_type_de_performance)
    bouton_changement_de_type_de_performance.place(x = taille_de_la_feuille_x + 2, y = 158)


# Slideurs
slideur_taille_du_crayon = tk.Scale(fenêtre, from_ = 1, to = 20, orient = "vertical", label = "Crayon", command = rafraichir_taille_du_crayon)
slideur_taille_du_crayon.place(x = taille_de_la_feuille_x + 2, y = 54)
slideur_taille_de_la_gomme = tk.Scale(fenêtre, from_ = 1, to = 20, orient = "vertical", label = "Gomme", command = rafraichir_taille_de_la_gomme)
slideur_taille_de_la_gomme.place(x = taille_de_la_feuille_x + 87, y = 54)
slideur_taille_de_la_gomme.set(5)


# Racourcis claviers
fenêtre.bind("<z>", lambda event : retour())
fenêtre.bind("<Z>", lambda event : retour())
fenêtre.bind("<r>", lambda event : rouge())
fenêtre.bind("<R>", lambda event : rouge())
fenêtre.bind("<t>", lambda event : rectangle())
fenêtre.bind("<T>", lambda event : rectangle())
fenêtre.bind("<y>", lambda event : cyan())
fenêtre.bind("<Y>", lambda event : cyan())
fenêtre.bind("<u>", lambda event : changement_de_type_de_performance())
fenêtre.bind("<U>", lambda event : changement_de_type_de_performance())
fenêtre.bind("<i>", lambda event : image_en_couleur())
fenêtre.bind("<I>", lambda event : image_en_couleur())
fenêtre.bind("<o>", lambda event : image_en_contour())
fenêtre.bind("<O>", lambda event : image_en_contour())
fenêtre.bind("<p>", lambda event : maj_palette_de_couleur())
fenêtre.bind("<P>", lambda event : maj_palette_de_couleur())
fenêtre.bind("<q>", lambda event : augmenter_taille())
fenêtre.bind("<Q>", lambda event : augmenter_taille())
fenêtre.bind("<s>", lambda event : diminuer_taille())
fenêtre.bind("<S>", lambda event : diminuer_taille())
fenêtre.bind("<g>", lambda event : gomme())
fenêtre.bind("<G>", lambda event : gomme())
fenêtre.bind("<h>", lambda event : remplissage_rectangulaire())
fenêtre.bind("<H>", lambda event : remplissage_rectangulaire())
fenêtre.bind("<j>", lambda event : jaune())
fenêtre.bind("<J>", lambda event : jaune())
fenêtre.bind("<k>", lambda event : bleu())
fenêtre.bind("<K>", lambda event : bleu())
fenêtre.bind("<l>", lambda event : ligne())
fenêtre.bind("<L>", lambda event : ligne())
fenêtre.bind("<m>", lambda event : magenta())
fenêtre.bind("<M>", lambda event : magenta())
fenêtre.bind("<w>", lambda event : générer_le_fichier_Gcode())
fenêtre.bind("<W>", lambda event : générer_le_fichier_Gcode())
fenêtre.bind("<x>", lambda event : autre_couleur_choix())
fenêtre.bind("<X>", lambda event : autre_couleur_choix())
fenêtre.bind("<v>", lambda event : vert())
fenêtre.bind("<V>", lambda event : vert())
fenêtre.bind("<n>", lambda event : noir())
fenêtre.bind("<N>", lambda event : noir())


# Bind du dessin
zone_de_dessin.bind("<Button-1>", premier_point)
zone_de_dessin.bind("<B1-Motion>", en_train_de_dessiner)
zone_de_dessin.bind("<ButtonRelease-1>", stop_dessiner)


# Affichage continu des modifications
fenêtre.mainloop()