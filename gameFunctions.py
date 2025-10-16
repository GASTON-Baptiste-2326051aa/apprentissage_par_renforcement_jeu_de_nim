import random
colors =  ["red", "yellow"]
countByColor = 5
def init_cups(nb_cups, nb_marbles_per_color):
    """
    Fonction permettant d'initialiser les gobelets avec des billes de différentes couleurs.
    :param nb_cups  :
    :param nb_marbles_per_color:
    :return:
    """
    cups = []
    for i in range(nb_cups):
        cup = []
        for j in range(nb_marbles_per_color):
            cup.append("red")
            cup.append("yellow")
        cups.append(cup)
    return cups

def learning(path, win, cups, nb_marbles) :
    """
    Fonction permettant de faire apprendre le joueur
    :param path: tableau contenant les gobelets parcourus par le joueur ainsi que la couleur de la bille piochée
    :param win: joueur a gagné (true) ou perdu (false)
    :param cups: tableau contenant les gobelets
    :param nb_marbles: nombre de billes à ajouter ou retirer
    :return: nouveau tableau après apprentissage
    """
    if win :
        #Pour chaque gobelet traversé, on ajoute une bille de la couleur piochée
        for cup in path :
            #On récupère l'indice du gobelet dans le tableau et on ajoute "nb_marble" fois
            #la couleur qui a permis de gagner
            for j in range(nb_marbles) :
                cups[cup[0]].append(cup[1])
    else :
        for cup in path :
            for j in range(nb_marbles) :
                # Si le gobelet est vide, on le réinitialise
                if len(cups[cup[0]]) == 0:
                    reset_cup(5, ["yellow", "red"])
                    break
                # Si la bille est dans le gobelet, on la retire
                elif cup[1] in cups[cup[0]] :
                    cups[cup[0]].remove(cup[1])
    return cups

def reset_cup(default_count, colors):
    """
    Fonction permettant de réinitialiser un gobelet avec un nombre par défaut de billes de chaque couleur
    :param default_count:
    :param colors:
    :return:
    """
    return [color for color in colors for _ in range(default_count)]



# def game ():
#     tab = init_cups(8, 2)
#     path = [[0,"yellow"], [2,"red"], [5,"yellow"], [7,"yellow"]]
#     newTab= learning(path,False,tab,1)
#     return newTab
#
# newTab= game()
# print(newTab)