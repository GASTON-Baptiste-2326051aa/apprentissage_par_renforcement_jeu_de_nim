import xlsxwriter
import json


class WriteExcel:
    def __init__(self, path):
        self.workbook = xlsxwriter.Workbook(path)
        self.formats = AddFormat(self.workbook)
        self.worksheet: WriteSheet = None
    
    def add_sheet(self, name, matches, take, default_count, reward, punishment):
        if self.worksheet != None:
            self.worksheet.autofit_worksheet()
        
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
        if self.worksheet != None:
            self.worksheet.autofit_worksheet()
        self.workbook.close()

class AddFormat:
    def __init__(self, workbook: xlsxwriter.Workbook):
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
    def __init__(self, workbook: xlsxwriter.Workbook, name, matches, take, default_count, reward, punishment, formats: AddFormat):
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
    
    
    def add_game(self, results, steps_p1, steps_p2, cups_p1, cups_p2, cups_reseted_p1 = [], cups_reseted_p2 = []):
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
            self.worksheet.write(first_row, self.states_offset+self.matches-1-step[0], self.take[step[1]], self.formats.glob_values_format)
        
        for step in steps_p2:
            self.worksheet.write(first_row+1, self.states_offset+self.matches-1-step[0], self.take[step[1]], self.formats.glob_values_format)
        
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
        self.worksheet.autofit()


matches = 8
take = {"red": 1, "yellow": 2, "blue": 4}
default_count = 5
reward = 2
punishment = 1

