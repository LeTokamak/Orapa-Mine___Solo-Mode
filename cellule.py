CELLULE_VIDE         = 0
TRIANGLE_HAUT_GAUCHE = 1
TRIANGLE_HAUT_DROITE = 2
TRIANGLE_BAS_DROITE  = 3
TRIANGLE_BAS_GAUCHE  = 4
CELLULE_PLEINE       = 5

COULEUR_TRANSPARENTE = 0
COULEUR_BLANC        = 1
COULEUR_JAUNE        = 2
COULEUR_ROUGE        = 3
COULEUR_BLEU         = 4
COULEUR_NOIR         = 5

class Cellule :
    def __init__(self, type_cellule = CELLULE_VIDE) :
        self.etat = type_cellule
        self.couleur = COULEUR_TRANSPARENTE
        self.identifiant_pierre = 0
        
    def est_vide(self) :
        return self.etat == CELLULE_VIDE
    
    def rotation_cellule_90_degres_sens_horaire(self) :
        if   self.etat == CELLULE_VIDE         : pass
        elif self.etat == CELLULE_PLEINE       : pass
        elif self.etat == TRIANGLE_HAUT_GAUCHE : self.etat = TRIANGLE_HAUT_DROITE
        elif self.etat == TRIANGLE_HAUT_DROITE : self.etat = TRIANGLE_BAS_DROITE
        elif self.etat == TRIANGLE_BAS_DROITE  : self.etat = TRIANGLE_BAS_GAUCHE
        elif self.etat == TRIANGLE_BAS_GAUCHE  : self.etat = TRIANGLE_HAUT_GAUCHE
        
    def set_couleur(self, couleur) :
        self.couleur = couleur
        
    def set_identifiant_pierre(self, identifiant_pierre) :
        if self.etat != CELLULE_VIDE : 
            self.identifiant_pierre = identifiant_pierre
        else :
            self.identifiant_pierre = 0