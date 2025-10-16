def update(nb_allumettes):
    board=[]
    for _ in range(nb_allumettes):
        board.append("/")
        board.append(" ")
    return board


def jeu():

    jouer = True
    nombre_allumettes=8
    board = [] 
    gobelets = [] 
    print("Qui va jouer en premier ? (1 pour l'ordinateur, 2 pour vous)")
    choix = input()
    if choix == "1":
        player = "MACHINE"
    else:
        player = "JOUEUR"
    while jouer:
        while nombre_allumettes > 0:
            if player == "JOUEUR":
                print("Combien d'allumettes voulez-vous retirer ? (1 ou 2)")
                player = "MACHINE"

            elif player == "MACHINE":
                print("L'ordinateur joue...")
                player = "JOUEUR"
            board = update(nombre_allumettes)
            print(board)
            print("Il reste " + str(nombre_allumettes) + " allumettes.")
    print("Le gagnant est " + player + " !")
    print("Voulez-vous rejouer ? (o/n)")
    reponse = input().lower()
    if reponse == "o":
        jouer = True
    else:
        jouer = False

    return
