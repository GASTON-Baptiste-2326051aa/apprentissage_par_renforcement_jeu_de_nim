import random

colors =  ["red", "yellow"] # jaune = 1 allumette, rouge = 2 allumettes
countByColor = 5

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
    cups[nb_cups-1] = ["red"]*nb_marbles_per_color 
    
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
    if win :
        # Pour chaque gobelet traversé, on ajoute une bille de la couleur piochée
        for cup in path :
            # On récupère l'indice du gobelet dans le tableau et on ajoute "nb_marble" fois
            # La couleur qui a permis de gagner
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




def game():
    """
    Fonction principale permettant de jouer au jeu de Nim, opposant un joueur à une machine.
    :return: Ne retourne rien, met fin au programme.
    """
    play = True

    while play:
        board = []
        path = []
        cups = init_cups(8,2)
        nb_matches = 8
        print("Qui va jouer en premier ? (1 pour l'ordinateur, 2 pour vous)")
        choice = input()

        if choice == "1":
            player = "MACHINE"

        else:
            player = "JOUEUR"

        while nb_matches > 0:
            
            if player == "JOUEUR":
                
                if nb_matches == 0:
                    break

                print("Combien d'allumettes voulez-vous retirer ? (1 ou 2)")
                choice_matches = int(input())
                while choice_matches > nb_matches:
                    if choice_matches not in [1, 2]:
                        print("Vous devez choisir 1 ou 2 allumettes.")
                    elif choice_matches > nb_matches:
                        print("Il ne reste que " + str(nb_matches) + " allumette !")
                    choice_matches = int(input("Combien d'allumettes voulez-vous retirer ? (1 ou 2) "))

                nb_matches-=choice_matches
                board = update(nb_matches)
                print(board)


                player = "MACHINE"


            elif player == "MACHINE":
                
                if nb_matches == 0:
                    break

                print("L'ordinateur joue...")
                cups_index = cups[nb_matches - 1]
                print(cups_index)
                choice = random.choice(cups_index)
                path.append([nb_matches - 1, choice])
                if choice == "red":
                    choice_matches = 2

                else:
                    choice_matches = 1

                nb_matches-=choice_matches
                print("L'ordinateur retire " + str(choice_matches) + " allumette(s).")
                board = update(nb_matches)
                print(board)

                player = "JOUEUR"

            print("Il reste " + str(nb_matches) + " allumettes.")


        print(path)
        if player == "JOUEUR":
            print("Le joueur gagne ! Nous allons punir la machine !")
            learning(path, False, cups, 2)

        elif player == "MACHINE":
            print("La machine gagne ! Nous allons récompenser la machine !")
            learning(path, True, cups, 2)



        print("Voulez-vous rejouer ? Appuyez sur 'o'")
        response = input().lower()

        if response == "o":
            play = True
        else:
            play = False

    return


game()