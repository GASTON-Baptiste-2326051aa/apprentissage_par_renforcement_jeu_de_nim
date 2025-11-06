import numpy as np
import matplotlib.pyplot as plt
import networkx as nx

# result = [['red', 'red', 'yellow'],['red', 'yellow', 'red', 'yellow'],['yellow', 'red', 'yellow'],['red', 'yellow', 'red', 'yellow'],['red', 'yellow', 'red', 'yellow'],['red', 'red', 'yellow'],['red', 'yellow', 'red', 'yellow'],['yellow']]

result = [['red', 'yellow', 'red', 'yellow', 'red', 'yellow'], ['red', 'yellow', 'red', 'yellow', 'red', 'yellow', 'red', 'red'], ['red', 'yellow', 'red', 'yellow', 'red', 'yellow'], ['red', 'yellow', 'red', 'yellow', 'red', 'yellow'], ['red', 'yellow', 'red', 'yellow', 'red', 'yellow', 'yellow', 'yellow'], ['red', 'yellow', 'red', 'yellow', 'red', 'yellow'], ['red', 'yellow', 'red', 'yellow', 'red', 'yellow'], ['yellow', 'yellow', 'yellow', 'yellow', 'yellow']]

def matrice(result) :
    mat = np.zeros((len(result)+1, len(result)+1), dtype=int)
    for cup in range(len(result)):
        for color in range(len(result[cup])):
            if result[cup][color] == 'yellow' :
                mat[cup][cup+1] += 1
            if result[cup][color] == 'red' and cup<=len(result)-2:
                mat[cup][cup+2] += 1
    return mat

print("Matrice d'adjacence : ", matrice(result))

def matrice2(result, mat_adj) :
    # Initialisation d'une matrice nulle
    mat_proba = np.zeros((len(result)+1, len(result)+1), dtype=float)
    # On parcourt la matrice d'adjacence
    for row in range(len(result)) :
        # Degré sortant utilisé pour calculer les probabilités
        sum_row = len(result[row])
        print(sum_row)
        # On parcourt la nouvelle matrice
        for col in range(len(mat_adj)) :
            if sum_row != 0 :
                mat_proba[row][col] = round(mat_adj[row][col]/sum_row, 2)
    return mat_proba

matrice_proba = matrice2(result, matrice(result))
print("Matrice d'adjacence avec proba : ", matrice_proba)

# Graphe à partir de la matrice d'adjacence

# Définir les noms des sommets

def noms_sommets(matrice_proba):
    sommets = []
    for i in range (len(matrice_proba)):
        sommets.append(str(len(matrice_proba)-i-1))
    return sommets

sommets = noms_sommets(matrice_proba)

# Créer un graphe orienté
G = nx.DiGraph()

# Ajouter les arêtes à partir de la matrice
n = len(matrice_proba)
for i in range(n):
    for j in range(n):
        poids = matrice_proba[i][j]
        if poids != 0:
            G.add_edge(sommets[i], sommets[j], weight=poids)

# Calculer la disposition des nœuds
pos = nx.spring_layout(G)  # placement automatique

# Dessiner les nœuds et arêtes
nx.draw(G, pos, with_labels=True, node_size=1000, node_color="lightblue", arrows=True)

# Ajouter les poids comme étiquettes sur les arêtes
labels = nx.get_edge_attributes(G, 'weight')
nx.draw_networkx_edge_labels(G, pos, edge_labels=labels)

# Afficher le graphe
plt.title("Graphe orienté et valué")
plt.show()

# Recherche des composantes fortement connexes
scc = list(nx.strongly_connected_components(G))
print("Composantes fortement connexes :", scc)

# Trouver les composantes sans successeur → noyau du graphe
# (aucune arête sortant de cette composante vers une autre)
meta_graph = nx.condensation(G)
noeuds_noyau = [scc[i] for i in range(meta_graph.number_of_nodes())
                if meta_graph.out_degree(i) == 0]

print("Noyau du graphe :", noeuds_noyau)