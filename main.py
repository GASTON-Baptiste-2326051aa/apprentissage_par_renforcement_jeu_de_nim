from write_excel import WriteExcel, WriteExcelReduced
from game_machine_machine import game
from charts import load_stats,bars_hypothese1,bars_hypothese2,bars_hypothese3,bars_hypothese4,bars_hypothese5
from game_machine_random import game_random


def create_data(): 
    """
    Fonction permettant de créer les données pour les graphiques.
    :return: Ne retourne rien.
    """
    hypothese1()
    hypothese2()
    hypothese3()
    hypothese4()
    hypothese5()
    
def show_all_charts():
    show_chart_h1()
    show_chart_h2()
    show_chart_h3()
    show_chart_h4()
    show_chart_h5()


def hypothese1():
    """
    Fonction principale permettant de créer les données pour l'hypothèse 1
    :return: Ne retourne rien.
    """
    #Création Excel
    writer1 = WriteExcel("Hypothèse 1")
    writer_reduced1 = WriteExcelReduced("Hypothèse 1")
    #Entraînement de l'IA
    game(1000,11,sheetname="11 allumettes", writer=writer1, writer_reduced=writer_reduced1)
    game(1000,20,sheetname="20 allumettes", writer=writer1, writer_reduced=writer_reduced1)
    game(1000,29,sheetname="29 allumettes", writer=writer1, writer_reduced=writer_reduced1)
    
    #Fermeture du excel
    writer1.close_workbook()
    writer_reduced1.close_workbook()
    print("H1")
    
def hypothese2():
    """
    Fonction principale permettant de créer les données pour l'hypothèse 2
    :return: Ne retourne rien.
    """
    #Création Excel
    writer2 = WriteExcel("Hypothèse 2")
    writer_reduced2 = WriteExcelReduced("Hypothèse 2")
    
    #Entraînement de l'IA
    game(1000,11,1,1,sheetname="Punition et récompense = 1",writer=writer2, writer_reduced=writer_reduced2)
    game(1000,11,3,3,sheetname="Punition et récompense = 3",writer=writer2, writer_reduced=writer_reduced2)
    game(1000,11,5,5,sheetname="Punition et récompense = 5",writer=writer2, writer_reduced=writer_reduced2)
    game(1000,11,6,6,sheetname="Punition et récompense = 6",writer=writer2, writer_reduced=writer_reduced2)
    
    #Fermeture du excel
    writer2.close_workbook()
    writer_reduced2.close_workbook()
    print("H2")
    
def hypothese3():    
    """
    Fonction principale permettant de créer les données pour l'hypothèse 3
    :return: Ne retourne rien.
    """
    #Création Excel
    writer3 = WriteExcel("Hypothèse 3")
    writer_reduced3 = WriteExcelReduced("Hypothèse 3")
    
    #Entraînement de l'IA
    game(1000,11,sheetname="IA n°1 commence",writer=writer3, writer_reduced=writer_reduced3)
    game(1000,11,sheetname="IA n°2 commence",writer=writer3, writer_reduced=writer_reduced3,first_player = "Machine 2")

    #Fermeture du excel
    writer3.close_workbook()
    writer_reduced3.close_workbook()
    print("H3")

    
def hypothese4():
    """
    Fonction principale permettant de créer les données pour l'hypothèse 4
    :return: Ne retourne rien.
    """
    #Création Excel
    writer4 = WriteExcel("Hypothèse 4")
    writer_reduced4 = WriteExcelReduced("Hypothèse 4")
    
    #Entraînement de l'IA
    game(1000,11,sheetname="2 choix",table_color = {"yellow": 1, "red": 2},writer=writer4, writer_reduced=writer_reduced4)
    game(1000,11,sheetname="3 choix",table_color = {"yellow": 1, "red": 2, "blue" : 3},writer=writer4, writer_reduced=writer_reduced4)
    game(1000,11,sheetname="4 choix",table_color = {"yellow": 1, "red": 2, "blue": 3, "black" : 4},writer=writer4, writer_reduced=writer_reduced4)
    
    #Fermeture du excel
    writer4.close_workbook()
    writer_reduced4.close_workbook()

def hypothese5():
    """
    Fonction principale permettant de créer les données pour l'hypothèse 5
    :return: Ne retourne rien.
    """
    #Création Excel
    writer5 = WriteExcel("Hypothèse 5")
    writer_reduced5 = WriteExcelReduced("Hypothèse 5")
    
    #Entraînement de l'IA
    game_random(1000,11,sheetname="Random",table_color = {"yellow": 1, "red": 2},writer=writer5, writer_reduced=writer_reduced5)
    game(1000,11,sheetname="Machines",table_color = {"yellow": 1, "red": 2},writer=writer5, writer_reduced=writer_reduced5)
    
    #Fermeture du excel
    writer5.close_workbook()
    writer_reduced5.close_workbook()
    
def show_chart_h1():
    """
    Fonction principale permettant d'afficher le graphique vérifiant l'hypothèse 1
    :return: Ne retourne rien.
    """
    dfs_h1 = load_stats("Hypothèse 1_reduced.xlsx",
                        ["11 allumettes", "20 allumettes", "29 allumettes"])
    bars_hypothese1(dfs_h1, 200)


def show_chart_h2():
    """
    Fonction principale permettant d'afficher le graphique vérifiant l'hypothèse 2
    :return: Ne retourne rien.
    """
    dfs_h2 = load_stats("Hypothèse 2_reduced.xlsx",
                        ["Punition et récompense = 1",
                         "Punition et récompense = 3",
                         "Punition et récompense = 5",
                         "Punition et récompense = 6"])
    bars_hypothese2(dfs_h2)


def show_chart_h3():
    """
    Fonction principale permettant d'afficher le graphique vérifiant l'hypothèse 3
    :return: Ne retourne rien.
    """
    df_h3 = load_stats("Hypothèse 3_reduced.xlsx",
                       ["IA n°1 commence","IA n°2 commence"])
    bars_hypothese3(df_h3)



def show_chart_h4():
    """
    Fonction principale permettant d'afficher le graphique vérifiant l'hypothèse 4
    :return: Ne retourne rien.
    """
    dfs_h4 = load_stats("Hypothèse 4_reduced.xlsx",
                        ["2 choix", "3 choix", "4 choix"])
    bars_hypothese4(dfs_h4)

def show_chart_h5():
    """
    Fonction principale permettant d'afficher le graphique vérifiant l'hypothèse 5
    :return: Ne retourne rien.
    """
    dfs_h5 = load_stats("Hypothèse 5_reduced.xlsx",
                        ["Random", "Machines"])
    bars_hypothese5(dfs_h5)


if __name__ == "__main__":
    create_data()
    show_all_charts()