writer = WriteExcel("../test.xlsx")
writer.add_sheet("test", matches, take, default_count, reward, punishment)
writer.worksheet.add_game({"P1": "gagne", "P2": "perd"}, [[7, 'red'], [4, 'yellow'], [1, 'yellow']], [[6, 'yellow'], [2, 'red']], [['red', 'yellow', 'red', 'yellow', 'red', 'yellow'], ['red', 'yellow', 'red', 'yellow', 'red', 'yellow', 'red', 'red'], ['red', 'yellow', 'red', 'yellow', 'red', 'yellow'], ['red', 'yellow', 'red', 'yellow', 'red', 'yellow'], ['red', 'yellow', 'red', 'yellow', 'red', 'yellow', 'yellow', 'yellow'], ['red', 'yellow', 'red', 'yellow', 'red', 'yellow'], ['red', 'yellow', 'red', 'yellow', 'red', 'yellow'], ['yellow', 'yellow', 'yellow', 'yellow', 'yellow']], [['red', 'yellow', 'red', 'yellow', 'red', 'yellow'], ['red', 'yellow', 'red', 'yellow', 'red', 'yellow', 'red', 'red'], ['red', 'yellow', 'red', 'yellow', 'red', 'yellow'], ['red', 'yellow', 'red', 'yellow', 'red', 'yellow'], ['red', 'yellow', 'red', 'yellow', 'red', 'yellow', 'yellow', 'yellow'], ['red', 'yellow', 'red', 'yellow', 'red', 'yellow'], ['red', 'yellow', 'red', 'yellow', 'red', 'yellow'], ['yellow', 'yellow', 'yellow', 'yellow', 'yellow']])
writer.worksheet.add_game({"P2": "perd"}, [[7, 'red'], [4, 'yellow'], [1, 'yellow']], [[6, 'yellow'], [2, 'red']], [['red', 'yellow', 'red', 'yellow', 'red', 'yellow'], ['red', 'yellow', 'red', 'yellow', 'red', 'yellow', 'red', 'red'], ['red', 'yellow', 'red', 'yellow', 'red', 'yellow'], ['red', 'yellow', 'red', 'yellow', 'red', 'yellow'], ['red', 'yellow', 'red', 'yellow', 'red', 'yellow', 'yellow', 'yellow'], ['red', 'yellow', 'red', 'yellow', 'red', 'yellow'], ['red', 'yellow', 'red', 'yellow', 'red', 'yellow'], ['yellow', 'yellow', 'yellow', 'yellow', 'yellow']], [[]], cups_reseted_p1 = ["8", "3"])
writer.worksheet.add_game({"P1": "gagne"}, [[7, 'red'], [4, 'yellow'], [1, 'yellow']], [[6, 'yellow'], [2, 'red']], [[]], [['red', 'yellow', 'red', 'yellow', 'red', 'yellow'], ['red', 'yellow', 'red', 'yellow', 'red', 'yellow', 'red', 'red'], ['red', 'yellow', 'red', 'yellow', 'red', 'yellow'], ['red', 'yellow', 'red', 'yellow', 'red', 'yellow'], ['red', 'yellow', 'red', 'yellow', 'red', 'yellow', 'yellow', 'yellow'], ['red', 'yellow', 'red', 'yellow', 'red', 'yellow'], ['red', 'yellow', 'red', 'yellow', 'red', 'yellow'], ['yellow', 'yellow', 'yellow', 'yellow', 'yellow']], cups_reseted_p1 = ["8", "3"], cups_reseted_p2 = ["5", "2"])
writer.worksheet.add_game({}, [[7, 'red'], [4, 'yellow'], [1, 'yellow']], [[6, 'yellow'], [2, 'red']], [[]], [[]], cups_reseted_p2 = ["5", "2"])
writer.add_sheet("test", matches, take, default_count, reward, punishment)
writer.worksheet.add_game({"P1": "gagne", "P2": "perd"}, [[7, 'red'], [4, 'yellow'], [1, 'yellow']], [[6, 'yellow'], [2, 'red']], [['red', 'yellow', 'red', 'yellow', 'red', 'yellow'], ['red', 'yellow', 'red', 'yellow', 'red', 'yellow', 'red', 'red'], ['red', 'yellow', 'red', 'yellow', 'red', 'yellow'], ['red', 'yellow', 'red', 'yellow', 'red', 'yellow'], ['red', 'yellow', 'red', 'yellow', 'red', 'yellow', 'yellow', 'yellow'], ['red', 'yellow', 'red', 'yellow', 'red', 'yellow'], ['red', 'yellow', 'red', 'yellow', 'red', 'yellow'], ['yellow', 'yellow', 'yellow', 'yellow', 'yellow']], [['red', 'yellow', 'red', 'yellow', 'red', 'yellow'], ['red', 'yellow', 'red', 'yellow', 'red', 'yellow', 'red', 'red'], ['red', 'yellow', 'red', 'yellow', 'red', 'yellow'], ['red', 'yellow', 'red', 'yellow', 'red', 'yellow'], ['red', 'yellow', 'red', 'yellow', 'red', 'yellow', 'yellow', 'yellow'], ['red', 'yellow', 'red', 'yellow', 'red', 'yellow'], ['red', 'yellow', 'red', 'yellow', 'red', 'yellow'], ['yellow', 'yellow', 'yellow', 'yellow', 'yellow']])
writer.worksheet.add_game({"P2": "perd"}, [[7, 'red'], [4, 'yellow'], [1, 'yellow']], [[6, 'yellow'], [2, 'red']], [['red', 'yellow', 'red', 'yellow', 'red', 'yellow'], ['red', 'yellow', 'red', 'yellow', 'red', 'yellow', 'red', 'red'], ['red', 'yellow', 'red', 'yellow', 'red', 'yellow'], ['red', 'yellow', 'red', 'yellow', 'red', 'yellow'], ['red', 'yellow', 'red', 'yellow', 'red', 'yellow', 'yellow', 'yellow'], ['red', 'yellow', 'red', 'yellow', 'red', 'yellow'], ['red', 'yellow', 'red', 'yellow', 'red', 'yellow'], ['yellow', 'yellow', 'yellow', 'yellow', 'yellow']], [[]], cups_reseted_p1 = ["8", "3"])
writer.worksheet.add_game({"P1": "gagne"}, [[7, 'red'], [4, 'yellow'], [1, 'yellow']], [[6, 'yellow'], [2, 'red']], [[]], [['red', 'yellow', 'red', 'yellow', 'red', 'yellow'], ['red', 'yellow', 'red', 'yellow', 'red', 'yellow', 'red', 'red'], ['red', 'yellow', 'red', 'yellow', 'red', 'yellow'], ['red', 'yellow', 'red', 'yellow', 'red', 'yellow'], ['red', 'yellow', 'red', 'yellow', 'red', 'yellow', 'yellow', 'yellow'], ['red', 'yellow', 'red', 'yellow', 'red', 'yellow'], ['red', 'yellow', 'red', 'yellow', 'red', 'yellow'], ['yellow', 'yellow', 'yellow', 'yellow', 'yellow']], cups_reseted_p1 = ["8", "3"], cups_reseted_p2 = ["5", "2"])
writer.worksheet.add_game({}, [[7, 'red'], [4, 'yellow'], [1, 'yellow']], [[6, 'yellow'], [2, 'red']], [[]], [[]], cups_reseted_p2 = ["5", "2"])
writer.add_sheet("test", matches, take, default_count, reward, punishment)
writer.worksheet.add_game({"P1": "gagne", "P2": "perd"}, [[7, 'red'], [4, 'yellow'], [1, 'yellow']], [[6, 'yellow'], [2, 'red']], [['red', 'yellow', 'red', 'yellow', 'red', 'yellow'], ['red', 'yellow', 'red', 'yellow', 'red', 'yellow', 'red', 'red'], ['red', 'yellow', 'red', 'yellow', 'red', 'yellow'], ['red', 'yellow', 'red', 'yellow', 'red', 'yellow'], ['red', 'yellow', 'red', 'yellow', 'red', 'yellow', 'yellow', 'yellow'], ['red', 'yellow', 'red', 'yellow', 'red', 'yellow'], ['red', 'yellow', 'red', 'yellow', 'red', 'yellow'], ['yellow', 'yellow', 'yellow', 'yellow', 'yellow']], [['red', 'yellow', 'red', 'yellow', 'red', 'yellow'], ['red', 'yellow', 'red', 'yellow', 'red', 'yellow', 'red', 'red'], ['red', 'yellow', 'red', 'yellow', 'red', 'yellow'], ['red', 'yellow', 'red', 'yellow', 'red', 'yellow'], ['red', 'yellow', 'red', 'yellow', 'red', 'yellow', 'yellow', 'yellow'], ['red', 'yellow', 'red', 'yellow', 'red', 'yellow'], ['red', 'yellow', 'red', 'yellow', 'red', 'yellow'], ['yellow', 'yellow', 'yellow', 'yellow', 'yellow']])
writer.worksheet.add_game({"P2": "perd"}, [[7, 'red'], [4, 'yellow'], [1, 'yellow']], [[6, 'yellow'], [2, 'red']], [['red', 'yellow', 'red', 'yellow', 'red', 'yellow'], ['red', 'yellow', 'red', 'yellow', 'red', 'yellow', 'red', 'red'], ['red', 'yellow', 'red', 'yellow', 'red', 'yellow'], ['red', 'yellow', 'red', 'yellow', 'red', 'yellow'], ['red', 'yellow', 'red', 'yellow', 'red', 'yellow', 'yellow', 'yellow'], ['red', 'yellow', 'red', 'yellow', 'red', 'yellow'], ['red', 'yellow', 'red', 'yellow', 'red', 'yellow'], ['yellow', 'yellow', 'yellow', 'yellow', 'yellow']], [[]], cups_reseted_p1 = ["8", "3"])
writer.worksheet.add_game({"P1": "gagne"}, [[7, 'red'], [4, 'yellow'], [1, 'yellow']], [[6, 'yellow'], [2, 'red']], [[]], [['red', 'yellow', 'red', 'yellow', 'red', 'yellow'], ['red', 'yellow', 'red', 'yellow', 'red', 'yellow', 'red', 'red'], ['red', 'yellow', 'red', 'yellow', 'red', 'yellow'], ['red', 'yellow', 'red', 'yellow', 'red', 'yellow'], ['red', 'yellow', 'red', 'yellow', 'red', 'yellow', 'yellow', 'yellow'], ['red', 'yellow', 'red', 'yellow', 'red', 'yellow'], ['red', 'yellow', 'red', 'yellow', 'red', 'yellow'], ['yellow', 'yellow', 'yellow', 'yellow', 'yellow']], cups_reseted_p1 = ["8", "3"], cups_reseted_p2 = ["5", "2"])
writer.worksheet.add_game({}, [[7, 'red'], [4, 'yellow'], [1, 'yellow']], [[6, 'yellow'], [2, 'red']], [[]], [[]], cups_reseted_p2 = ["5", "2"])
writer.add_sheet("test-1", matches, take, default_count, reward, punishment)
writer.worksheet.add_game({"P1": "gagne", "P2": "perd"}, [[7, 'red'], [4, 'yellow'], [1, 'yellow']], [[6, 'yellow'], [2, 'red']], [['red', 'yellow', 'red', 'yellow', 'red', 'yellow'], ['red', 'yellow', 'red', 'yellow', 'red', 'yellow', 'red', 'red'], ['red', 'yellow', 'red', 'yellow', 'red', 'yellow'], ['red', 'yellow', 'red', 'yellow', 'red', 'yellow'], ['red', 'yellow', 'red', 'yellow', 'red', 'yellow', 'yellow', 'yellow'], ['red', 'yellow', 'red', 'yellow', 'red', 'yellow'], ['red', 'yellow', 'red', 'yellow', 'red', 'yellow'], ['yellow', 'yellow', 'yellow', 'yellow', 'yellow']], [['red', 'yellow', 'red', 'yellow', 'red', 'yellow'], ['red', 'yellow', 'red', 'yellow', 'red', 'yellow', 'red', 'red'], ['red', 'yellow', 'red', 'yellow', 'red', 'yellow'], ['red', 'yellow', 'red', 'yellow', 'red', 'yellow'], ['red', 'yellow', 'red', 'yellow', 'red', 'yellow', 'yellow', 'yellow'], ['red', 'yellow', 'red', 'yellow', 'red', 'yellow'], ['red', 'yellow', 'red', 'yellow', 'red', 'yellow'], ['yellow', 'yellow', 'yellow', 'yellow', 'yellow']])
writer.worksheet.add_game({"P2": "perd"}, [[7, 'red'], [4, 'yellow'], [1, 'yellow']], [[6, 'yellow'], [2, 'red']], [['red', 'yellow', 'red', 'yellow', 'red', 'yellow'], ['red', 'yellow', 'red', 'yellow', 'red', 'yellow', 'red', 'red'], ['red', 'yellow', 'red', 'yellow', 'red', 'yellow'], ['red', 'yellow', 'red', 'yellow', 'red', 'yellow'], ['red', 'yellow', 'red', 'yellow', 'red', 'yellow', 'yellow', 'yellow'], ['red', 'yellow', 'red', 'yellow', 'red', 'yellow'], ['red', 'yellow', 'red', 'yellow', 'red', 'yellow'], ['yellow', 'yellow', 'yellow', 'yellow', 'yellow']], [[]], cups_reseted_p1 = ["8", "3"])
writer.worksheet.add_game({"P1": "gagne"}, [[7, 'red'], [4, 'yellow'], [1, 'yellow']], [[6, 'yellow'], [2, 'red']], [[]], [['red', 'yellow', 'red', 'yellow', 'red', 'yellow'], ['red', 'yellow', 'red', 'yellow', 'red', 'yellow', 'red', 'red'], ['red', 'yellow', 'red', 'yellow', 'red', 'yellow'], ['red', 'yellow', 'red', 'yellow', 'red', 'yellow'], ['red', 'yellow', 'red', 'yellow', 'red', 'yellow', 'yellow', 'yellow'], ['red', 'yellow', 'red', 'yellow', 'red', 'yellow'], ['red', 'yellow', 'red', 'yellow', 'red', 'yellow'], ['yellow', 'yellow', 'yellow', 'yellow', 'yellow']], cups_reseted_p1 = ["8", "3"], cups_reseted_p2 = ["5", "2"])
writer.worksheet.add_game({}, [[7, 'red'], [4, 'yellow'], [1, 'yellow']], [[6, 'yellow'], [2, 'red']], [[]], [[]], cups_reseted_p2 = ["5", "2"])
writer.add_sheet("test-5", matches, take, default_count, reward, punishment)
writer.worksheet.add_game({"P1": "gagne", "P2": "perd"}, [[7, 'red'], [4, 'yellow'], [1, 'yellow']], [[6, 'yellow'], [2, 'red']], [['red', 'yellow', 'red', 'yellow', 'red', 'yellow'], ['red', 'yellow', 'red', 'yellow', 'red', 'yellow', 'red', 'red'], ['red', 'yellow', 'red', 'yellow', 'red', 'yellow'], ['red', 'yellow', 'red', 'yellow', 'red', 'yellow'], ['red', 'yellow', 'red', 'yellow', 'red', 'yellow', 'yellow', 'yellow'], ['red', 'yellow', 'red', 'yellow', 'red', 'yellow'], ['red', 'yellow', 'red', 'yellow', 'red', 'yellow'], ['yellow', 'yellow', 'yellow', 'yellow', 'yellow']], [['red', 'yellow', 'red', 'yellow', 'red', 'yellow'], ['red', 'yellow', 'red', 'yellow', 'red', 'yellow', 'red', 'red'], ['red', 'yellow', 'red', 'yellow', 'red', 'yellow'], ['red', 'yellow', 'red', 'yellow', 'red', 'yellow'], ['red', 'yellow', 'red', 'yellow', 'red', 'yellow', 'yellow', 'yellow'], ['red', 'yellow', 'red', 'yellow', 'red', 'yellow'], ['red', 'yellow', 'red', 'yellow', 'red', 'yellow'], ['yellow', 'yellow', 'yellow', 'yellow', 'yellow']])
writer.worksheet.add_game({"P2": "perd"}, [[7, 'red'], [4, 'yellow'], [1, 'yellow']], [[6, 'yellow'], [2, 'red']], [['red', 'yellow', 'red', 'yellow', 'red', 'yellow'], ['red', 'yellow', 'red', 'yellow', 'red', 'yellow', 'red', 'red'], ['red', 'yellow', 'red', 'yellow', 'red', 'yellow'], ['red', 'yellow', 'red', 'yellow', 'red', 'yellow'], ['red', 'yellow', 'red', 'yellow', 'red', 'yellow', 'yellow', 'yellow'], ['red', 'yellow', 'red', 'yellow', 'red', 'yellow'], ['red', 'yellow', 'red', 'yellow', 'red', 'yellow'], ['yellow', 'yellow', 'yellow', 'yellow', 'yellow']], [[]], cups_reseted_p1 = ["8", "3"])
writer.worksheet.add_game({"P1": "gagne"}, [[7, 'red'], [4, 'yellow'], [1, 'yellow']], [[6, 'yellow'], [2, 'red']], [[]], [['red', 'yellow', 'red', 'yellow', 'red', 'yellow'], ['red', 'yellow', 'red', 'yellow', 'red', 'yellow', 'red', 'red'], ['red', 'yellow', 'red', 'yellow', 'red', 'yellow'], ['red', 'yellow', 'red', 'yellow', 'red', 'yellow'], ['red', 'yellow', 'red', 'yellow', 'red', 'yellow', 'yellow', 'yellow'], ['red', 'yellow', 'red', 'yellow', 'red', 'yellow'], ['red', 'yellow', 'red', 'yellow', 'red', 'yellow'], ['yellow', 'yellow', 'yellow', 'yellow', 'yellow']], cups_reseted_p1 = ["8", "3"], cups_reseted_p2 = ["5", "2"])
writer.worksheet.add_game({}, [[7, 'red'], [4, 'yellow'], [1, 'yellow']], [[6, 'yellow'], [2, 'red']], [[]], [[]], cups_reseted_p2 = ["5", "2"])
writer.add_sheet("test", matches, take, default_count, reward, punishment)
writer.worksheet.add_game({"P1": "gagne", "P2": "perd"}, [[7, 'red'], [4, 'yellow'], [1, 'yellow']], [[6, 'yellow'], [2, 'red']], [['red', 'yellow', 'red', 'yellow', 'red', 'yellow'], ['red', 'yellow', 'red', 'yellow', 'red', 'yellow', 'red', 'red'], ['red', 'yellow', 'red', 'yellow', 'red', 'yellow'], ['red', 'yellow', 'red', 'yellow', 'red', 'yellow'], ['red', 'yellow', 'red', 'yellow', 'red', 'yellow', 'yellow', 'yellow'], ['red', 'yellow', 'red', 'yellow', 'red', 'yellow'], ['red', 'yellow', 'red', 'yellow', 'red', 'yellow'], ['yellow', 'yellow', 'yellow', 'yellow', 'yellow']], [['red', 'yellow', 'red', 'yellow', 'red', 'yellow'], ['red', 'yellow', 'red', 'yellow', 'red', 'yellow', 'red', 'red'], ['red', 'yellow', 'red', 'yellow', 'red', 'yellow'], ['red', 'yellow', 'red', 'yellow', 'red', 'yellow'], ['red', 'yellow', 'red', 'yellow', 'red', 'yellow', 'yellow', 'yellow'], ['red', 'yellow', 'red', 'yellow', 'red', 'yellow'], ['red', 'yellow', 'red', 'yellow', 'red', 'yellow'], ['yellow', 'yellow', 'yellow', 'yellow', 'yellow']])
writer.worksheet.add_game({"P2": "perd"}, [[7, 'red'], [4, 'yellow'], [1, 'yellow']], [[6, 'yellow'], [2, 'red']], [['red', 'yellow', 'red', 'yellow', 'red', 'yellow'], ['red', 'yellow', 'red', 'yellow', 'red', 'yellow', 'red', 'red'], ['red', 'yellow', 'red', 'yellow', 'red', 'yellow'], ['red', 'yellow', 'red', 'yellow', 'red', 'yellow'], ['red', 'yellow', 'red', 'yellow', 'red', 'yellow', 'yellow', 'yellow'], ['red', 'yellow', 'red', 'yellow', 'red', 'yellow'], ['red', 'yellow', 'red', 'yellow', 'red', 'yellow'], ['yellow', 'yellow', 'yellow', 'yellow', 'yellow']], [[]], cups_reseted_p1 = ["8", "3"])
writer.worksheet.add_game({"P1": "gagne"}, [[7, 'red'], [4, 'yellow'], [1, 'yellow']], [[6, 'yellow'], [2, 'red']], [[]], [['red', 'yellow', 'red', 'yellow', 'red', 'yellow'], ['red', 'yellow', 'red', 'yellow', 'red', 'yellow', 'red', 'red'], ['red', 'yellow', 'red', 'yellow', 'red', 'yellow'], ['red', 'yellow', 'red', 'yellow', 'red', 'yellow'], ['red', 'yellow', 'red', 'yellow', 'red', 'yellow', 'yellow', 'yellow'], ['red', 'yellow', 'red', 'yellow', 'red', 'yellow'], ['red', 'yellow', 'red', 'yellow', 'red', 'yellow'], ['yellow', 'yellow', 'yellow', 'yellow', 'yellow']], cups_reseted_p1 = ["8", "3"], cups_reseted_p2 = ["5", "2"])
writer.worksheet.add_game({}, [[7, 'red'], [4, 'yellow'], [1, 'yellow']], [[6, 'yellow'], [2, 'red']], [[]], [[]], cups_reseted_p2 = ["5", "2"])
writer.add_sheet("test", matches, take, default_count, reward, punishment)
writer.worksheet.add_game({"P1": "gagne", "P2": "perd"}, [[7, 'red'], [4, 'yellow'], [1, 'yellow']], [[6, 'yellow'], [2, 'red']], [['red', 'yellow', 'red', 'yellow', 'red', 'yellow'], ['red', 'yellow', 'red', 'yellow', 'red', 'yellow', 'red', 'red'], ['red', 'yellow', 'red', 'yellow', 'red', 'yellow'], ['red', 'yellow', 'red', 'yellow', 'red', 'yellow'], ['red', 'yellow', 'red', 'yellow', 'red', 'yellow', 'yellow', 'yellow'], ['red', 'yellow', 'red', 'yellow', 'red', 'yellow'], ['red', 'yellow', 'red', 'yellow', 'red', 'yellow'], ['yellow', 'yellow', 'yellow', 'yellow', 'yellow']], [['red', 'yellow', 'red', 'yellow', 'red', 'yellow'], ['red', 'yellow', 'red', 'yellow', 'red', 'yellow', 'red', 'red'], ['red', 'yellow', 'red', 'yellow', 'red', 'yellow'], ['red', 'yellow', 'red', 'yellow', 'red', 'yellow'], ['red', 'yellow', 'red', 'yellow', 'red', 'yellow', 'yellow', 'yellow'], ['red', 'yellow', 'red', 'yellow', 'red', 'yellow'], ['red', 'yellow', 'red', 'yellow', 'red', 'yellow'], ['yellow', 'yellow', 'yellow', 'yellow', 'yellow']])
writer.worksheet.add_game({"P2": "perd"}, [[7, 'red'], [4, 'yellow'], [1, 'yellow']], [[6, 'yellow'], [2, 'red']], [['red', 'yellow', 'red', 'yellow', 'red', 'yellow'], ['red', 'yellow', 'red', 'yellow', 'red', 'yellow', 'red', 'red'], ['red', 'yellow', 'red', 'yellow', 'red', 'yellow'], ['red', 'yellow', 'red', 'yellow', 'red', 'yellow'], ['red', 'yellow', 'red', 'yellow', 'red', 'yellow', 'yellow', 'yellow'], ['red', 'yellow', 'red', 'yellow', 'red', 'yellow'], ['red', 'yellow', 'red', 'yellow', 'red', 'yellow'], ['yellow', 'yellow', 'yellow', 'yellow', 'yellow']], [[]], cups_reseted_p1 = ["8", "3"])
writer.worksheet.add_game({"P1": "gagne"}, [[7, 'red'], [4, 'yellow'], [1, 'yellow']], [[6, 'yellow'], [2, 'red']], [[]], [['red', 'yellow', 'red', 'yellow', 'red', 'yellow'], ['red', 'yellow', 'red', 'yellow', 'red', 'yellow', 'red', 'red'], ['red', 'yellow', 'red', 'yellow', 'red', 'yellow'], ['red', 'yellow', 'red', 'yellow', 'red', 'yellow'], ['red', 'yellow', 'red', 'yellow', 'red', 'yellow', 'yellow', 'yellow'], ['red', 'yellow', 'red', 'yellow', 'red', 'yellow'], ['red', 'yellow', 'red', 'yellow', 'red', 'yellow'], ['yellow', 'yellow', 'yellow', 'yellow', 'yellow']], cups_reseted_p1 = ["8", "3"], cups_reseted_p2 = ["5", "2"])
writer.worksheet.add_game({}, [[7, 'red'], [4, 'yellow'], [1, 'yellow']], [[6, 'yellow'], [2, 'red']], [[]], [[]], cups_reseted_p2 = ["5", "2"])
writer.close_workbook()