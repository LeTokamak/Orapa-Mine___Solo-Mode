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

COULEUR_HEXA_BLANC        = "#DDDDDD"
COULEUR_HEXA_ROUGE        = "#EC2A2A"
COULEUR_HEXA_JAUNE        = "#FCB73B"
COULEUR_HEXA_BLEU         = "#0E71B5"
COULEUR_HEXA_NOIR         = "#454644"

COULEUR_HEXA_ROSE         = "#F59495"
COULEUR_HEXA_BEIGE        = "#F4E2A7"
COULEUR_HEXA_CYAN         = "#90D1F7"

COULEUR_HEXA_ORANGE       = "#F27932"
COULEUR_HEXA_VIOLET       = "#95378E"
COULEUR_HEXA_VERT         = "#7BBD55"

COULEUR_HEXA_ORANGE_CLAIR = "#F7A77F"
COULEUR_HEXA_VIOLET_CLAIR = "#B16EAB"
COULEUR_HEXA_VERT_CLAIR   = "#CEE07A"

COULEUR_HEXA_GRIS         = "#636365"

VERS_LE_BAS    = 0
VERS_LA_DROITE = 1
VERS_LE_HAUT   = 2
VERS_LA_GAUCHE = 3

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
        if   self.etat == CELLULE_VIDE : 
            return patches.Rectangle((x, y), cell_size, cell_size, linewidth=0, facecolor="none" , edgecolor="none")
        
        if   self.couleur != COULEUR_TRANSPARENTE : 
            if   self.couleur == COULEUR_BLANC        : couleur = COULEUR_HEXA_BLANC
            elif self.couleur == COULEUR_JAUNE        : couleur = COULEUR_HEXA_JAUNE
            elif self.couleur == COULEUR_ROUGE        : couleur = COULEUR_HEXA_ROUGE
            elif self.couleur == COULEUR_BLEU         : couleur = COULEUR_HEXA_BLEU
            elif self.couleur == COULEUR_NOIR         : couleur = COULEUR_HEXA_NOIR
            
            if   self.etat == CELLULE_PLEINE       : return patches.Rectangle((x, y), cell_size, cell_size                                          , facecolor=couleur)
            elif self.etat == TRIANGLE_HAUT_GAUCHE : return patches.Polygon([(x, y), (x, y + cell_size), (x + cell_size, y + cell_size)]            , facecolor=couleur)
            elif self.etat == TRIANGLE_HAUT_DROITE : return patches.Polygon([(x, y + cell_size), (x + cell_size, y), (x + cell_size, y + cell_size)], facecolor=couleur)
            elif self.etat == TRIANGLE_BAS_DROITE  : return patches.Polygon([(x, y), (x + cell_size, y), (x + cell_size, y + cell_size)]            , facecolor=couleur)
            elif self.etat == TRIANGLE_BAS_GAUCHE  : return patches.Polygon([(x, y), (x + cell_size, y), (x, y + cell_size)]                        , facecolor=couleur)

        else :
            epaisseur_ligne = 1
            motif_hachure   = '/+\\x'
            if   self.etat == CELLULE_PLEINE       : return patches.Rectangle((x, y), cell_size, cell_size                                          , closed=True, linewidth=epaisseur_ligne, facecolor="none" , edgecolor="lightgray", hatch=motif_hachure)
            elif self.etat == TRIANGLE_HAUT_GAUCHE : return patches.Polygon([(x, y), (x, y + cell_size), (x + cell_size, y + cell_size)]            , closed=True, linewidth=epaisseur_ligne, facecolor="none" , edgecolor="lightgray", hatch=motif_hachure)
            elif self.etat == TRIANGLE_HAUT_DROITE : return patches.Polygon([(x, y + cell_size), (x + cell_size, y), (x + cell_size, y + cell_size)], closed=True, linewidth=epaisseur_ligne, facecolor="none" , edgecolor="lightgray", hatch=motif_hachure)
            elif self.etat == TRIANGLE_BAS_DROITE  : return patches.Polygon([(x, y), (x + cell_size, y), (x + cell_size, y + cell_size)]            , closed=True, linewidth=epaisseur_ligne, facecolor="none" , edgecolor="lightgray", hatch=motif_hachure)
            elif self.etat == TRIANGLE_BAS_GAUCHE  : return patches.Polygon([(x, y), (x + cell_size, y), (x, y + cell_size)]                        , closed=True, linewidth=epaisseur_ligne, facecolor="none" , edgecolor="lightgray", hatch=motif_hachure)
            
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
            
    def reflexion(self, direction_rayon_entree) :
        if self.est_vide() :
            return direction_rayon_entree
        
        if self.etat == CELLULE_PLEINE :
            if self.couleur == COULEUR_TRANSPARENTE :
                return direction_rayon_entree
            else :
                if   direction_rayon_entree == VERS_LE_BAS    : return VERS_LE_HAUT
                elif direction_rayon_entree == VERS_LE_HAUT   : return VERS_LE_BAS
                elif direction_rayon_entree == VERS_LA_DROITE : return VERS_LA_GAUCHE
                elif direction_rayon_entree == VERS_LA_GAUCHE : return VERS_LA_DROITE
        
        if direction_rayon_entree == VERS_LE_BAS :
            if   self.etat == TRIANGLE_BAS_DROITE : return VERS_LA_GAUCHE
            elif self.etat == TRIANGLE_BAS_GAUCHE : return VERS_LA_DROITE
            
            elif self.couleur == COULEUR_TRANSPARENTE : return direction_rayon_entree
            else                                      : return VERS_LE_HAUT
        
        if direction_rayon_entree == VERS_LA_DROITE :
            if   self.etat == TRIANGLE_HAUT_DROITE : return VERS_LE_BAS
            elif self.etat == TRIANGLE_BAS_DROITE  : return VERS_LE_HAUT
            
            elif self.couleur == COULEUR_TRANSPARENTE : return direction_rayon_entree
            else                                      : return VERS_LA_GAUCHE
        
        if direction_rayon_entree == VERS_LE_HAUT :
            if   self.etat == TRIANGLE_HAUT_DROITE : return VERS_LA_GAUCHE
            elif self.etat == TRIANGLE_HAUT_GAUCHE : return VERS_LA_DROITE
            
            elif self.couleur == COULEUR_TRANSPARENTE : return direction_rayon_entree
            else                                      : return VERS_LE_BAS
            
        if direction_rayon_entree == VERS_LA_GAUCHE :
            if   self.etat == TRIANGLE_BAS_GAUCHE  : return VERS_LE_HAUT
            elif self.etat == TRIANGLE_HAUT_GAUCHE : return VERS_LE_BAS
            
            elif self.couleur == COULEUR_TRANSPARENTE : return direction_rayon_entree
            else                                      : return VERS_LA_DROITE
            
        print("ERREUR - La direction de sortie du laser n'a pas été trouvée")
        
        return 9999