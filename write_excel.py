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
no_step = workbook.add_format({
    "bg_color": "black"
})


matches = 8
take = {"red": 1, "yellow": 2, "blue": 4}
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

nb_take = len(take)
games_offset = 7
game_height = 2 + 2*nb_take

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
        first_row+1+nb_take, 1,
        "P1", games_titles_format
    )
    worksheet.merge_range(
        first_row+2+nb_take, 1,
        first_row+1+nb_take*2, 1,
        "P2", games_titles_format
    )
    
    players = list(results.keys())
    worksheet.merge_range(
        first_row+2, 2,
        first_row+1+nb_take, 2,
        results["P1"] if "P1" in players else "no data", games_titles_format
    )
    worksheet.merge_range(
        first_row+2+nb_take, 2,
        first_row+1+nb_take*2, 2,
        results["P2"] if "P2" in players else "no data", games_titles_format
    )
    
    worksheet.write(first_row, 3, json.dumps(cups_reseted_p1) if len(cups_reseted_p1) > 0 else "-", glob_values_format)
    worksheet.write(first_row+1, 3, json.dumps(cups_reseted_p2) if len(cups_reseted_p2) > 0 else "-", glob_values_format)
    
    counter = 0
    for nb_matches in take.values():
        counter += 1
        worksheet.write(first_row+1+counter, 4, nb_matches)
        worksheet.write(first_row+1+counter+nb_take, 4, nb_matches)
    
    for step in steps_p1:
        worksheet.write(first_row, states_offset+matches-1-step[0], take[step[1]], glob_values_format)
    
    for step in steps_p2:
        worksheet.write(first_row+1, states_offset+matches-1-step[0], take[step[1]], glob_values_format)
    
    worksheet.conditional_format(first_row, states_offset, first_row+1, states_offset+7, {
        'type':'blanks',
        'format': no_step
    })
    
    


    
game_counter += 1
add_game({"P1": "gagne", "P2": "perd"}, [[7, 'red'], [4, 'yellow'], [1, 'yellow']], [[6, 'yellow'], [2, 'red']], [], [])
game_counter += 1
add_game({"P2": "perd"}, [[7, 'red'], [4, 'yellow'], [1, 'yellow']], [[6, 'yellow'], [2, 'red']], [], [], cups_reseted_p1 = ["8", "3"])
game_counter += 1
add_game({"P1": "gagne"}, [[7, 'red'], [4, 'yellow'], [1, 'yellow']], [[6, 'yellow'], [2, 'red']], [], [], cups_reseted_p1 = ["8", "3"], cups_reseted_p2 = ["5", "2"])
game_counter += 1
add_game({}, [[7, 'red'], [4, 'yellow'], [1, 'yellow']], [[6, 'yellow'], [2, 'red']], [], [], cups_reseted_p2 = ["5", "2"])







worksheet.autofit()
workbook.close()