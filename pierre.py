from cellule import Cellule, CELLULE_VIDE, TRIANGLE_HAUT_GAUCHE, TRIANGLE_HAUT_DROITE, TRIANGLE_BAS_DROITE, TRIANGLE_BAS_GAUCHE, CELLULE_PLEINE, COULEUR_TRANSPARENTE, COULEUR_BLANC, COULEUR_JAUNE, COULEUR_ROUGE, COULEUR_BLEU, COULEUR_NOIR

class Pierre_precieuse :
    def __init__(self, forme_pierre, couleur_pierre, identifiant_pierre = 0) :
        self.rotation = 0
        
        self.groupe_de_cellules = []
        for ligne in forme_pierre :
            nouvelle_ligne = []
            for etat in ligne :
                nouvelle_ligne.append(Cellule(etat))
            self.groupe_de_cellules.append(nouvelle_ligne)
            
        self.couleur_pierre = couleur_pierre
        
        self.identifiant_pierre = identifiant_pierre
        
        self.attribution_cellules_pierre()
    
    def dimensions(self) :
        return (len(self.groupe_de_cellules), len(self.groupe_de_cellules[0]))

    def affichage_matrice_pierre(self) :
        for ligne in self.groupe_de_cellules :
            for cellule in ligne :
                print(cellule, end = " ")
            print()
    
    def attribution_cellules_pierre(self) :
        for i in range(len(self.groupe_de_cellules)) :
            for j in range(len(self.groupe_de_cellules[i])) :
                self.groupe_de_cellules[i][j].set_couleur(self.couleur_pierre)
                self.groupe_de_cellules[i][j].set_identifiant_pierre(self.identifiant_pierre)
    
    def rotation_pierre_90_degres_sens_horaire(self, nb_rotation = 1) :
        for _ in range(nb_rotation) :
            ### Mise à jour de la rotation
            self.rotation = (self.rotation + 90) % 360
            
            ### Recherche taille max de la forme de la pierre
            taille_max = max(len(self.groupe_de_cellules), len(self.groupe_de_cellules[0]))
            taille_min = min(len(self.groupe_de_cellules), len(self.groupe_de_cellules[0]))
            
            moins_de_colonnes_que_de_lignes = len(self.groupe_de_cellules[0]) < len(self.groupe_de_cellules)
            
            ### Ajout lignes ou colonnes pour obtenir une forme carrée
            forme_pierre_carree = list(self.groupe_de_cellules)
            
            if not (taille_max == 3  and  taille_min == 1):
                if moins_de_colonnes_que_de_lignes :
                    for i_ligne in range(len(forme_pierre_carree)) :
                        for i in range(taille_max - taille_min) :
                            forme_pierre_carree[i_ligne].append(Cellule())
                else :
                    for i in range(taille_max - taille_min) :
                        forme_pierre_carree.append([Cellule()]*(len(forme_pierre_carree[0])))
                    
            else :
                if moins_de_colonnes_que_de_lignes :
                    for i_ligne in range(len(forme_pierre_carree)) :
                        forme_pierre_carree[i_ligne] = [Cellule(), forme_pierre_carree[i_ligne][0], Cellule()]
                else :
                    forme_pierre_carree = [ [Cellule(), Cellule(), Cellule()],
                                            forme_pierre_carree[0]           ,
                                            [Cellule(), Cellule(), Cellule()]
                                          ]
                
            ### Déplacement des cellules de la pierre
                       
            # == Coins == #
            if taille_max >= 2 :
                tempo                                           = forme_pierre_carree[taille_max-1][0]
                forme_pierre_carree[taille_max-1][0]            = forme_pierre_carree[taille_max-1][taille_max-1]
                forme_pierre_carree[taille_max-1][taille_max-1] = forme_pierre_carree[0]           [taille_max-1]
                forme_pierre_carree[0]           [taille_max-1] = forme_pierre_carree[0][0]
                forme_pierre_carree[0]           [0]            = tempo
            
            if taille_max == 3 :
                tempo                                           = forme_pierre_carree[0][1]
                forme_pierre_carree[0][1]                       = forme_pierre_carree[1][0]
                forme_pierre_carree[1][0]                       = forme_pierre_carree[2][1]
                forme_pierre_carree[2][1]                       = forme_pierre_carree[1][2]
                forme_pierre_carree[1][2]                       = tempo
                
            if taille_max == 4 :
                # == Carré central == #
                tempo                                           = forme_pierre_carree[1][1]
                forme_pierre_carree[1][1]                       = forme_pierre_carree[2][1]
                forme_pierre_carree[2][1]                       = forme_pierre_carree[2][2]
                forme_pierre_carree[2][2]                       = forme_pierre_carree[1][2]
                forme_pierre_carree[1][2]                       = tempo
                
                # == Bords de gauche == #
                tempo                                           = forme_pierre_carree[0][1]
                forme_pierre_carree[0][1]                       = forme_pierre_carree[2][0]
                forme_pierre_carree[2][0]                       = forme_pierre_carree[3][2]
                forme_pierre_carree[3][2]                       = forme_pierre_carree[1][3]
                forme_pierre_carree[1][3]                       = tempo
                
                # == Bords de droite == #
                tempo                                           = forme_pierre_carree[1][0]
                forme_pierre_carree[1][0]                       = forme_pierre_carree[3][1]
                forme_pierre_carree[3][1]                       = forme_pierre_carree[2][3]
                forme_pierre_carree[2][3]                       = forme_pierre_carree[0][2]
                forme_pierre_carree[0][2]                       = tempo
            
            
            ### Rotation des cellules de la pierre
            for i_ligne in range(len(forme_pierre_carree)) :
                for j_colonne in range(len(forme_pierre_carree[0])) :
                    forme_pierre_carree[i_ligne][j_colonne].rotation_cellule_90_degres_sens_horaire()
            
    
            ### Suppression lignes vides
            indices_lignes_vides = [i_ligne
                                    for i_ligne in range(len(forme_pierre_carree))
                                    if all(cellule.est_vide() for cellule in forme_pierre_carree[i_ligne])
                                   ]
            
            nouvelle_forme_pierre = [forme_pierre_carree[i_ligne] 
                                     for i_ligne in range(len(forme_pierre_carree)) 
                                     if i_ligne not in indices_lignes_vides
                                    ]
                               
            
            ### Suppression colonnes vides
            indices_colonnes_vides = [j_colonne
                                      for j_colonne in range(len(nouvelle_forme_pierre[0]))
                                      if all(cellule.est_vide() for cellule in [nouvelle_forme_pierre[i_ligne][j_colonne] for i_ligne in range(len(nouvelle_forme_pierre))])
                                     ]
            
            nouvelle_forme_pierre_v2 = [ [nouvelle_forme_pierre[i_ligne][j_colonne] 
                                          for j_colonne in range(len(nouvelle_forme_pierre[0])) 
                                          if j_colonne not in indices_colonnes_vides
                                         ] 
                                         for i_ligne in range(len(nouvelle_forme_pierre)) 
                                       ]
            
            
            ### Mise à jour de la forme de la pierre
            self.groupe_de_cellules = nouvelle_forme_pierre_v2
            self.attribution_cellules_pierre()
            
            
            
