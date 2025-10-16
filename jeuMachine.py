def update(nb_matches):
    board=[]
    for _ in range(nb_matches):
        board.append("/")
    return board


def game():
    play = True
    while play:
        board = []
        nb_matches = 8
        print("Qui va jouer en premier ? (1 pour l'ordinateur, 2 pour vous)")
        choice = input()
        if choice == "1":
            player = "MACHINE"
        else:
            player = "JOUEUR"
        while nb_matches > 0:
            if player == "JOUEUR":
                print("Combien d'allumettes voulez-vous retirer ? (1 ou 2)")
                choice_matches = int(input())
                while choice_matches > nb_matches:
                    if choice_matches not in [1, 2]:
                        print("Vous devez choisir 1 ou 2 allumettes.")
                    elif choice_matches > nb_matches:
                        print("Il ne reste que", nb_matches, "allumette(s) !")
                    choice_matches = int(input("Combien d'allumettes voulez-vous retirer ? (1 ou 2) "))
                nb_matches-=choice_matches
                board = update(nb_matches)
                print(board)
                player = "MACHINE"

            elif player == "MACHINE":
                print("L'ordinateur joue...")
                player = "JOUEUR"
                board = update(nb_matches)
                print(board)
            print("Il reste " + str(nb_matches) + " allumettes.")
        print("Le gagnant est " + player + " !")
        print("Voulez-vous rejouer ? (o/n)")
        response = input().lower()
        if response == "o":
            play = True
        else:
            play = False
    return


game()