import random
from write_excel import WriteExcel

table_color = {"yellow": 1, "red": 2}


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


def game(max_games = 30, number_matches=11, rewards=3, punishment=1):
    """
    Fonction principale permettant de jouer au jeu de Nim, opposant un joueur à une machine.
    :return: Ne retourne rien, met fin au programme.
    """

    # Création d'une nouvelle feuille dans le fichier excel
    writer.add_sheet("test", number_matches, table_color, 6, rewards, punishment)

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
                if choice == "red": 
                    choice_matches = 2 
                else:
                    choice_matches = 1

                path_2.append((len(cups_2) - nb_matches, choice))

                nb_matches -= choice_matches

                if nb_matches == 0:
                    break

                player = "MACHINE 1"


        if player == "MACHINE 1":
            cups_1 = learning(path_1, True, cups_1, rewards, reset_history_1)
            cups_2 = learning(path_2, False, cups_2, punishment, reset_history_2)
            score_1 += 1
            results = {"P1": "gagne", "P2": "perd"} # Les résultats finaux de la partie pour le excel

        elif player == "MACHINE 2":
            cups_2 = learning(path_2, True, cups_2, rewards, reset_history_2)
            cups_1 = learning(path_1, False, cups_1, punishment, reset_history_1)
            score_2 += 1
            results = {"P1": "perd", "P2": "gagne"} # Les résultats finaux de la partie pour le excel

        game += 1

        # Ecriture des données de la partie sur la feuille
        writer.worksheet.add_game(results, score_1, score_2, path_1, path_2, cups_1, cups_2, cups_reseted_p1=reset_history_1, cups_reseted_p2=reset_history_2)

        """
        print("Voulez-vous rejouer ? Appuyez sur 'o'")
        response = input().lower()

        if response == "o":
            play = True
        else:
            play = False
        """

    return f"Score final : {score_1}-{score_2} en {game-1} parties."


# Création d'un fichier excel
writer = WriteExcel("test.xlsx")
print(game(max_games=200))
print(game(max_games=100))
print(game(max_games=30))
# Fermeture du fichier excel
writer.close_workbook()