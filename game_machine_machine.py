import random, time

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
    cups_1 = init_cups(8,2)
    cups_2 = init_cups(8,2)

    while play:
        board = []
        path_1 = []
        path_2 = []

        nb_matches = 8
        player = "MACHINE 1" # On fait commencer la machine 1 par défaut.
        print("Nouvelle partie ! Il y a " + str(nb_matches) + " allumettes sur le plateau.")
        board = update(nb_matches)
        print(board)

        while nb_matches > 0:

            if player == "MACHINE 1":         
                print("La machine 1 joue...")
                time.sleep(2)
                
                cups_index = cups_1[len(cups_1) - nb_matches]
                choice = random.choice(cups_index)
                if choice == "red": 
                    choice_matches = 2 
                else:
                    choice_matches = 1

                path_1.append((len(cups_1) - nb_matches, choice))

                nb_matches -= choice_matches
                print("La machine 1 retire " + str(choice_matches) + " allumette(s).")
                board = update(nb_matches)
                print(board)

                if nb_matches == 0:
                    break

                if nb_matches == 0:
                    break

                player = "MACHINE 2"

            else:
                print("La machine 2 joue...")
                time.sleep(2)
                cups_index = cups_2[len(cups_2) - nb_matches]
                choice = random.choice(cups_index)
                if choice == "red": 
                    choice_matches = 2 
                else:
                    choice_matches = 1

                path_2.append((len(cups_2) - nb_matches, choice))

                nb_matches -= choice_matches
                print("La machine 2 retire " + str(choice_matches) + " allumette(s).")
                board = update(nb_matches)
                print(board)

                if nb_matches == 0:
                    break

                player = "MACHINE 1"

            print("Il reste " + str(nb_matches) + " allumette(s).")

        print("Chemin de la partie : ", path_1, path_2)
        if player == "MACHINE 1":
            print("La machine 1 gagne ! Nous allons récompenser la machine 1 et punir la machine 2 !")
            cups_1 = learning(path_1, True, cups_1, 1)
            cups_2 = learning(path_2, False, cups_2, 1)

        elif player == "MACHINE":
            print("La machine 2 gagne ! Nous allons récompenser la machine 2 et punir la machine 1 !")
            cups_2 = learning(path_2, True, cups_2, 1)
            cups_1 = learning(path_1, False, cups_1, 1)

        
        print("État des gobelets de la machine 1 après apprentissage : ", cups_1)
        print("État des gobelets de la machine 2 après apprentissage : ", cups_2)


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