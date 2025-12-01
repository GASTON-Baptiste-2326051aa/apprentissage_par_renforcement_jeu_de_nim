import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

df = pd.read_excel("test_reduced.xlsx", sheet_name="tmp")
df_1 = pd.read_excel("test_reduced.xlsx", sheet_name="tmp-1")
df_2 = pd.read_excel("test_reduced.xlsx", sheet_name="tmp-2")

df["win_M1"] = (df["Gagnant"] == "MACHINE 1").astype(int)
df_1["win_M1"] = (df_1["Gagnant"] == "MACHINE 1").astype(int)
df_2["win_M1"] = (df_2["Gagnant"] == "MACHINE 1").astype(int)

step = 100
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


w, x = 0.2, np.arange(len(chunked_means))
fig, ax = plt.subplots()
ax.bar(x - w, chunked_means, w,  label="7 allumettes", color='blue', align="center")
ax.bar(x, chunked_means_1, w, label="11 allumettes", color='orange', align="center")
ax.bar(x + w, chunked_means_2, w, label="16 allumettes", color='green', align="center")
plt.title("Score des machines au fil des parties selon le nombre d'allumettes")
plt.xlabel("Partie")
plt.ylabel("Score")
plt.legend()
plt.show()
