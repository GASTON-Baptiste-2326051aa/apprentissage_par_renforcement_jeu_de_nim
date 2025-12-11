import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def load_stats(filepath, sheets):
    dfs = {}
    for s in sheets:
        df = pd.read_excel(filepath, sheet_name=s)
        df["win_M1"] = (df["Gagnant"] == "MACHINE 1").astype(int)
        dfs[s] = df
    return dfs

def curve_hypothese1(dfs):
    plt.figure(figsize=(12, 6))
    for name, df in dfs.items():
        cum = df["win_M1"].expanding().mean()
        plt.plot(cum, label=name)

    plt.title("Évolution du taux de victoire (Hypothèse 1)")
    plt.xlabel("Parties")
    plt.ylabel("Taux cumulé")
    plt.ylim(0, 1)
    plt.grid(alpha=0.3)
    plt.legend()
    plt.show()


def curve_hypothese2(dfs, step=100):
    plt.figure(figsize=(12, 6))
    for name, df in dfs.items():
        chunked = []
        for i in range(0, df["win_M1"].size, step):
            chunked.append(df["win_M1"].iloc[i:i+step].mean())
        plt.plot(chunked, label=name)

    plt.title("Score moyen par bloc (Hypothèse 2)")
    plt.xlabel(f"Bloc de {step} parties")
    plt.ylabel("Score")
    plt.ylim(0, 1)
    plt.grid(alpha=0.3)
    plt.legend()
    plt.show()


def curve_hypothese3(df):
    cum = df["win_M1"].expanding().mean()
    plt.figure(figsize=(12, 6))
    plt.plot(cum, color="purple")

    plt.title("Taux de victoire de l’IA qui commence (Hypothèse 3)")
    plt.xlabel("Parties")
    plt.ylabel("Taux cumulé")
    plt.ylim(0, 1)
    plt.grid(alpha=0.3)
    plt.show()


def curve_hypothese4(dfs):
    plt.figure(figsize=(12, 6))
    for name, df in dfs.items():
        cum = df["win_M1"].expanding().mean()
        plt.plot(cum, label=name)

    plt.title("Impact du nombre de choix (Hypothèse 4)")
    plt.xlabel("Parties")
    plt.ylabel("Taux cumulé")
    plt.ylim(0, 1)
    plt.grid(alpha=0.3)
    plt.legend()
    plt.show()


def bars_hypothese1(dfs, step=100):
    plt.figure(figsize=(14, 7))
    w = 0.12  # barres plus fines
    
    # Longueur commune
    min_len = min(df["win_M1"].size // step for df in dfs.values())
    x = np.arange(min_len)

    for i, (name, df) in enumerate(dfs.items()):
        chunked = []
        for j in range(0, df["win_M1"].size, step):
            chunked.append(df["win_M1"].iloc[j:j+step].mean() * 100)  # pourcentage

        chunked = chunked[:min_len]

        # Décalage réduit pour éviter la surcharge visuelle
        plt.bar(x + (i - len(dfs)/2) * w, chunked, w, label=name)

    # Axe X = nombre de parties
    plt.xticks(x, [(i+1)*step for i in range(min_len)], rotation=45)

    plt.title("Évolution du taux de victoire (par blocs de 100 parties)")
    plt.xlabel("Nombre de parties jouées")
    plt.ylabel("Taux de victoire (%)")
    plt.ylim(0, 100)
    plt.grid(axis="y", alpha=0.3)
    plt.legend()
    plt.tight_layout()
    plt.show()




def bars_hypothese2(dfs, step=100):
    plt.figure(figsize=(12, 6))
    w = 0.25

    min_len = min(df["win_M1"].size // step + 1 for df in dfs.values())
    x = np.arange(min_len)

    for i, (name, df) in enumerate(dfs.items()):
        chunked = []
        for j in range(0, df["win_M1"].size, step):
            chunked.append(df["win_M1"].iloc[j:j+step].mean())

        chunked = chunked[:min_len]
        plt.bar(x + i*w, chunked, w, label=name)

    plt.title("Diagramme en barres — Punition/Récompense (Hypothèse 2)")
    plt.xlabel(f"Bloc de {step} parties")
    plt.ylabel("Score moyen")
    plt.legend()
    plt.show()


def bars_hypothese3(df, step=100):
    chunked = []
    for i in range(0, df["win_M1"].size, step):
        chunked.append(df["win_M1"].iloc[i:i+step].mean())

    x = np.arange(len(chunked))
    plt.figure(figsize=(12, 6))
    plt.bar(x, chunked, color="purple")

    plt.title("Diagramme en barres — IA qui commence (Hypothèse 3)")
    plt.xlabel(f"Bloc de {step} parties")
    plt.ylabel("Score moyen")
    plt.show()


def bars_hypothese4(dfs, step=100):
    plt.figure(figsize=(12, 6))
    w = 0.25

    min_len = min(df["win_M1"].size // step + 1 for df in dfs.values())
    x = np.arange(min_len)

    for i, (name, df) in enumerate(dfs.items()):
        chunked = []
        for j in range(0, df["win_M1"].size, step):
            chunked.append(df["win_M1"].iloc[j:j+step].mean())

        chunked = chunked[:min_len]
        plt.bar(x + i*w, chunked, w, label=name)

    plt.title("Diagramme en barres — Nombre de choix (Hypothèse 4)")
    plt.xlabel(f"Bloc de {step} parties")
    plt.ylabel("Score moyen")
    plt.legend()
    plt.show()
