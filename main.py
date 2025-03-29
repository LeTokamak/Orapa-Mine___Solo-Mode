from plateau import Plateau

nb_lignes = 8
nb_colonnes = 10

plateau = Plateau(nb_lignes, nb_colonnes, avec_triangle_noir=True, avec_triangle_transparent=True)
plateau.choix_aleatoire_configuration()

partie_finie = False

while not partie_finie:
    ### Choix du joueur
    entree_du_laser = input("Où souhaitez-vous tirer un laser ? ")
    
    if entree_du_laser in plateau.entrees_disponibles_lettres or entree_du_laser in plateau.entrees_disponibles_nombres :
        plateau.tirer_laser(entree_du_laser)
        
    elif entree_du_laser == "FIN" :
        partie_finie = True
        plateau.affichage_graph_matplotlib()
        