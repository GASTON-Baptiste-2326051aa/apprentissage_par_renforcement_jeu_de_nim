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

def matrice_adj(result):
    mat = np.zeros((len(result)+1, len(result)+1), dtype=int)
    for cup in range(len(result)):
        for color in range(len(result[cup])):
            if result[cup][color] == 'yellow' :
                mat[cup][cup+1] += 1
            if result[cup][color] == 'red' and cup<=len(result)-2:
                mat[cup][cup+2] += 1
    return mat

# Matrice d'adjacence avec probabilités

def matrice_proba(result, mat_adj):

    # Initialisation d'une matrice nulle
    mat_proba = np.zeros((len(result)+1, len(result)+1), dtype=float)

    # Parcours de la matrice d'adjacence
    for row in range(len(result)):
        # Degré sortant utilisé pour calculer les probabilités
        sum_row = len(result[row])
        # Parcours de la nouvelle matrice
        for col in range(len(mat_adj)):
            if sum_row != 0:
                mat_proba[row][col] = round(mat_adj[row][col]/sum_row, 2)

    return mat_proba

# Fonction d'affichage du graphe de manière linéaire

def graphe_trace_lineaire(G, couleurs):

    plt.figure(figsize=(14, 5)) 

    # Définition de la disposition linéaire
    ordre = sorted(G.nodes(), key=lambda x: int(x), reverse=True)
    pos = {node: (i, 0) for i, node in enumerate(ordre)}

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
    nx.draw_networkx_nodes(G, pos, node_color=couleurs, node_size=350)
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
    sommets_noyau = mpatches.Patch(color='red', label='sommet dans le noyau')
    sommets_simples = mpatches.Patch(color='lightblue', label='sommet hors du noyau')

    # Ajustement des limites de l'axe Y
    ax = plt.gca()
    ax.set_ylim(-0.5, 0.7)

    # Paramétrage et affichage du graphe
    plt.title("Graphe des états du Jeu de Nim")
    plt.legend(handles=[sommets_noyau, sommets_simples], loc='lower right')
    plt.axis("off")
    plt.show()

# Création du graphe avec recherche des sommets dans le noyau

def graphe_noyau(mat_proba):

    # Création graphe orienté
    G = nx.DiGraph()

    # Définition des noms des sommets : nb d'allumettes restantes
    sommets = []
    for i in range (len(mat_proba)):
        sommets.append(str(len(mat_proba)-i-1))

    # Ajouter les arêtes à partir de la matrice
    for i in range(len(mat_proba)):
        for j in range(len(mat_proba)):
            poids = mat_proba[i][j]
            if poids != 0:
                G.add_edge(sommets[i], sommets[j], weight=poids)

    grundy = {}

    # Parcours et définition de la valeur pour chaque sommet
    for s in sorted(sommets, key=int):
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
    couleurs = []
    for sommet in G.nodes():
        if grundy[sommet] == 0 :
            couleurs.append("red")
        else :
            couleurs.append("lightblue")

    # Tracé du graphe
    graphe_trace_lineaire(G, couleurs)

    return G, couleurs

def main():

    # Lecture du fichier résultat après jeu
    result = read_txt("apprentissage_par_renforcement_jeu_de_nim/results/11_1_2000.txt")

    # Affichage matrice d'adjacence
    print("Matrice d'adjacence : ", matrice_adj(result))

    # Affichage matrice d'adjacence avec probabilités
    mat_proba = matrice_proba(result, matrice_adj(result))
    print("Matrice d'adjacence avec probabilités : ", mat_proba)

    # Affichage du graphe à partir de la matrice d'adjacence avec les probabilités
    # Avec mise en évidence des sommets dans le noyau
    G_noyau = graphe_noyau(mat_proba)

main()