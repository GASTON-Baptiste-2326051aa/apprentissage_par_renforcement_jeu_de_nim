import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_excel("test_reduced.xlsx", sheet_name="tmp")
df_1 = pd.read_excel("test_reduced.xlsx", sheet_name="tmp-1")
df_2 = pd.read_excel("test_reduced.xlsx", sheet_name="tmp-2")

df["win_M1"] = (df["Gagnant"] == "MACHINE 1").astype(int)
df_1["win_M1"] = (df_1["Gagnant"] == "MACHINE 1").astype(int)
df_2["win_M1"] = (df_2["Gagnant"] == "MACHINE 1").astype(int)

step = 50
chunked_means = []
chunked_means_1 = []
chunked_means_2 = []

for i in range(0, df["win_M1"].size, step):
    chunk = df["win_M1"].iloc[i:i+step]
    chunked_means.append(chunk.mean())

for i in range(0, df["win_M1"].size, step):
    chunk = df_1["win_M1"].iloc[i:i+step]
    chunked_means_1.append(chunk.mean())

for i in range(0, df["win_M1"].size, step):
    chunk = df_2["win_M1"].iloc[i:i+step]
    chunked_means_2.append(chunk.mean())


plt.barh(chunked_means, step, label="7 allumettes", color='blue')
plt.title("Score des machines au fil des parties selon le nombre d'allumettes")
plt.xlabel("Partie")
plt.ylabel("Score")
plt.legend()
plt.show()
