from cellule import Cellule, CELLULE_VIDE, TRIANGLE_HAUT_GAUCHE, TRIANGLE_HAUT_DROITE, TRIANGLE_BAS_DROITE, TRIANGLE_BAS_GAUCHE, CELLULE_PLEINE, COULEUR_TRANSPARENTE, COULEUR_BLANC, COULEUR_JAUNE, COULEUR_ROUGE, COULEUR_BLEU, COULEUR_NOIR
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
    
    def nettoyage_grille(self): 
        self.grille = [ [Cellule() for i in range(self.nb_colonnes)] for j in range(self.nb_lignes) ]
    
    def choix_aleatoire_configuration(self) :
        
        regle_e_respecte = False
        
        while not regle_e_respecte :
            
            self.nettoyage_grille()
            
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
        fig, ax = plt.subplots(figsize=(self.nb_colonnes, self.nb_lignes))

        # Cacher les axes
        ax.axis('off')

        # Définir la taille de chaque cellule
        cell_size = 1

        # Dessiner les cellules de la grille
        for i in range(self.nb_lignes):
            for j in range(self.nb_colonnes):
                # Calculer la position de chaque cellule
                x = j * cell_size
                y = (self.nb_lignes - 1 - i) * cell_size

                ax.add_patch(self.grille[i][j].forme_geometrique_matplolib(x, y, cell_size))
                    

        # Ajouter des étiquettes pour les colonnes
        col_labels = [chr(65 + i) for i in range(self.nb_colonnes)]
        for j, label in enumerate(col_labels):
            ax.text(j * cell_size + cell_size / 2, self.nb_lignes * cell_size + 0.2, label, ha='center', va='center')

        # Ajouter des étiquettes pour les lignes
        row_labels = [str(i + 1) for i in range(self.nb_lignes)]
        for i, label in enumerate(row_labels):
            ax.text(-0.2, (self.nb_lignes - 1 - i) * cell_size + cell_size / 2, label, ha='center', va='center')

        # Ajuster les limites de l'axe
        ax.set_xlim(0, self.nb_colonnes * cell_size)
        ax.set_ylim(0, self.nb_lignes * cell_size)

        plt.show()


            
            
plateau = Plateau()
plateau.choix_aleatoire_configuration()
plateau.affichage_matrice_pierre()

plateau.affichage_graph_matplotlib()