forme_triangle_jaune = [[TRIANGLE_BAS_GAUCHE , CELLULE_VIDE                                                  ],
                        [CELLULE_PLEINE      , TRIANGLE_BAS_GAUCHE                                           ]]

forme_carree_bleu    = [[TRIANGLE_BAS_DROITE , TRIANGLE_BAS_GAUCHE                                           ],
                        [TRIANGLE_HAUT_DROITE, TRIANGLE_HAUT_GAUCHE                                          ]]

forme_piece_rouge    = [[TRIANGLE_HAUT_DROITE, CELLULE_PLEINE      , TRIANGLE_BAS_GAUCHE                     ]]


forme_triangle_blanc = [[CELLULE_VIDE        , TRIANGLE_BAS_DROITE , TRIANGLE_BAS_GAUCHE, CELLULE_VIDE       ],
                        [TRIANGLE_BAS_DROITE , CELLULE_PLEINE      , CELLULE_PLEINE     , TRIANGLE_BAS_GAUCHE]]

forme_petit_triangle = [[TRIANGLE_BAS_DROITE , TRIANGLE_BAS_GAUCHE                                           ]]


Triangle_jaune       = Pierre_precieuse(forme_triangle_jaune, COULEUR_JAUNE       )
Carree_bleu          = Pierre_precieuse(forme_carree_bleu   , COULEUR_BLEU        )
Piece_rouge          = Pierre_precieuse(forme_piece_rouge   , COULEUR_ROUGE       )
Triangle_blanc       = Pierre_precieuse(forme_triangle_blanc, COULEUR_BLANC       )
Triangle_noir        = Pierre_precieuse(forme_petit_triangle, COULEUR_NOIR        )
Triangle_transparent = Pierre_precieuse(forme_petit_triangle, COULEUR_TRANSPARENTE)

def creation_lot_pierres(avec_triangle_noir = False, avec_triangle_transparent = False) :
    lot = []
    lot.append(Pierre_precieuse(forme_triangle_blanc, COULEUR_BLANC, 1))
    lot.append(Pierre_precieuse(forme_triangle_blanc, COULEUR_BLANC, 2))
    lot.append(Pierre_precieuse(forme_triangle_jaune, COULEUR_JAUNE, 3))
    lot.append(Pierre_precieuse(forme_piece_rouge   , COULEUR_ROUGE, 4))
    lot.append(Pierre_precieuse(forme_carree_bleu   , COULEUR_BLEU , 5))
    
    if avec_triangle_noir :
        lot.append(Pierre_precieuse(forme_petit_triangle, COULEUR_NOIR, 6))
        
    if avec_triangle_transparent :
        lot.append(Pierre_precieuse(forme_petit_triangle, COULEUR_TRANSPARENTE, 7))
        
    return lot

if __name__ == "__main__" :
    test = Triangle_blanc
    test.affichage_matrice_pierre()
    test.rotation_pierre_90_degres_sens_horaire()
    print()
    test.affichage_matrice_pierre()
