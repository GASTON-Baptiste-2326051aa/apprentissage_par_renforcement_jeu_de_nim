import xlsxwriter
import json


class WriteExcelReduced:
    """
    Classe créant un fichier excel et gérant son édition (version réduite)
    """

    def __init__(self, path: str):
        """
        Fonction d'initialisation des instances de la classe WriteExcelReduced.
        Initialise un fichier excel, une feuille de calcul et les formatages des cellules nécessaires.
        :param path: Chemin du fichier excel
        """

        self.workbook = xlsxwriter.Workbook(path+"_reduced.xlsx")
        self.worksheet: WriteSheet = None
        self.game_counter = None

        self.glob_titles_format = self.workbook.add_format({
            "bold": 1,
            "bg_color": "#999999",
            "font_color": "white",
            "align": "center"
        })
        self.glob_values_format = self.workbook.add_format({
            "align": "center"
        })
    
    def add_sheet(self, name):
        """
        Ajoute et initialise une nouvelle feuille de calcul au fichier excel et réinitialise le compteur de parties.
        :param name: Nom de la feuille
        """

        if self.worksheet != None:
            self.worksheet.autofit()  # Pour une mise en page propre et lisible de la feuille
        
        # Gère les noms des feuilles (évite les doublons)
        while (True):
            try:
                self.worksheet = self.workbook.add_worksheet(name)
                self.setup()
                self.game_counter = 0
                break
            except:
                last_occ = name.rfind('-')
                if last_occ > -1:
                    number = name[last_occ+1:]
                    if number.isdigit():
                        name = name[:last_occ+1]+str(int(number)+1)
                    else:
                        name += "-1"
                else:
                    name += "-1"
    
    def setup(self):
        """
        Prépare la feuille en y écrivant les paramètres du jeu et les intitulés des colonnes.
        """
        
        self.worksheet.write(0, 0, "Partie", self.glob_titles_format)
        self.worksheet.write(0, 1, "Gagnant", self.glob_titles_format)

    def add_game(self, winner):
        """
        Rajoute les données associées à une partie sur la feuille.
        :param winner: Le joueur ayant gagné la partie
        """

        self.game_counter += 1
        self.worksheet.write(self.game_counter, 0, self.game_counter, self.glob_values_format)
        self.worksheet.write(self.game_counter, 1, winner, self.glob_values_format)
    
    def close_workbook(self):
        """
        Ferme le fichier excel en édition.
        """

        if self.worksheet != None:
            self.worksheet.autofit()
        self.workbook.close()
        




class WriteExcel:
    """
    Classe créant un fichier excel et gérant son édition.
    """

    def __init__(self, path: str):
        """
        Fonction d'initialisation des instances de la classe WriteExcel.
        Initialise un fichier excel, une instance des formatages des cellules nécessaires pour le excel et une instance de feuille de calcul.
        :param path: Chemin du fichier excel
        """

        self.workbook = xlsxwriter.Workbook(path+".xlsx")
        self.formats = AddFormat(self.workbook)
        self.worksheet: WriteSheet = None
    
    def add_sheet(self, name, matches, take, default_count, reward, punishment):
        """
        Ajoute et initialise une nouvelle feuille de calcul au fichier excel.
        :param name: Nom de la feuille
        :param: matches: Nombre d'allumettes du jeu
        :param take: Les différents coups possibles du jeu
        :param default_count: Le nombre de billes de chaque couleur dans chaque gobelet au moment de l'initialisation
        :param reward: La récompense en cas de victoire
        :param punishment: La punition en cas de défaite
        """

        if self.worksheet != None:
            self.worksheet.autofit_worksheet()  # Pour une mise en page propre et lisible de la feuille
        
        # Gère les noms des feuilles (évite les doublons)
        while (True):
            try:
                self.worksheet = WriteSheet(self.workbook, name, matches, take, default_count, reward, punishment, self.formats)
                break
            except:
                last_occ = name.rfind('-')
                if last_occ > -1:
                    number = name[last_occ+1:]
                    if number.isdigit():
                        name = name[:last_occ+1]+str(int(number)+1)
                    else:
                        name += "-1"
                else:
                    name += "-1"
    
    def close_workbook(self):
        """
        Ferme le fichier excel en édition.
        """

        if self.worksheet != None:
            self.worksheet.autofit_worksheet()
        self.workbook.close()


