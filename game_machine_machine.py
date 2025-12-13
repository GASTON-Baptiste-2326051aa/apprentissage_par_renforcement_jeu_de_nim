import random
from write_excel import WriteExcel, WriteExcelReduced
from game_functions import learning, update, init_cups, init_cup


def game(max_games = 2000, number_matches=11, rewards=1, punishment=1, sheetname="tmp", table_color = {"yellow": 1, "red": 2}, writer = WriteExcel("tmp"), writer_reduced = WriteExcelReduced("tmp"), first_player = "MACHINE 1" ) :
    """
    Fonction principale permettant de jouer au jeu de Nim, opposant un joueur à une machine.
    :return: Ne retourne rien, met fin au programme.
    """
    color_one_match = -1
    for color, match in table_color.items():
        if match == 1:
            color_one_match = color
            break
        
    # s'il n'y a aucun coup permettant de ne retirer qu'une seule allumette, l'apprentissage ne peut pas avoir lieu
    if color_one_match == -1:
        return "Paramètres non recevables : Aucun coup ne permet de ne retirer qu'une seule allumette"
    
    # Création d'une nouvelle feuille dans le fichier excel
    writer.add_sheet(sheetname, number_matches, table_color, 6, rewards, punishment)
    writer_reduced.add_sheet(sheetname)

    cups_1 = init_cups(number_matches,6,color_one_match, table_color)
    cups_2 = init_cups(number_matches,6,color_one_match, table_color)
    score_1 = 0
    score_2 = 0
    game = 1
    
    while max_games >= game:
        reset_history_1 = []
        reset_history_2 = []
        path_1 = []
        path_2 = []

        nb_matches = number_matches
        player = first_player

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
            cups_1 = learning(path_1, True, cups_1, rewards, reset_history_1, number_matches,table_color)
            cups_2 = learning(path_2, False, cups_2, punishment, reset_history_2, number_matches,table_color)
            score_1 += 1
            results = {"P1": "gagne", "P2": "perd"} # Les résultats finaux de la partie pour le excel

        elif player == "MACHINE 2":
            cups_2 = learning(path_2, True, cups_2, rewards, reset_history_2, number_matches,table_color)
            cups_1 = learning(path_1, False, cups_1, punishment, reset_history_1, number_matches,table_color)
            score_2 += 1
            results = {"P1": "perd", "P2": "gagne"} # Les résultats finaux de la partie pour le excel

        game += 1

        # Ecriture des données de la partie sur la feuille
        writer.worksheet.add_game(results, score_1, score_2, path_1, path_2, cups_1, cups_2, cups_reseted_p1=reset_history_1, cups_reseted_p2=reset_history_2)
        writer_reduced.add_game(player)

    return f"Score final : {score_1}-{score_2} en {game-1} parties."

