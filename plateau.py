from cellule import Cellule, CELLULE_VIDE, TRIANGLE_HAUT_GAUCHE, TRIANGLE_HAUT_DROITE, TRIANGLE_BAS_DROITE, TRIANGLE_BAS_GAUCHE, CELLULE_PLEINE, COULEUR_TRANSPARENTE, COULEUR_BLANC, COULEUR_JAUNE, COULEUR_ROUGE, COULEUR_BLEU, COULEUR_NOIR, VERS_LA_DROITE, VERS_LA_GAUCHE, VERS_LE_BAS, VERS_LE_HAUT
from pierre import Pierre_precieuse, creation_lot_pierres
import random as rd
import matplotlib.pyplot as plt
import matplotlib.patches as patches

plt.style.use('dark_background')

# e. Aucune pierre ne doit être complètement caché par d'autres pierres.
#	 Autrement dit, il est possible pour chaque pierre, de la voir depuis au moins un bord du plateau.

# => Deux interprétations possibles :
#    1) SANS_REFLEXION : Pour chaque pierre, il y a au moins une entrée de laser pouvant la toucher directement (sans avoir été réfléchi).
#    2) AVEC_REFLEXION : Pour chaque pierre, il y a au moins une entrée de laser pouvant la toucher (directement ou via une réflexion, sur une autre pierre).

# La règle semble s'interpréter de la première manière.

REGLE_VISIBILITE_INTERPRETATION_SANS_REFLEXION = 0
REGLE_VISIBILITE_INTERPRETATION_AVEC_REFLEXION = 1

CHOIX_INTERPRETATION_REGLE_VISIBILITE = REGLE_VISIBILITE_INTERPRETATION_SANS_REFLEXION