class AddFormat:
    """
    Classe créant les différents formatages des cellules nécessaires pour un fichier excel donné.
    """

    def __init__(self, workbook: xlsxwriter.Workbook):
        """
        Fonction d'initialisation des instances de la classe AddFormat.
        Initialise tous les différents formatages des cellules qui seront utilisés pour le fichier excel passé en paramètre.
        :param workbook: Le fichier excel
        """

        self.glob_titles_format = workbook.add_format({
            "bold": 1,
            "bg_color": "#999999",
            "font_color": "white",
            "align": "center"
        })
        self.glob_values_format = workbook.add_format({
            "align": "center"
        })
        self.games_titles_format = workbook.add_format({
            "bold": 1,
            "align": "center",
            "valign": "vcenter"
        })
        self.no_step = workbook.add_format({
            "bg_color": "black"
        })

class WriteSheet:
    """
    Classe créant une feuille de calcul pour un fichier excel donné et gérant son édition.
    """

    def __init__(self, workbook: xlsxwriter.Workbook, name, matches, take, default_count, reward, punishment, formats: AddFormat):
        """
        Fonction d'initialisation des instances de la classe WriteSheet.
        Initialise une feuille de calcul et y écrit les paramètres du jeu.
        :param workbook: Le fichier excel
        :param name: Nom de la feuille
        :param: matches: Nombre d'allumettes du jeu
        :param take: Les différents coups possibles du jeu
        :param default_count: Le nombre de billes de chaque couleur dans chaque gobelet au moment de l'initialisation
        :param reward: La récompense en cas de victoire
        :param punishment: La punition en cas de défaite
        :param formats: Instance de la classe AddFormat
        """

        self.workbook = workbook
        self.worksheet = self.workbook.add_worksheet(name)
        
        self.game_counter = 0
        self.matches = matches
        self.take = take
        self.default_count = default_count
        self.reward = reward
        self.punishment = punishment

        self.nb_take = len(self.take)
        self.games_offset = 7
        self.game_height = 2 + 2*self.nb_take
        self.states_offset = 6

        self.formats = formats

        self.setup()
    
    
    def setup(self):
        """
        Prépare la feuille en y écrivant les paramètres du jeu et les intitulés des colonnes.
        """

        glob_titles = ["max allumettes", "coups possibles", "proba initiale de chaque coup", "nb billes/couleur", "récompense", "punition"]
        glob_values = [self.matches, self.take, round(1/(self.nb_take), 3), self.default_count, self.reward, self.punishment]
        
        for i in range(len(glob_titles)):
            self.worksheet.write(0, i, glob_titles[i], self.formats.glob_titles_format)
        for i in range(len(glob_values)):
            self.worksheet.write(1, i, json.dumps(glob_values[i]), self.formats.glob_values_format)
        
        titles = ["num parties", "joueur", "résultat", "gobelets réinitialisés", "allumettes retirées"]
        for i in range(len(titles)):
            self.worksheet.write(4, i, titles[i], self.formats.glob_titles_format)
        
        self.worksheet.write(5, self.states_offset-1, "état", self.formats.glob_titles_format)
        for i in range(self.matches):
            self.worksheet.write(5, self.states_offset+i, self.matches-i, self.formats.glob_titles_format)
    
    
    def add_game(self, results, score_p1, score_p2, steps_p1, steps_p2, cups_p1, cups_p2, cups_reseted_p1 = [], cups_reseted_p2 = []):
        """
        Rajoute les données associées à une partie sur la feuille.
        :param results: Tableau indiquant quel joueur a gagné et quel joueur a perdu la partie
        :param score_p1: Score du joueur 1 après la partie
        :param score_p2: Score du joueur 2 après la partie
        :param steps_p1: Tableau retraçant les coups joués par le joueur 1
        :param steps_p2: Tableau retraçant les coups joués par le joueur 2
        :param cups_p1: Tableau contenant l'état des gobelets du joueur 1 après application des récompenses et punitions
        :param cups_p2: Tableau contenant l'état des gobelets du joueur 2 après application des récompenses et punitions
        :param cups_reseted_p1: Tableau contenant la liste des gobelets du joueur 1 qui ont été complètement vidés par la punition après la partie et qui ont dû être réinitialisés
        :param cups_reseted_p2: Tableau contenant la liste des gobelets du joueur 2 qui ont été complètement vidés par la punition après la partie et qui ont dû être réinitialisés
        """

        self.game_counter += 1
        
        first_row = self.games_offset+self.game_height*(self.game_counter-1)
        last_row = self.games_offset+self.game_height*self.game_counter-1
        
        self.worksheet.merge_range(
            first_row, 0,
            last_row, 0,
            self.game_counter, self.formats.games_titles_format
        )
        
        self.worksheet.write(first_row, 1, "P1", self.formats.games_titles_format)
        self.worksheet.write(first_row+1, 1, "P2", self.formats.games_titles_format)
        
        self.worksheet.write(first_row, 2, score_p1, self.formats.games_titles_format)
        self.worksheet.write(first_row+1, 2, score_p2, self.formats.games_titles_format)
        
        self.worksheet.merge_range(
            first_row+2, 1,
            first_row+1+self.nb_take, 1,
            "P1", self.formats.games_titles_format
        )
        self.worksheet.merge_range(
            first_row+2+self.nb_take, 1,
            first_row+1+self.nb_take*2, 1,
            "P2", self.formats.games_titles_format
        )
        
        players = list(results.keys())
        self.worksheet.merge_range(
            first_row+2, 2,
            first_row+1+self.nb_take, 2,
            results["P1"] if "P1" in players else "no data", self.formats.games_titles_format
        )
        self.worksheet.merge_range(
            first_row+2+self.nb_take, 2,
            first_row+1+self.nb_take*2, 2,
            results["P2"] if "P2" in players else "no data", self.formats.games_titles_format
        )
        
        self.worksheet.write(first_row, 3, json.dumps(cups_reseted_p1) if len(cups_reseted_p1) > 0 else "-", self.formats.glob_values_format)
        self.worksheet.write(first_row+1, 3, json.dumps(cups_reseted_p2) if len(cups_reseted_p2) > 0 else "-", self.formats.glob_values_format)
        
        counter = 0
        for nb_matches in self.take.values():
            counter += 1
            self.worksheet.write(first_row+1+counter, 4, nb_matches)
            self.worksheet.write(first_row+1+counter+self.nb_take, 4, nb_matches)
        
        for step in steps_p1:
            self.worksheet.write(first_row, self.states_offset+step[0], self.take[step[1]], self.formats.glob_values_format)
        
        for step in steps_p2:
            self.worksheet.write(first_row+1, self.states_offset+step[0], self.take[step[1]], self.formats.glob_values_format)
        
        self.worksheet.conditional_format(first_row, self.states_offset, first_row+1, self.states_offset+self.matches-1, {
            'type':'blanks',
            'format': self.formats.no_step
        })
        
        for cup_index in range(len(cups_p1)):
            cup = cups_p1[cup_index]
            if (len(cup) == 0):
                continue
            counter = 0
            for color in self.take:
                counter += 1
                self.worksheet.write(first_row+1+counter, self.states_offset+cup_index, round(cup.count(color)/max(len(cup), 1), 3), self.formats.glob_values_format)
        
        for cup_index in range(len(cups_p2)):
            cup = cups_p2[cup_index]
            if (len(cup) == 0):
                continue
            counter = 0
            for color in self.take:
                counter += 1
                self.worksheet.write(first_row+1+self.nb_take+counter, self.states_offset+cup_index, round(cup.count(color)/max(len(cup), 1), 3), self.formats.glob_values_format)
    
    def autofit_worksheet(self):
        """
        Gère la mise en page de la feuille pour la rendre propre et lisible.
        """
        
        self.worksheet.autofit()