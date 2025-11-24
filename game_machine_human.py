import random

tableau_couleur = {"yellow": 1, "red": 2}

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
    :param nb_cups : Nombre de gobelets.
    :param nb_marbles_per_color: Nombre de billes par couleur dans chaque gobelet.
    :return: Un tableau contenant les gobelets initialisés.
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


def learning(path, win, cups, nb_marbles) :
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
                cups[cup_index]=reset_cup(2, ["yellow", "red"])
    return cups

def reset_cup(default_count, colors):
    """
    Fonction permettant de réinitialiser un gobelet avec un nombre par défaut de billes de chaque couleur
    :param default_count:
    :param colors:
    :return:
    """
    print("Réinitialisation du gobelet...")
    return [color for color in colors for _ in range(default_count)]


def game():
    """
    Fonction principale permettant de jouer au jeu de Nim, opposant un joueur à une machine.
    :return: Ne retourne rien, met fin au programme.
    """
    play = True
    cups = init_cups(8,2)

    while play:
        board = []
        path = []
        score_1 = 0
        score_2 = 0

        nb_matches = 8
        player = "MACHINE" # On fait commencer la machine par défaut.
        print("Nouvelle partie ! Il y a " + str(nb_matches) + " allumettes sur le plateau.")
        board = update(nb_matches)
        print(board)

        while nb_matches > 0:

            if player == "JOUEUR":         

                choice_matches = int(input("Combien d'allumettes voulez-vous retirer ? (1 ou 2)"))
                while choice_matches not in [1, 2] or choice_matches > nb_matches:
                    if choice_matches not in [1, 2]:
                        print("Vous devez choisir 1 ou 2 allumettes.")
                    else:
                        print("Il ne reste que " + str(nb_matches) + " allumette(s) !")
                    choice_matches = int(input("Combien d'allumettes voulez-vous retirer ? (1 ou 2) "))

                nb_matches -= choice_matches
                board = update(nb_matches)
                print(board)

                if nb_matches == 0:
                    break

                player = "MACHINE"

            else:
                print("L'ordinateur joue...")
                cups_index = cups[len(cups) - nb_matches]
                choice = random.choice(cups_index)
                if choice == "red": 
                    choice_matches = 2 
                else:
                    choice_matches = 1

                path.append((len(cups) - nb_matches, choice))

                nb_matches -= choice_matches
                print("L'ordinateur retire " + str(choice_matches) + " allumette(s).")
                board = update(nb_matches)
                print(board)

                if nb_matches == 0:
                    break

                player = "JOUEUR"

            print("Il reste " + str(nb_matches) + " allumette(s).")

        print("Chemin de la partie : ", path)
        if player == "JOUEUR":
            print("Le joueur gagne ! Nous allons punir la machine !")
            cups = learning(path, False, cups, 1)
            score_1 += 1

        elif player == "MACHINE":
            print("La machine gagne ! Nous allons récompenser la machine !")
            cups = learning(path, True, cups, 1)
            score_2 += 1

        
        print("État des gobelets après apprentissage : ", cups)

        """
        print("Voulez-vous rejouer ? Appuyez sur 'o'")
        response = input().lower()

        if response == "o":
            play = True
        else:
            play = False
        """

    return



game()