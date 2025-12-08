import random
from write_excel import WriteExcel, WriteExcelReduced

table_color = {"yellow": 1, "red": 2, "blue": 4}
color_one_match = -1
for color, match in table_color.items():
    if match == 1:
        color_one_match = color
        break
if color_one_match == -1:
    print("paramètres non recevables")


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


    cups = [init_cup(nb_marbles_per_color, nb_cups-index) for index in range(nb_cups-1)]
    cups.append([color_one_match])
    return cups

def learning(path, win, cups, nb_marbles, reset_history, nb_cups):
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
                cups[cup_index]=init_cup(2, nb_cups-cup_index)
                
    return cups

def init_cup(default_count, cups_left):
    """
    Fonction permettant d'initialiser un gobelet avec un nombre par défaut de billes de chaque couleur
    :param default_count: Nombre de billes par couleur dans le gobelet
    :param cups_left: Nombre de gobelets restants, sert à déterminer si certains coups deviennent impossibles à cause d'un nombre de gobelets restants insuffisant
    :return: Un nouveau gobelet
    """
    
    return [color for color in table_color for _ in range(default_count) if table_color[color] <= cups_left]


def game(max_games = 30, number_matches=11, rewards=3, punishment=1, sheetname="tmp"):
    """
    Fonction principale permettant de jouer au jeu de Nim, opposant un joueur à une machine.
    :return: Ne retourne rien, met fin au programme.
    """

    # Création d'une nouvelle feuille dans le fichier excel
    writer.add_sheet(sheetname, number_matches, table_color, 6, rewards, punishment)
    writer_reduced.add_sheet(sheetname)

    cups_1 = init_cups(number_matches,6)
    cups_2 = init_cups(number_matches,6)
    score_1 = 0
    score_2 = 0
    game = 1
    
    while max_games >= game:
        reset_history_1 = []
        reset_history_2 = []
        path_1 = []
        path_2 = []

        nb_matches = number_matches
        player = "MACHINE 1" # On fait commencer la machine 1 par défaut.

        while nb_matches > 0:

            if player == "MACHINE 1":         
                
                cups_index = cups_1[len(cups_1) - nb_matches]
                choice = random.choice(cups_index)
                choice_matches = table_color.get(choice)

                path_1.append((len(cups_1) - nb_matches, choice))

                nb_matches -= choice_matches

                if nb_matches == 0:
                    break

                player = "MACHINE 2"

            else:
                cups_index = cups_2[len(cups_2) - nb_matches]
                choice = random.choice(cups_index)
                choice_matches = table_color.get(choice)

                path_2.append((len(cups_2) - nb_matches, choice))

                nb_matches -= choice_matches

                if nb_matches == 0:
                    break

                player = "MACHINE 1"


        if player == "MACHINE 1":
            cups_1 = learning(path_1, True, cups_1, rewards, reset_history_1, number_matches)
            cups_2 = learning(path_2, False, cups_2, punishment, reset_history_2, number_matches)
            score_1 += 1
            results = {"P1": "gagne", "P2": "perd"} # Les résultats finaux de la partie pour le excel

        elif player == "MACHINE 2":
            cups_2 = learning(path_2, True, cups_2, rewards, reset_history_2, number_matches)
            cups_1 = learning(path_1, False, cups_1, punishment, reset_history_1, number_matches)
            score_2 += 1
            results = {"P1": "perd", "P2": "gagne"} # Les résultats finaux de la partie pour le excel

        game += 1

        # Ecriture des données de la partie sur la feuille
        writer.worksheet.add_game(results, score_1, score_2, path_1, path_2, cups_1, cups_2, cups_reseted_p1=reset_history_1, cups_reseted_p2=reset_history_2)
        writer_reduced.add_game(player)

    return f"Score final : {score_1}-{score_2} en {game-1} parties."


# Création d'un fichier excel
writer = WriteExcel("test")
writer_reduced = WriteExcelReduced("test")

print(game(max_games=2000, number_matches=7))
#game(max_games=2000, number_matches=11)
#game(max_games=2000, number_matches=16)

# Fermeture du fichier excel
writer.close_workbook()
writer_reduced.close_workbook()
