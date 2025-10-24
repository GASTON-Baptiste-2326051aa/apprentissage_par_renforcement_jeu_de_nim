import xlsxwriter
import json

workbook = xlsxwriter.Workbook('Téléchargements/example2.xlsx')
worksheet = workbook.add_worksheet("test")

glob_titles_format = workbook.add_format({
    "bold": 1,
    "bg_color": "#999999",
    "font_color": "white",
    "align": "center"
})
glob_values_format = workbook.add_format({
    "align": "center"
})
games_titles_format = workbook.add_format({
    "bold": 1,
    "align": "center",
    "valign": "vcenter"
})
bold = workbook.add_format({
    "bold": 1
})


matches = 8
take = {"red": 1, "yellow": 2}
default_proba = 0.5
default_count = 5
recompense = 2
punition = 1

game_counter = 0

glob_titles = ["max allumettes", "coups possibles", "proba initiale de chaque coup", "nb billes/couleur", "récompense", "punition"]
glob_values = [matches, take, default_proba, default_count, recompense, punition]

for i in range(len(glob_titles)):
    worksheet.write(0, i, glob_titles[i], glob_titles_format)
for i in range(len(glob_values)):
    worksheet.write(1, i, json.dumps(glob_values[i]), glob_values_format)

titles = ["num parties", "joueur", "résultat", "gobelets réinitialisés", "allumettes retirées"]
for i in range(len(titles)):
    worksheet.write(4, i, titles[i], glob_titles_format)

states_offset = len(titles)+1
worksheet.write(5, states_offset-1, "état", glob_titles_format)
for i in range(matches):
    worksheet.write(5, states_offset+i, 8-i, glob_titles_format)

games_offset = 7
game_height = 6

def add_game(results, steps_p1, steps_p2, cups_p1, cups_p2, cups_reseted_p1 = [], cups_reseted_p2 = []):
    first_row = games_offset+game_height*(game_counter-1)
    last_row = games_offset+game_height*game_counter-1
    worksheet.merge_range(
        first_row, 0,
        last_row, 0,
        game_counter, games_titles_format
    )
    worksheet.write(first_row, 1, "P1", games_titles_format)
    worksheet.write(first_row+1, 1, "P2", games_titles_format)
    worksheet.merge_range(
        first_row+2, 1,
        first_row+3, 1,
        "P1", games_titles_format
    )
    worksheet.merge_range(
        first_row+4, 1,
        first_row+5, 1,
        "P2", games_titles_format
    )
    
    worksheet.write(first_row, 3, json.dumps(cups_reseted_p1) if len(cups_reseted_p1) > 0 else "-")
    worksheet.write(first_row+1, 3, json.dumps(cups_reseted_p2) if len(cups_reseted_p2) > 0 else "-")


    
game_counter += 1
add_game({"P1": "gagne", "P2": "perd"}, [[5, 'red'], [2, 'red']], [[7, 'red'], [3, 'yellow']], [], [])
game_counter += 1
add_game({"P1": "gagne", "P2": "perd"}, [[5, 'red'], [2, 'red']], [[7, 'red'], [3, 'yellow']], [], [], cups_reseted_p1 = ["8", "3"])
game_counter += 1
add_game({"P1": "gagne", "P2": "perd"}, [[5, 'red'], [2, 'red']], [[7, 'red'], [3, 'yellow']], [], [], cups_reseted_p1 = ["8", "3"], cups_reseted_p2 = ["5", "2"])
game_counter += 1
add_game({"P1": "gagne", "P2": "perd"}, [[5, 'red'], [2, 'red']], [[7, 'red'], [3, 'yellow']], [], [], cups_reseted_p2 = ["5", "2"])







worksheet.autofit()
workbook.close()