import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import networkx as nx
import ast

# jaune : tire 1 baton
# rouge : tire deux batons

# Lecture du fichier résultat après jeu

def read_txt(fichier):
    with open(fichier, "r") as f:
        contenu = f.read()
    return ast.literal_eval(contenu)

# Matrice d'adjacence

def adjacency_matrix(result):
    mat = np.zeros((len(result)+1, len(result)+1), dtype=int)
    for cup in range(len(result)):
        for color in range(len(result[cup])):
            if result[cup][color] == 'yellow' :
                mat[cup][cup+1] += 1
            if result[cup][color] == 'red' and cup<=len(result)-2:
                mat[cup][cup+2] += 1
    return mat

# Matrice de transition

def transition_matrix(result, adj_mat):

    # Initialisation d'une matrice nulle
    mat = np.zeros((len(result)+1, len(result)+1), dtype=float)

    # Parcours de la matrice d'adjacence
    for row in range(len(result)):
        # Degré sortant utilisé pour calculer les probabilités
        sum_row = len(result[row])
        # Parcours de la nouvelle matrice
        for col in range(len(adj_mat)):
            if sum_row != 0:
                mat[row][col] = round(adj_mat[row][col]/sum_row, 2)

    return mat

# Fonction d'affichage du graphe de manière linéaire

def draw_linear_graph(G, colors, title):

    # Définition de la taille de la figure
    plt.figure(figsize=(14, 5))

    # Définition de la disposition linéaire
    sorted_nodes = sorted(G.nodes(), key=lambda x: int(x), reverse=True)
    pos = {node: (i, 0) for i, node in enumerate(sorted_nodes)}

    # Tracé des arêtes (avec courbure pour les transitions de 2 en 2)
    for u, v in G.edges():
        diff = abs(int(u) - int(v))
        if diff == 2:
            rad = -0.3
        else:
            rad = 0.0

        nx.draw_networkx_edges(
            G,
            pos,
            edgelist=[(u, v)],
            connectionstyle=f"arc3,rad={rad}",
            arrowstyle='->',
            arrowsize=16,
            edge_color='gray' 
        )

    # Tracé des nœuds avec labels
    nx.draw_networkx_nodes(G, pos, node_color=colors, node_size=350)
    nx.draw_networkx_labels(G, pos, font_size=10)

    # Tracé des labels des arêtes
    edge_labels_straight = {}
    edge_labels_curved = {}

    for u, v, data in G.edges(data=True):
        weight = data['weight']
        diff = abs(int(u) - int(v))
        
        if diff == 1:
            edge_labels_straight[(u, v)] = weight
        elif diff == 2:
            edge_labels_curved[(u, v)] = weight

    # Tracé des labels pour les arêtes de 1 en 1 (droites)
    nx.draw_networkx_edge_labels(
        G,
        pos,
        edge_labels=edge_labels_straight,
        font_size=8,
        rotate=False,
        label_pos=0.5
    )

    # Tracé des labels pour les arêtes de 2 en 2 (courbées)
    vertical_offset = 0.09
    bbox_settings = {"boxstyle": "round, pad=0.2", "fc": "white", "alpha": 1, "ec": "none"}
    
    for (u, v), weight in edge_labels_curved.items():
        
        x_u, y_u = pos[u]
        x_v, y_v = pos[v]
        mid_x = (x_u + x_v) / 2
        mid_y = (y_u + y_v) / 2
        
        x_label, y_label = (mid_x, mid_y + vertical_offset)

        plt.text(
            x_label,
            y_label,
            s=str(weight),
            fontsize=8,
            horizontalalignment='center',
            verticalalignment='center',
            bbox=bbox_settings,
            zorder=5
        )

    # Légende des sommets 
    kernel_nodes = mpatches.Patch(color='red', label='sommet dans le noyau')
    simple_nodes = mpatches.Patch(color='lightblue', label='sommet hors du noyau')

    # Ajustement des limites de l'axe Y
    ax = plt.gca()
    ax.set_ylim(-0.5, 0.7)

    # Paramétrage et affichage du graphe
    plt.title(title)
    plt.legend(handles=[kernel_nodes, simple_nodes], loc='lower right')
    plt.axis("off")
    plt.show()

# Création du graphe avec recherche des sommets dans le noyau

def kernel_graph(trans_matrix):

    # Création du graphe orienté
    G = nx.DiGraph()
  
    n = len(trans_matrix)
    
    # Définition des noms des sommets
    nodes = [str(n - i - 1) for i in range(n)]

    # Ajout des arêtes à partir de la matrice
    for i in range(n):
        for j in range(n):
            weight = trans_matrix[i][j]
            if weight!= 0:
                G.add_edge(nodes[i], nodes[j], weight=weight)

    grundy = {}

    # Parcours et définition de la valeur pour chaque sommet
    for s in sorted(nodes, key=int):
        succ = list(G.successors(s))

        # État terminal = 0
        if not succ:
            grundy[s] = 0
            continue

        # Calcul de la valeur minimale différentes de celles des successeurs (mex)
        g_values = {grundy[x] for x in succ if x in grundy}
        mex = 0
        while mex in g_values:
            mex += 1

        grundy[s] = mex

    # Définition des couleurs pour chaque sommet en fonction de la valeur de grundy
    colors = []
    for sommet in G.nodes():
        if grundy[sommet] == 0 :
            colors.append("red")
        else :
            colors.append("lightblue")

    return G, colors

def main():

    # Lecture du fichier résultat après jeu
    result = read_txt("apprentissage_par_renforcement_jeu_de_nim/results/11_1_2000.txt")

    # Affichage matrice d'adjacence
    print("Matrice d'adjacence : ", adjacency_matrix(result))

    # Affichage matrice de transition
    trans_matrix = transition_matrix(result, adjacency_matrix(result))
    print("Matrice de transition : ", trans_matrix)

    # Création du graphe avec recherche des sommets dans le noyau
    G, colors = kernel_graph(trans_matrix)

    # Affichage du graphe à partir de la matrice d'adjacence avec les probabilités
    # Avec mise en évidence des sommets dans le noyau
    draw_linear_graph(G, colors, "Graphe des probabilités de jeu de la machine 1 après 2000 parties d'entraînement avec mise en évidence du noyau")

main()