class Plateau :
    def __init__(self, nb_lignes = 8, nb_colonnes = 10, avec_triangle_noir = False, avec_triangle_transparent = False) :
        self.nb_lignes = nb_lignes
        self.nb_colonnes = nb_colonnes
        
        self.grille = [ [Cellule() for i in range(self.nb_colonnes)] for j in range(self.nb_lignes) ]
        
        self.lot_pierres_precieuse = creation_lot_pierres(avec_triangle_noir, avec_triangle_transparent)
        
        self.entrees_disponibles_nombres = [str(i)    for i in range(1, self.nb_lignes + self.nb_colonnes + 1)]
        self.entrees_disponibles_lettres = [chr(64+i) for i in range(1, self.nb_lignes + self.nb_colonnes + 1)]
    
    def nettoyage_grille(self): 
        self.grille = [ [Cellule() for i in range(self.nb_colonnes)] for j in range(self.nb_lignes) ]
    
    def choix_aleatoire_configuration(self) :
        
        regle_e_respecte = False
        
        while not regle_e_respecte :
            
            self.nettoyage_grille()
            
            rd.shuffle(self.lot_pierres_precieuse)
            
            for pierre in self.lot_pierres_precieuse :
                
                ### Verification emplacement valide - Partie 1
                
                toutes_les_regles_respectes_partie_1 = False
                
                while not toutes_les_regles_respectes_partie_1 :
                    
                    # === Choix de la position de la pierre ===
                    
                    orientation = rd.randint(0, 3)
                    pierre.rotation_pierre_90_degres_sens_horaire(orientation)
                    
                    nb_lignes_pierre, nb_colonnes_pierre = pierre.dimensions()
                    
                    num_ligne_choisi   = rd.randint(0, self.nb_lignes   - nb_lignes_pierre  )
                    num_colonne_choisi = rd.randint(0, self.nb_colonnes - nb_colonnes_pierre)
                    
                    # === Verification des règles ===
                    
                    # Règle implicite n°1 : Les pièces ne doivent pas se superposer.
                    
                    regle_implicite_1 = True
                    
                    for i in range(nb_lignes_pierre) :
                        for j in range(nb_colonnes_pierre) :
                            regle_implicite_1 = regle_implicite_1 and self.grille[num_ligne_choisi + i][num_colonne_choisi + j].est_vide()
                    
                    # a. Pour chaque pierre, la face avec le motif grillagé doit être visible.
                    # => Règle vérifiée par construction du programme, il n'est pas possible de retourner une pierre sur sa face arrière.
                    
                    # b. Le motif grillagé de chaque pierre doit être aligné avec la grille présente sur le plateau.
                    # => Règle vérifiée par construction du programme, il n'est possible de tourner une pierre qu'en respectant cette règle (avec un angle multiple de 90°).
                    
                    # c. Les pierres peuvent toucher les bords du plateau, mais elles ne doivent pas sortir de la grille.
                    # => Règle vérifiée par les variables num_ligne_choisi et num_colonne_choisi, qui ne peuvent être choisi de manière à ce que la pierre sorte de la grille.
                    
                    # d. Les bords des pierres ne doivent pas directement se toucher.
                    #    En revanche, un coin peut toucher un coin ou le bord d'une autre pierre.
                    # => Pour les cellules VIDES : Ne fait pas parti de la pièce, donc aucune notion de bord
                    # => Si non                  : Les cellules extérieures adjacentes doivent soit vide, soit triangulaire orienté dans le bon sens.
                    
                    regle_d = True
                    
                    for i in range(nb_lignes_pierre) :
                        for j in range(nb_colonnes_pierre) :
                            if not pierre.groupe_de_cellules[i][j].est_vide() :
                                
                                # Analyse bord doit de la cellule
                                
                                if (num_colonne_choisi + j + 1 < self.nb_colonnes 
                                    and 
                                    pierre.groupe_de_cellules[i][j].etat in [CELLULE_PLEINE, 
                                                                            TRIANGLE_HAUT_DROITE, 
                                                                            TRIANGLE_BAS_DROITE
                                                                            ]
                                    ) :
                                    regle_d = (regle_d 
                                            and 
                                            self.grille[num_ligne_choisi + i][num_colonne_choisi + j + 1].etat not in [CELLULE_PLEINE, 
                                                                                                                        TRIANGLE_HAUT_GAUCHE, 
                                                                                                                        TRIANGLE_BAS_GAUCHE]
                                            )
                                    
                                # Analyse bord gauche de la cellule
                                
                                if (num_colonne_choisi + j - 1 >= 0 
                                    and 
                                    pierre.groupe_de_cellules[i][j].etat in [CELLULE_PLEINE, 
                                                                            TRIANGLE_HAUT_GAUCHE, 
                                                                            TRIANGLE_BAS_GAUCHE
                                                                            ]
                                    ) :
                                    regle_d = (regle_d 
                                            and 
                                            self.grille[num_ligne_choisi + i][num_colonne_choisi + j - 1].etat not in [CELLULE_PLEINE, 
                                                                                                                        TRIANGLE_HAUT_DROITE, 
                                                                                                                        TRIANGLE_BAS_DROITE]
                                            )
                                    
                                # Analyse bord inférieure de la cellule
                                
                                if (num_ligne_choisi + i + 1 < self.nb_lignes
                                    and 
                                    pierre.groupe_de_cellules[i][j].etat in [CELLULE_PLEINE, 
                                                                            TRIANGLE_BAS_GAUCHE, 
                                                                            TRIANGLE_BAS_DROITE
                                                                            ]
                                    ) :
                                    regle_d = (regle_d 
                                            and 
                                            self.grille[num_ligne_choisi + i + 1][num_colonne_choisi + j].etat not in [CELLULE_PLEINE, 
                                                                                                                        TRIANGLE_HAUT_GAUCHE,
                                                                                                                        TRIANGLE_HAUT_DROITE]
                                            )
                                    
                                if (num_ligne_choisi + i - 1 >= 0 
                                    and 
                                    pierre.groupe_de_cellules[i][j].etat in [CELLULE_PLEINE, 
                                                                            TRIANGLE_HAUT_GAUCHE, 
                                                                            TRIANGLE_HAUT_DROITE
                                                                            ]
                                    ) :
                                    regle_d = (regle_d 
                                            and 
                                            self.grille[num_ligne_choisi + i - 1][num_colonne_choisi + j].etat not in [CELLULE_PLEINE, 
                                                                                                                        TRIANGLE_BAS_GAUCHE,
                                                                                                                        TRIANGLE_BAS_DROITE]
                                            )
                    
                    toutes_les_regles_respectes_partie_1 = (regle_implicite_1 and regle_d)
                    
                ### Placement de la pierre ### (Tamponnement du plateau)
                
                for i in range(nb_lignes_pierre) :
                        for j in range(nb_colonnes_pierre) :
                            if not pierre.groupe_de_cellules[i][j].est_vide() :
                                self.grille[num_ligne_choisi + i][num_colonne_choisi + j].etat               = pierre.groupe_de_cellules[i][j].etat
                                self.grille[num_ligne_choisi + i][num_colonne_choisi + j].identifiant_pierre = pierre.identifiant_pierre
                                self.grille[num_ligne_choisi + i][num_colonne_choisi + j].couleur            = pierre.couleur_pierre
                
            # e. Aucune pierre ne doit être complètement caché par d'autres pierres.
            #	 Autrement dit, il est possible pour chaque pierre, de la voir depuis au moins un bord du plateau.
            
            # => Deux interprétations possibles :
            #    1) SANS_REFLEXION : Pour chaque pierre, il y a au moins une entrée de laser pouvant la toucher directement (sans avoir été réfléchi).
            #    2) AVEC_REFLEXION : Pour chaque pierre, il y a au moins une entrée de laser pouvant la toucher (directement ou via une réflexion, sur une autre pierre).
            
            # La règle semble s'interpréter de la première manière.
            
            # La vérification est faite à posteriori, lorsque toutes les pierres sont placées. 
            # Si cette règle n'est pas respectée, le plateau est refait depuis le début (Ce qui sera probablement très rare).
            
            if   CHOIX_INTERPRETATION_REGLE_VISIBILITE == REGLE_VISIBILITE_INTERPRETATION_SANS_REFLEXION :
                liste_pierres_vues = []
                
                # Observation depuis le bord supérieur du plateau
                
                for j in range(self.nb_colonnes) :
                    
                    vue_bloquee = False
                    
                    for i in range(self.nb_lignes) :
                        if not vue_bloquee and not self.grille[i][j].est_vide():
                            
                            vue_bloquee = True
                            
                            if self.grille[i][j].identifiant_pierre not in liste_pierres_vues :
                                liste_pierres_vues.append(self.grille[i][j].identifiant_pierre)
                
                # Observation depuis le bord inférieur du plateau
                
                for j in range(self.nb_colonnes) :
                    
                    vue_bloquee = False
                    
                    for i in range(self.nb_lignes-1, -1, -1) :
                        if not vue_bloquee and not self.grille[i][j].est_vide():
                                
                            vue_bloquee = True
                            
                            if self.grille[i][j].identifiant_pierre not in liste_pierres_vues :
                                liste_pierres_vues.append(self.grille[i][j].identifiant_pierre)
                
                # Observation depuis le bord gauche du plateau
                
                for i in range(self.nb_lignes) :
                    
                    vue_bloquee = False
                    
                    for j in range(self.nb_colonnes) :
                        if not vue_bloquee and not self.grille[i][j].est_vide():
                                
                            vue_bloquee = True
                            
                            if self.grille[i][j].identifiant_pierre not in liste_pierres_vues :
                                liste_pierres_vues.append(self.grille[i][j].identifiant_pierre)
                
                # Observation depuis le bord droit du plateau                
                
                for i in range(self.nb_lignes) :
                    
                    vue_bloquee = False
                    
                    for j in range(self.nb_colonnes-1, -1, -1) :
                        if not vue_bloquee and not self.grille[i][j].est_vide():
                                
                            vue_bloquee = True
                            
                            if self.grille[i][j].identifiant_pierre not in liste_pierres_vues :
                                liste_pierres_vues.append(self.grille[i][j].identifiant_pierre)
                
                regle_e_respecte = len(liste_pierres_vues) == len(self.lot_pierres_precieuse)
                
                
            elif CHOIX_INTERPRETATION_REGLE_VISIBILITE == REGLE_VISIBILITE_INTERPRETATION_AVEC_REFLEXION :
                # TODO
                
                regle_e_respecte = True
                pass

    def affichage_matrice_pierre(self) :
        for ligne in self.grille :
            for cellule in ligne :
                print(cellule, end = " ")
            print()
            
    def affichage_graph_matplotlib(self) :
        
        # Créer une figure et un axe
        fig, ax = plt.subplots(figsize=(self.nb_colonnes+1, self.nb_lignes+1))

        # Cacher les axes
        ax.axis('off')

        # Définir la taille de chaque cellule
        cell_size = 1
        
        # Fixer le rapport d'aspect pour éviter la déformation
        ax.set_aspect('equal', adjustable='box')

        # Ajouter des lignes de grille
        for i in range(self.nb_lignes + 1):
            # Ligne horizontale
            ax.plot([0, self.nb_colonnes * cell_size], [(self.nb_lignes - i) * cell_size, (self.nb_lignes - i) * cell_size], color='gray', linewidth=2)

        for j in range(self.nb_colonnes + 1):
            # Ligne verticale
            ax.plot([j * cell_size, j * cell_size], [0, self.nb_lignes * cell_size], color='gray', linewidth=2)

        # Dessiner les cellules de la grille
        for i in range(self.nb_lignes):
            for j in range(self.nb_colonnes):
                # Calculer la position de chaque cellule
                x = j * cell_size
                y = (self.nb_lignes - 1 - i) * cell_size

                ax.add_patch(self.grille[i][j].forme_geometrique_matplolib(x, y, cell_size))

        # Ajouter des étiquettes pour les colonnes (côté supérieur)
        for j in range(self.nb_colonnes):
            ax.text(j * cell_size + cell_size / 2, self.nb_lignes * cell_size + 0.2, str(j + 1), ha='center', va='center', color='white')

        # Ajouter des étiquettes pour les colonnes (côté droit)
        for i in range(self.nb_lignes):
            ax.text(self.nb_colonnes * cell_size + 0.2, (self.nb_lignes - 1 - i) * cell_size + cell_size / 2, str(self.nb_colonnes + i + 1), ha='center', va='center', color='white')

        # Ajouter des étiquettes pour les lignes (côté gauche)
        for i in range(self.nb_lignes):
            ax.text(-0.2, (self.nb_lignes - 1 - i) * cell_size + cell_size / 2, chr(65 + i), ha='center', va='center', color='white')

        # Ajouter des étiquettes pour les lignes (côté inférieur)
        for j in range(self.nb_colonnes):
            ax.text(j * cell_size + cell_size / 2, -0.2, chr(self.nb_lignes + 65 + j), ha='center', va='center', color='white')       

        # Ajuster les limites de l'axe
        ax.set_xlim(-0.5, self.nb_colonnes * cell_size + 0.5)
        ax.set_ylim(-0.5, self.nb_lignes * cell_size   + 0.5)

        plt.show()
        
    
    def tirer_laser(self, entree_laser_brute_valide) :
        
        index_ligne_colonne   = None
        ligne_selectionnee    = False
        sens_croissant_choisi = False
                
        ### Interprétation entrée
        
        if entree_laser_brute_valide in self.entrees_disponibles_nombres :
            if int(entree_laser_brute_valide)-1 < self.nb_colonnes :
                # Colonne en sens croissant (haut vers le bas)
                index_ligne_colonne   = int(entree_laser_brute_valide)-1
                ligne_selectionnee    = False
                sens_croissant_choisi = True
                
            else : 
                # Ligne en sens décroissant (droite vers la gauche)
                index_ligne_colonne   = int(entree_laser_brute_valide) - 1 - self.nb_colonnes
                ligne_selectionnee    = True
                sens_croissant_choisi = False
                
        else :
            code_ascii = ord(entree_laser_brute_valide)
            index_brute = code_ascii - 64 - 1
            
            if index_brute < self.nb_lignes :
                # Ligne en sens croissant (gauche vers la droite)
                index_ligne_colonne   = index_brute
                ligne_selectionnee    = True
                sens_croissant_choisi = True
                
            else :
                # Colonne en sens décroissant (bas vers le haut)
                index_ligne_colonne   = index_brute - self.nb_lignes
                ligne_selectionnee    = False
                sens_croissant_choisi = False
        
        ### Variable de départ
        
        if sens_croissant_choisi :
            i_ligne   = -1
            j_colonne = -1
        else :
            i_ligne   = self.nb_lignes
            j_colonne = self.nb_colonnes
        
        if ligne_selectionnee :
            i_ligne = index_ligne_colonne
        else :
            j_colonne = index_ligne_colonne
            
        if       sens_croissant_choisi and not ligne_selectionnee : direction_laser = VERS_LE_BAS
        elif not sens_croissant_choisi and not ligne_selectionnee : direction_laser = VERS_LE_HAUT
        elif     sens_croissant_choisi and     ligne_selectionnee : direction_laser = VERS_LA_DROITE
        elif not sens_croissant_choisi and     ligne_selectionnee : direction_laser = VERS_LA_GAUCHE
        
        ### Simulation du laser
        
        trajet_du_laser_terminee            = False
        
        liste_identifiants_pierres_touchees = []
        nombre_de_reflexions                = 0
        liste_couleurs_pierres_touchees     = []
        
        while not trajet_du_laser_terminee :
            
            if   direction_laser == VERS_LE_BAS    : i_ligne   += 1
            elif direction_laser == VERS_LE_HAUT   : i_ligne   -= 1
            elif direction_laser == VERS_LA_DROITE : j_colonne += 1
            elif direction_laser == VERS_LA_GAUCHE : j_colonne -= 1
            
            if (i_ligne   == -1               or 
                i_ligne   == self.nb_lignes   or
                j_colonne == -1               or
                j_colonne == self.nb_colonnes ):
                trajet_du_laser_terminee = True
            
            else :
                nouvelle_direction_laser = self.grille[i_ligne][j_colonne].reflexion(direction_laser)
                
                if direction_laser != nouvelle_direction_laser :
                    nombre_de_reflexions += 1
                    
                    if self.grille[i_ligne][j_colonne].identifiant_pierre not in liste_identifiants_pierres_touchees :
                        liste_identifiants_pierres_touchees.append(self.grille[i_ligne][j_colonne].identifiant_pierre)
                        
                    if self.grille[i_ligne][j_colonne].couleur            not in liste_couleurs_pierres_touchees :
                        liste_couleurs_pierres_touchees.append(self.grille[i_ligne][j_colonne].couleur)
                
                direction_laser = nouvelle_direction_laser
                
        ### Sortie du laser
        
        index_de_sortie_grille_nombre_lettre = ""
        
        if   i_ligne   == -1               : index_de_sortie_grille_nombre_lettre = str(j_colonne + 1)
        elif j_colonne == self.nb_colonnes : index_de_sortie_grille_nombre_lettre = str(i_ligne   + self.nb_colonnes + 1)
        elif j_colonne == -1               : index_de_sortie_grille_nombre_lettre = chr(64 + 1 + i_ligne)
        elif i_ligne   == self.nb_lignes   : index_de_sortie_grille_nombre_lettre = chr(64 + 1 + self.nb_lignes + j_colonne)
        
        if COULEUR_NOIR in liste_couleurs_pierres_touchees :
            print("Le laser ne ressort pas, il a probablement été absorbé par une pierre précieuse d'un noir profond...")
            
        else :
            print(f"Le laser sort en {index_de_sortie_grille_nombre_lettre}.")
            print(f"Il a été réfléchi {nombre_de_reflexions} fois sur des pierres précieuses.")
            
            if len(liste_identifiants_pierres_touchees) <= 1 : mot_pierre = "pierre"
            else                                             : mot_pierre = "pierres"
                
            print(f"Il a touché lors de ces réflexions {len(liste_identifiants_pierres_touchees)} {mot_pierre}.")
            
            if COULEUR_TRANSPARENTE in liste_couleurs_pierres_touchees :
                liste_couleurs_pierres_touchees.remove(COULEUR_TRANSPARENTE)
                
            if COULEUR_NOIR in liste_couleurs_pierres_touchees :
                liste_couleurs_pierres_touchees.remove(COULEUR_NOIR)
            
            if   len(liste_couleurs_pierres_touchees) == 0 : mot_couleur = None
            
            elif len(liste_couleurs_pierres_touchees) == 1 :
                if   COULEUR_BLANC         in liste_couleurs_pierres_touchees : mot_couleur = "Blanc"
                elif COULEUR_JAUNE         in liste_couleurs_pierres_touchees : mot_couleur = "Jaune"
                elif COULEUR_BLEU          in liste_couleurs_pierres_touchees : mot_couleur = "Bleu"
                elif COULEUR_ROUGE         in liste_couleurs_pierres_touchees : mot_couleur = "Rouge"
                
            elif len(liste_couleurs_pierres_touchees) == 2 :
                if   COULEUR_BLANC         in liste_couleurs_pierres_touchees :
                    if   COULEUR_JAUNE     in liste_couleurs_pierres_touchees : mot_couleur = "Beige"
                    elif COULEUR_BLEU      in liste_couleurs_pierres_touchees : mot_couleur = "Cyan"
                    elif COULEUR_ROUGE     in liste_couleurs_pierres_touchees : mot_couleur = "Rose"
                elif COULEUR_JAUNE         in liste_couleurs_pierres_touchees :
                    if   COULEUR_BLEU      in liste_couleurs_pierres_touchees : mot_couleur = "Vert"
                    elif COULEUR_ROUGE     in liste_couleurs_pierres_touchees : mot_couleur = "Orange"
                elif COULEUR_BLEU          in liste_couleurs_pierres_touchees :
                    if COULEUR_ROUGE       in liste_couleurs_pierres_touchees : mot_couleur = "Violet"
                else                                                          : mot_couleur = "ERREUR"
                
            elif len(liste_couleurs_pierres_touchees) == 3 :
                if   COULEUR_BLANC         in liste_couleurs_pierres_touchees :
                    if   COULEUR_JAUNE     in liste_couleurs_pierres_touchees : 
                        if COULEUR_BLEU    in liste_couleurs_pierres_touchees : mot_couleur = "Vert Clair"
                        elif COULEUR_ROUGE in liste_couleurs_pierres_touchees : mot_couleur = "Orange Clair"
                    elif COULEUR_BLEU      in liste_couleurs_pierres_touchees :
                        if COULEUR_ROUGE   in liste_couleurs_pierres_touchees : mot_couleur = "Violet Clair"
                elif COULEUR_JAUNE         in liste_couleurs_pierres_touchees :
                    if COULEUR_BLEU        in liste_couleurs_pierres_touchees :
                        if COULEUR_ROUGE   in liste_couleurs_pierres_touchees : mot_couleur = "Noir"
                else                                                          : mot_couleur = "ERREUR"
                
            elif len(liste_couleurs_pierres_touchees) == 4 : mot_couleur = "Gris"
            
            if mot_couleur == None :
                print(f"Le laser n'a aucune couleur.")
            else :
                print(f"Le laser resort en étant {mot_couleur}.")

if __name__ == "__main__" :

    plateau = Plateau(avec_triangle_noir=True, avec_triangle_transparent=True)
    plateau.choix_aleatoire_configuration()

    for i in plateau.entrees_disponibles_nombres :
        print()
        print()
        print(i)
        plateau.tirer_laser(str(i))

    for i in plateau.entrees_disponibles_lettres :
        print()
        print()
        print(i)
        plateau.tirer_laser(i)

    plateau.affichage_graph_matplotlib()