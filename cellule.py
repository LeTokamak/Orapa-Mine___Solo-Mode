import matplotlib.patches as patches

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

COULEUR_HEXA_BLANC   = "#FFFFFF"
COULEUR_HEXA_TRANSPARENT = "#AAAAAA"
COULEUR_HEXA_JAUNE   = "#DDDD00"
COULEUR_HEXA_ROUGE   = "#AA0000"
COULEUR_HEXA_BLEU    = "#0000AA"
COULEUR_HEXA_NOIR    = "#000000"

class Cellule :
    def __init__(self, type_cellule = CELLULE_VIDE) :
        self.etat = type_cellule
        self.couleur = COULEUR_TRANSPARENTE
        self.identifiant_pierre = 0
    
    def __str__(self):
        if   self.etat == CELLULE_VIDE         : return " "
        elif self.etat == CELLULE_PLEINE       : return "■"
        elif self.etat == TRIANGLE_HAUT_GAUCHE : return "◤"
        elif self.etat == TRIANGLE_HAUT_DROITE : return "◥"
        elif self.etat == TRIANGLE_BAS_DROITE  : return "◢"
        elif self.etat == TRIANGLE_BAS_GAUCHE  : return "◣"

    def forme_geometrique_matplolib(self, x, y, cell_size):
        if   self.couleur == COULEUR_TRANSPARENTE : couleur = COULEUR_HEXA_TRANSPARENT
        elif self.couleur == COULEUR_BLANC        : couleur = COULEUR_HEXA_BLANC
        elif self.couleur == COULEUR_JAUNE        : couleur = COULEUR_HEXA_JAUNE
        elif self.couleur == COULEUR_ROUGE        : couleur = COULEUR_HEXA_ROUGE
        elif self.couleur == COULEUR_BLEU         : couleur = COULEUR_HEXA_BLEU
        elif self.couleur == COULEUR_NOIR         : couleur = COULEUR_HEXA_NOIR
        
        if   self.etat == CELLULE_VIDE         : return patches.Rectangle((x, y), cell_size, cell_size, linewidth=0                                           , facecolor="#000000FF", edgecolor='white')
        elif self.etat == CELLULE_PLEINE       : return patches.Rectangle((x, y), cell_size, cell_size, linewidth=0                                           , facecolor=couleur, edgecolor="#000000FF")
        elif self.etat == TRIANGLE_HAUT_GAUCHE : return patches.Polygon([(x, y), (x, y + cell_size), (x + cell_size, y + cell_size)]            , closed=True, linewidth=0, facecolor=couleur, edgecolor="#000000FF")
        elif self.etat == TRIANGLE_HAUT_DROITE : return patches.Polygon([(x, y + cell_size), (x + cell_size, y), (x + cell_size, y + cell_size)], closed=True, linewidth=0, facecolor=couleur, edgecolor="#000000FF")
        elif self.etat == TRIANGLE_BAS_DROITE  : return patches.Polygon([(x, y), (x + cell_size, y), (x + cell_size, y + cell_size)]            , closed=True, linewidth=0, facecolor=couleur, edgecolor="#FFFFFFFF")
        elif self.etat == TRIANGLE_BAS_GAUCHE  : return patches.Polygon([(x, y), (x + cell_size, y), (x, y + cell_size)]                        , closed=True, linewidth=0, facecolor=couleur, edgecolor="#000000FF")
    
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