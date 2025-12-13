def update(nb_matches):
    """
    Fonction mettant à jour le plateau de jeu basé sur le nombre d'allumettes actuel.
    :param nb_matches: Nombre d'allumettes dans le jeu
    :return: Un tableau représentant notre plateau de jeu
    """

    board=[]
    for _ in range(nb_matches):
        board.append("/")
    return board


def init_cups(nb_cups, nb_marbles_per_color, color_one_match, table_color):
    """
    Fonction permettant d'initialiser les gobelets avec des billes de différentes couleurs.
    :param nb_cups : Nombre de gobelets
    :param nb_marbles_per_color: Nombre de billes par couleur dans chaque gobelet
    :return: Un tableau contenant les gobelets initialisés
    """


    cups = [init_cup(nb_marbles_per_color, nb_cups-index, table_color) for index in range(nb_cups-1)]
    cups.append([color_one_match])
    return cups

def learning(path, win, cups, nb_marbles, reset_history, nb_cups,table_color):
    """
    Fonction permettant de faire apprendre la machine
    :param path: Tableau contenant les gobelets parcourus par la machine ainsi que la couleur de la bille piochée
    :param win: Booléen indiquant si la machine a gagné (true) ou perdu (false)
    :param cups: Tableau contenant les gobelets
    :param nb_marbles: Nombre de billes à ajouter ou retirer
    :param nb_cups: Nombre de gobelets
    :return: Nouveau tableau après apprentissage
    """

    for cup_index, color in path :
        if cup_index == nb_cups-1:
            continue

        if win :
            # On récupère l'indice du gobelet dans le tableau et on ajoute "nb_marble" fois
            # La couleur qui a permis de gagner
            for _ in range(nb_marbles) :
                cups[cup_index].append(color)
        else :
            for _ in range(nb_marbles) :
                if color in cups[cup_index] :
                    cups[cup_index].remove(color)

            if len(cups[cup_index]) == 0:
                reset_history.append(cup_index+1)
                cups[cup_index]=init_cup(2, nb_cups-cup_index,table_color)
                
    return cups

def init_cup(default_count, cups_left, table_color):
    """
    Fonction permettant d'initialiser un gobelet avec un nombre par défaut de billes de chaque couleur
    :param default_count: Nombre de billes par couleur dans le gobelet
    :param cups_left: Nombre de gobelets restants, sert à déterminer si certains coups deviennent impossibles à cause d'un nombre de gobelets restants insuffisant
    :return: Un nouveau gobelet
    """
    
    return [color for color in table_color for _ in range(default_count) if table_color[color] <= cups_left]
