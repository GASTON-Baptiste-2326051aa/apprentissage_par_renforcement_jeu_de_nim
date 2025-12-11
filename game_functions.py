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


def init_cups(nb_cups, nb_marbles_per_color):
    """
    Fonction permettant d'initialiser les gobelets avec des billes de différentes couleurs.
    :param nb_cups : Nombre de gobelets
    :param nb_marbles_per_color: Nombre de billes par couleur dans chaque gobelet
    :return: Un tableau contenant les gobelets initialisés
    """
    cups = []
    for _ in range(nb_cups):
        cup = []
        for _ in range(nb_marbles_per_color):
            cup.append("red")
            cup.append("yellow")
        cups.append(cup)
    cups[nb_cups-1] = ["yellow"]*nb_marbles_per_color 
    return cups


def learning(path, win, cups, nb_marbles, reset_history) :
    """
    Fonction permettant de faire apprendre la machine
    :param path: tableau contenant les gobelets parcourus par la machine ainsi que la couleur de la bille piochée
    :param win: machine a gagné (true) ou perdu (false)
    :param cups: tableau contenant les gobelets
    :param nb_marbles: nombre de billes à ajouter ou retirer
    :return: nouveau tableau après apprentissage
    """
    for cup_index, color in path :
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
                reset_history.append(cup_index)
                cups[cup_index]=reset_cup(2, ["yellow", "red"])
                
    return cups

def reset_cup(default_count, colors):
    """
    Fonction permettant de réinitialiser un gobelet avec un nombre par défaut de billes de chaque couleur
    :param default_count:
    :param colors:
    :return:
    """
    return [color for color in colors for _ in range(default_count)]