import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_excel("test_reduced.xlsx", sheet_name="test")
df_1 = pd.read_excel("test_reduced.xlsx", sheet_name="test-1")
df_2 = pd.read_excel("test_reduced.xlsx", sheet_name="test-2")

df["win_M1"] = (df["Gagnant"] == "MACHINE 1").astype(int)
df["win_M2"] = (df["Gagnant"] == "MACHINE 2").astype(int)
df_1["win_M1"] = (df_1["Gagnant"] == "MACHINE 1").astype(int)
df_1["win_M2"] = (df_1["Gagnant"] == "MACHINE 2").astype(int)
df_2["win_M1"] = (df_2["Gagnant"] == "MACHINE 1").astype(int)
df_2["win_M2"] = (df_2["Gagnant"] == "MACHINE 2").astype(int)


rolling_rate_m1 = df["win_M1"].rolling(window=20).mean()
rolling_rate_m2 = df["win_M2"].rolling(window=20).mean()
rolling_rate_m1_1 = df_1["win_M1"].rolling(window=20).mean()
rolling_rate_m2_1 = df_1["win_M2"].rolling(window=20).mean()
rolling_rate_m1_2 = df_2["win_M1"].rolling(window=20).mean()
rolling_rate_m2_2 = df_2["win_M2"].rolling(window=20).mean()


fig, ax = plt.subplots(3, 1, figsize=(10, 15))

ax[0].plot(rolling_rate_m1, label="Score MACHINE 1", color='blue')
ax[0].plot(rolling_rate_m2, label="Score MACHINE 2", color='orange')
ax[0].set_title("Score des machines au fil des parties avec 7 allumettes")
ax[0].set_xlabel("Partie")
ax[0].set_ylabel("Score")
ax[0].legend()

ax[1].plot(rolling_rate_m1_1, label="Score MACHINE 1 - test-1", color='green')
ax[1].plot(rolling_rate_m2_1, label="Score MACHINE 2 - test-1", color='red')
ax[1].set_title("Score des machines au fil des parties avec 11 allumettes")
ax[1].set_xlabel("Partie")
ax[1].set_ylabel("Score")
ax[1].legend()


ax[1].plot(rolling_rate_m1_1, label="Score MACHINE 1 - test-2", color='green')
ax[1].plot(rolling_rate_m2_1, label="Score MACHINE 2 - test-2", color='red')
ax[1].set_title("Score des machines au fil des parties avec 11 allumettes")
ax[1].set_xlabel("Partie")
ax[1].set_ylabel("Score")
ax[1].legend()
plt.show()
