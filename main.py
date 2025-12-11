from write_excel import WriteExcel, WriteExcelReduced
from game_machine_machine import game
from charts import load_stats, curve_hypothese1,curve_hypothese2,curve_hypothese3,curve_hypothese4,bars_hypothese1,bars_hypothese2,bars_hypothese3,bars_hypothese4
def create_data(): 
    hypothese1()
    hypothese2()
    hypothese3()
    hypothese4()
        


def hypothese1():
    print("H1")

    #Création Excel
    writer1 = WriteExcel("Hypothèse 1")
    writer_reduced1 = WriteExcelReduced("Hypothèse 1")
    
    game(2000,11,sheetname="11 allumettes", writer=writer1, writer_reduced=writer_reduced1)
    print("H1")
    game(2000,16,sheetname="16 allumettes", writer=writer1, writer_reduced=writer_reduced1)
    print("H1")
    game(2000,21,sheetname="20 allumettes", writer=writer1, writer_reduced=writer_reduced1)
    print("H1")
    
    writer1.close_workbook()
    writer_reduced1.close_workbook()
    
def hypothese2():
    #Création Excel
    writer2 = WriteExcel("Hypothèse 2")
    writer_reduced2 = WriteExcelReduced("Hypothèse 2")
    
    game(2000,11,1,1,sheetname="Punition et récompense = 1",writer=writer2, writer_reduced=writer_reduced2)
    print("H2")
    game(2000,11,3,3,sheetname="Punition et récompense = 3",writer=writer2, writer_reduced=writer_reduced2)
    print("H2")
    game(2000,11,5,5,sheetname="Punition et récompense = 5",writer=writer2, writer_reduced=writer_reduced2)
    print("H2")

    
    # Limite punition trop élevée
    
    writer2.close_workbook()
    writer_reduced2.close_workbook()
    
def hypothese3():
    print("H3")
    #Création Excel
    writer3 = WriteExcel("Hypothèse 3")
    writer_reduced3 = WriteExcelReduced("Hypothèse 3")
    
    game(2000,11,sheetname="IA n°1 commence",writer=writer3, writer_reduced=writer_reduced3)
    print("H3")
    
    writer3.close_workbook()
    writer_reduced3.close_workbook()
    
def hypothese4():
    print("H4")
    #Création Excel
    writer4 = WriteExcel("Hypothèse 4")
    writer_reduced4 = WriteExcelReduced("Hypothèse 4")
    
    game(2000,11,sheetname="2 choix",table_color = {"yellow": 1, "red": 2},writer=writer4, writer_reduced=writer_reduced4)
    print("H4")
    game(2000,11,sheetname="3 choix",table_color = {"yellow": 1, "red": 2, "blue" : 3},writer=writer4, writer_reduced=writer_reduced4)
    print("H4")
    game(2000,11,sheetname="4 choix",table_color = {"yellow": 1, "red": 2, "blue": 3, "black" : 4},writer=writer4, writer_reduced=writer_reduced4)
    print("H4")    
    writer4.close_workbook()
    writer_reduced4.close_workbook()
    
def show_graph_h1(type="bars"):
    dfs_h1 = load_stats("Hypothèse 1_reduced.xlsx",
                        ["11 allumettes", "16 allumettes", "20 allumettes"])

    match type:
        case "curve":
            curve_hypothese1(dfs_h1)
        case "bars":
            bars_hypothese1(dfs_h1)
        case _:
            raise ValueError("type must be 'curve' or 'bars'")


def show_graph_h2(type="bars"):
    dfs_h2 = load_stats("Hypothèse 2_reduced.xlsx",
                        ["Punition et récompense = 1",
                         "Punition et récompense = 3",
                         "Punition et récompense = 5"])

    match type:
        case "curve":
            curve_hypothese2(dfs_h2)
        case "bars":
            bars_hypothese2(dfs_h2)
        case _:
            raise ValueError("type must be 'curve' or 'bars'")


def show_graph_h3(type="bars"):
    df_h3 = load_stats("Hypothèse 3_reduced.xlsx",
                       ["IA n°1 commence"])["IA n°1 commence"]

    match type:
        case "curve":
            curve_hypothese3(df_h3)
        case "bars":
            bars_hypothese3(df_h3)
        case _:
            raise ValueError("type must be 'curve' or 'bars'")


def show_graph_h4(type="bars"):
    dfs_h4 = load_stats("Hypothèse 4_reduced.xlsx",
                        ["2 choix", "3 choix", "4 choix"])

    match type:
        case "curve":
            curve_hypothese4(dfs_h4)
        case "bars":
            bars_hypothese4(dfs_h4)
        case _:
            raise ValueError("type must be 'curve' or 'bars'")



    

    