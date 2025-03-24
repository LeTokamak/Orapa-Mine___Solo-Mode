from plateau import nouvelle_configuration_plateau

nb_lignes = 8
nb_colonnes = 10

plateau = nouvelle_configuration_plateau(nb_lignes, nb_colonnes)

partie_finie = False

while not partie_finie:
    ### Choix du joueur
    entree_du_laser = input("Où souhaitez-vous tirer un laser ? ")
    
    if entree_du_laser in plateau.entrees_disponibles :
        (sortie_du_laser, nb_deviation_laser, couleur_laser) = plateau.tirer_laser(entree_du_laser)
        print("Sortie du laser : ", sortie_du_laser)
        print("Nb de deviation du laser : ", nb_deviation_laser)
        print("Couleur du laser : ", couleur_laser)
        
    elif entree_du_laser == "FIN" :
        partie_finie = True
        