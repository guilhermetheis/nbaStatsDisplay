# -*- coding: utf-8 -*-
'''
Created on Mon Sep 11 08:37:17 2023

@author: Guilherme
'''

import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageDraw, ImageFont
from tkinter import filedialog
from nba_api.stats.endpoints import LeagueDashPlayerStats
from datetime import date
import tkinter.messagebox as messagebox
import re

## LUT Space

teamsID = {'Atlanta Hawks': 1610612737,
 'Boston Celtics': 1610612738,
 'Cleveland Cavaliers': 1610612739,
 'New Orleans Pelicans': 1610612740,
 'Chicago Bulls': 1610612741,
 'Dallas Mavericks': 1610612742,
 'Denver Nuggets': 1610612743,
 'Golden State Warriors': 1610612744,
 'Houston Rockets': 1610612745,
 'Los Angeles Clippers': 1610612746,
 'Los Angeles Lakers': 1610612747,
 'Miami Heat': 1610612748,
 'Milwaukee Bucks': 1610612749,
 'Minnesota Timberwolves': 1610612750,
 'Brooklyn Nets': 1610612751,
 'New York Knicks': 1610612752,
 'Orlando Magic': 1610612753,
 'Indiana Pacers': 1610612754,
 'Philadelphia 76ers': 1610612755,
 'Phoenix Suns': 1610612756,
 'Portland Trail Blazers': 1610612757,
 'Sacramento Kings': 1610612758,
 'San Antonio Spurs': 1610612759,
 'Oklahoma City Thunder': 1610612760,
 'Toronto Raptors': 1610612761,
 'Utah Jazz': 1610612762,
 'Memphis Grizzlies': 1610612763,
 'Washington Wizards': 1610612764,
 'Detroit Pistons': 1610612765,
 'Charlotte Hornets': 1610612766}

seasonTypes = ['Pre Season', 'All Star', 'Regular Season', 'Playoffs']

nGames = ['1', '5', '10', '20']

dTypes = ['Totals', 'PerGame', 'Per36']


def generate_report():
    selectedTeam = option1_var.get()
    selectedNGames = option3_var.get()
    selectedSType = option2_var.get()
    selectedMode = option4_var.get()
    
    data = LeagueDashPlayerStats(team_id_nullable=teamsID[selectedTeam], last_n_games=int(selectedNGames), season_type_all_star=selectedSType, per_mode_detailed=selectedMode)
    df = data.get_data_frames()[0]
    df = df[['PLAYER_NAME', 'PTS', 'AST', 'REB']]
    df = df.sort_values('PTS', ascending=False)
    
    myStr = ' '
    
    for index in df.index:
        myStr = myStr +  re.sub(r'^(\w)\w*', r'\1.', df['PLAYER_NAME'][index]) + ' ' + str(df['PTS'][index]) + '/' + str(df['AST'][index]) + '/' + str(df['REB'][index]) + ' | '
    
    
    font_size = int(font_size_entry.get())
    background_color = background_color_entry.get()
    text_color = text_color_entry.get()
    
    background_color_conv = tuple(int(background_color[i:i+2], 16) for i in (0, 2, 4))
    text_color_conv = tuple(int(text_color[i:i+2], 16) for i in (0, 2, 4))
    im = Image.new("RGB", (0, 0),background_color_conv)
    
    
    # Load a font (you may need to specify the font file path)
    font = ImageFont.truetype(file_path, font_size)
    
    _, _, *dim = ImageDraw.Draw(im).textbbox((0, 0), myStr, font=font)
    im = im.resize(dim)  # Resize to fit "perfectly"
    draw = ImageDraw.Draw(im)
    draw.text((0, 0), myStr, fill=text_color_conv, font=font)
    
    # Save the image as PNG
    im.save(selected_path+'/'+selectedTeam+date.today().strftime('%Y%m%d')+'.png')    
    
    # You can perform some action with the selected options here.
    # For this example, let's just print them.
    messagebox.showinfo('Image Generated', 'The image has been saved')
    print('Selected Path:', selected_path)

def select_path():
    global selected_path
    selected_path = filedialog.askdirectory()
    path_label.config(text='Selected Path: ' + selected_path)

def select_font_file():
    global file_path
    file_path = filedialog.askopenfilename(
        filetypes=[("TrueType Fonts", "*.ttf")],
        title="Select a TrueType Font (.ttf) File"
    )
    
    file_label.config(text='Selected Font: ' + file_path)

# Create the main window
root = tk.Tk()
root.title()

ttk.Label(root, text='Font Size: ').pack()
font_size_entry = ttk.Entry(root)
font_size_entry.pack()

ttk.Label(root, text='Background Color: ').pack()
background_color_entry = ttk.Entry(root)
background_color_entry.pack()

ttk.Label(root, text='Text Color:').pack()
text_color_entry = ttk.Entry(root)
text_color_entry.pack()



# Create three dropdown options
option1_var = tk.StringVar()
option1_label = tk.Label(root, text='Team: ')
option1_label.pack()
option1_menu = tk.OptionMenu(root, option1_var, *list(teamsID.keys()))
option1_menu.pack()

option2_var = tk.StringVar()
option2_label = tk.Label(root, text='Season Type: ')
option2_label.pack()
option2_menu = tk.OptionMenu(root, option2_var, *seasonTypes)
option2_menu.pack()

option3_var = tk.StringVar()
option3_label = tk.Label(root, text='Last N Games: ')
option3_label.pack()
option3_menu = tk.OptionMenu(root, option3_var, *nGames)
option3_menu.pack()

option4_var = tk.StringVar()
option4_label = tk.Label(root, text='Stats Type: ')
option4_label.pack()
option4_menu = tk.OptionMenu(root, option4_var, *dTypes)
option4_menu.pack()




select_button = tk.Button(root, text="Select Font File", command=select_font_file)
select_button.pack()
file_label = tk.Label(root, text='Selected File: ')
file_label.pack()

# Create a 'Select Path' button
select_path_button = tk.Button(root, text='Select Path', command=select_path)
select_path_button.pack()
# Create a label to display the selected path
path_label = tk.Label(root, text='Selected Path: ')
path_label.pack()

# Create a 'Generate' button
generate_button = tk.Button(root, text='Generate', command=generate_report)
generate_button.pack()

# Initialize the selected path variable
selected_path = ''
file_path = ''

# Start the main loop
root.mainloop()

