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
game_height = 5

def add_game():
    worksheet.merge_range(
        games_offset+game_height*(game_counter-1), 0,
        games_offset+game_height*game_counter, 0,
        game_counter, games_titles_format
    )
    
    
game_counter += 1
add_game()
game_counter += 1
#add_game()







worksheet.autofit()
workbook.close()