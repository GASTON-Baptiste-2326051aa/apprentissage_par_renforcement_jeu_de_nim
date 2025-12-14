import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def load_stats(filepath, sheets):
    """
    Charge les statistiques de parties depuis un fichier Excel
    et prépare les données pour l'analyse.
    :param filepath: Chemin du fichier Excel
    :param sheets: Liste des noms de feuilles à analyser
    :return: dictionnaire {nom_feuille: DataFrame}
    """
    dfs = {}
    for s in sheets:
        # Lecture de la feuille Excel
        df = pd.read_excel(filepath, sheet_name=s)
        # Création d'une variable binaire : win_M1 = 1 si MACHINE 1 gagne, sinon 0
        df["win_M1"] = (df["Gagnant"] == "MACHINE 1").astype(int)
        # Stockage dans un dictionnaire pour faciliter l’itération
        dfs[s] = df
    return dfs

def bars_hypothese1(dfs, step=200):
    """
    Diagramme en barres montrant l’évolution du taux de victoire
    de la machine 1 selon le nombre d’allumettes initiale
    """
    plt.figure(figsize=(14, 7))

    # Largeur des barres
    w = 0.12
    # On impose une longueur commune à toutes les séries pour garantir une comparaison équitable
    min_len = min(df["win_M1"].size // step for df in dfs.values())
    x = np.arange(min_len)

    for i, (name, df) in enumerate(dfs.items()):
        # Calcul du taux de victoire par blocs de parties
        chunked = []
        # On parcourt les parties par blocs de taille 'step'
        for j in range(0, min_len * step, step):
            # Sélection des résultats des 'step' parties consécutives
            bloc = df["win_M1"].iloc[j : j + step]
            # Calcul du taux de victoire moyen sur ce bloc
            taux_victoire = bloc.mean() * 100 
            # Stockage du résultat
            chunked.append(taux_victoire)
        # Décalage horizontal pour placer plusieurs barres par bloc
        plt.bar(x + (i - len(dfs)/2) * w,chunked,w,label=name)
        
    # L’axe X correspond ici au nombre total de parties jouées
    plt.xticks(x, [(i+1)*step for i in range(min_len)], rotation=45)
    plt.title("Évolution du taux de victoire selon le nombre d’allumettes")
    plt.xlabel("Nombre de parties jouées")
    plt.ylabel("Taux de victoire (%)")
    plt.ylim(0, 100)
    plt.grid(axis="y", alpha=0.3)
    plt.legend()
    plt.tight_layout()
    plt.show()

def bars_hypothese2(dfs, step=200):
    """
    Diagramme en barres comparant différents systèmes
    de punition et de récompense.
    """
    plt.figure(figsize=(14, 7))
    w = 0.18

    min_len = min(df["win_M1"].size // step for df in dfs.values())
    x = np.arange(min_len)

    for i, (name, df) in enumerate(dfs.items()):
        # Calcul du taux de victoire par blocs de parties
        chunked = []
        # On parcourt les parties par blocs de taille 'step'
        for j in range(0, min_len * step, step):
            # Sélection des résultats des 'step' parties consécutives
            bloc = df["win_M1"].iloc[j : j + step]
            # Calcul du taux de victoire moyen sur ce bloc
            taux_victoire = bloc.mean() * 100 
            # Stockage du résultat
            chunked.append(taux_victoire)
        # Décalage horizontal pour placer plusieurs barres par bloc
        plt.bar(x + (i - len(dfs)/2) * w,chunked,w,label=name)

    plt.xticks(x, [(i+1)*step for i in x], rotation=45)
    plt.title("Impact de la punition et de la récompense sur l’apprentissage")
    plt.xlabel("Nombre de parties jouées")
    plt.ylabel("Taux de victoire (%)")
    plt.ylim(0, 100)
    plt.grid(axis="y", alpha=0.3)
    plt.legend()
    plt.tight_layout()
    plt.show()

def bars_hypothese3(dfs, step=200):
    """
    Diagramme en barres mesurant l’impact de l’ordre de jeu.
    """
    plt.figure(figsize=(14, 7))
    w = 0.25

    min_len = min(df["win_M1"].size // step for df in dfs.values())
    x = np.arange(min_len)

    for i, (name, df) in enumerate(dfs.items()):
        # Calcul du taux de victoire par blocs de parties
        chunked = []
        # On parcourt les parties par blocs de taille 'step'
        for j in range(0, min_len * step, step):
            # Sélection des résultats des 'step' parties consécutives
            bloc = df["win_M1"].iloc[j : j + step]
            # Calcul du taux de victoire moyen sur ce bloc
            taux_victoire = bloc.mean() * 100 
            # Stockage du résultat
            chunked.append(taux_victoire)
        # Décalage horizontal pour placer plusieurs barres par bloc
        plt.bar(x + (i - len(dfs)/2) * w,chunked,w,label=name)
        
    plt.xticks(x, [(i+1)*step for i in x], rotation=45)
    plt.title("Impact de l’ordre de jeu sur le taux de victoire de la machine 1")
    plt.xlabel("Nombre de parties jouées")
    plt.ylabel("Taux de victoire (%)")
    plt.ylim(0, 100)
    plt.grid(axis="y", alpha=0.3)
    plt.legend()
    plt.tight_layout()
    plt.show()

def bars_hypothese4(dfs, step=200):
    """
    Diagramme en barres analysant l’effet du nombre de choix
    possibles à chaque tour (ex : prendre 1, 2, 3 ou 4 allumettes).
    """
    plt.figure(figsize=(14, 7))
    w = 0.2

    min_len = min(df["win_M1"].size // step for df in dfs.values())
    x = np.arange(min_len)

    for i, (name, df) in enumerate(dfs.items()):
        # Calcul du taux de victoire par blocs de parties
        chunked = []
        # On parcourt les parties par blocs de taille 'step'
        for j in range(0, min_len * step, step):
            # Sélection des résultats des 'step' parties consécutives
            bloc = df["win_M1"].iloc[j : j + step]
            # Calcul du taux de victoire moyen sur ce bloc
            taux_victoire = bloc.mean() * 100 
            # Stockage du résultat
            chunked.append(taux_victoire)
        # Décalage horizontal pour placer plusieurs barres par bloc
        plt.bar(x + (i - len(dfs)/2) * w,chunked,w,label=name)

    plt.xticks(x, [(i+1)*step for i in x], rotation=45)
    plt.title("Impact du nombre de choix possibles sur l’apprentissage")
    plt.xlabel("Nombre de parties jouées")
    plt.ylabel("Taux de victoire (%)")
    plt.ylim(0, 100)
    plt.grid(axis="y", alpha=0.3)
    plt.legend()
    plt.tight_layout()
    plt.show()
