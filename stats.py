import numpy as np
import matplotlib.pyplot as plt
import networkx as nx

# jaune : tire 1 baton
# rouge : tire deux batons

# result = [['red', 'red', 'yellow'],['red', 'yellow', 'red', 'yellow'],['yellow', 'red', 'yellow'],['red', 'yellow', 'red', 'yellow'],['red', 'yellow', 'red', 'yellow'],['red', 'red', 'yellow'],['red', 'yellow', 'red', 'yellow'],['yellow']]

result = [['red', 'yellow', 'red', 'yellow', 'red', 'yellow'], ['red', 'yellow', 'red', 'yellow', 'red', 'yellow', 'red', 'red'], ['red', 'yellow', 'red', 'yellow', 'red', 'yellow'], ['red', 'yellow', 'red', 'yellow', 'red', 'yellow'], ['red', 'yellow', 'red', 'yellow', 'red', 'yellow', 'yellow', 'yellow'], ['red', 'yellow', 'red', 'yellow', 'red', 'yellow'], ['red', 'yellow', 'red', 'yellow', 'red', 'yellow'], ['yellow', 'yellow', 'yellow', 'yellow', 'yellow']]

def matrice_adj(result) :
    mat = np.zeros((len(result)+1, len(result)+1), dtype=int)
    for cup in range(len(result)):
        for color in range(len(result[cup])):
            if result[cup][color] == 'yellow' :
                mat[cup][cup+1] += 1
            if result[cup][color] == 'red' and cup<=len(result)-2:
                mat[cup][cup+2] += 1
    return mat

# Affichage matrice d'adjacence
print("Matrice d'adjacence : ", matrice_adj(result))

def matrice_proba(result, mat_adj) :
    # Initialisation d'une matrice nulle
    mat_proba = np.zeros((len(result)+1, len(result)+1), dtype=float)
    # On parcourt la matrice d'adjacence
    for row in range(len(result)) :
        # Degré sortant utilisé pour calculer les probabilités
        sum_row = len(result[row])
        # On parcourt la nouvelle matrice
        for col in range(len(mat_adj)) :
            if sum_row != 0 :
                mat_proba[row][col] = round(mat_adj[row][col]/sum_row, 2)
    return mat_proba

# Affichage matrice d'adhacence avec probabilités
mat_proba = matrice_proba(result, matrice_adj(result))
print("Matrice d'adjacence avec probabilités : ", mat_proba)

# Définir les noms des sommets
def noms_sommets(mat_proba):
    sommets = []
    for i in range (len(mat_proba)):
        sommets.append(str(len(mat_proba)-i-1))
    return sommets

sommets = noms_sommets(mat_proba)

def graphe(mat_proba, sommets):
    
    # Créer un graphe orienté
    G = nx.DiGraph()

    # Ajouter les arêtes à partir de la matrice
    for i in range(len(mat_proba)):
        for j in range(len(mat_proba)):
            poids = mat_proba[i][j]
            if poids != 0:
                G.add_edge(sommets[i], sommets[j], weight=poids)

    graphe_trace(G)

    return G

def graphe_trace(G, couleurs = []):

    # Disposition des noeuds
    pos = nx.spring_layout(G)

    # Dessiner les noeuds et arêtes
    if couleurs == [] :
        nx.draw(G, pos, with_labels=True, node_size=1000, node_color="lightblue", arrows=True)
    else :
        nx.draw(G, pos, with_labels=True, node_size=1000, node_color=couleurs, arrows=True)
    
    # Ajouter les poids comme étiquettes sur les arêtes
    labels = nx.get_edge_attributes(G, 'weight')
    nx.draw_networkx_edge_labels(G, pos, edge_labels=labels)

    # Afficher le graphe
    plt.title("Graphe orienté et valué")
    plt.show()

# Affichage du graphe à partir de la matrice d'adjacence avec les probabilités
G_simple = graphe(mat_proba, sommets)

# Recherche des sommets dans le noyau
def graphe_noyau(mat_proba, sommets):

    # Créer un graphe orienté
    G = nx.DiGraph()

    # Ajouter les arêtes à partir de la matrice
    for i in range(len(mat_proba)):
        for j in range(len(mat_proba)):
            poids = mat_proba[i][j]
            if poids != 0:
                G.add_edge(sommets[i], sommets[j], weight=poids)

    grundy = {}

    # On parcourt les sommets dans l'ordre croissant (0,1,2,...)
    for s in sorted(sommets, key=int):
        succ = list(G.successors(s))

        # État terminal : grundy = 0
        if not succ:
            grundy[s] = 0
            continue

        # Calcul du mex
        g_values = {grundy[x] for x in succ if x in grundy}
        mex = 0
        while mex in g_values:
            mex += 1

        grundy[s] = mex

    couleurs = []

    for sommet in G.nodes():
        if grundy[sommet] == 0 :
            couleurs.append("red")
        else :
            couleurs.append("lightblue")

    graphe_trace(G, couleurs)

    return G, couleurs
            
# Affichage du graphe à partir de la matrice d'adjacence avec les probabilités
# Avec mise en évidence des sommets dans le noyau
G_noyau = graphe_noyau(mat_proba, sommets)