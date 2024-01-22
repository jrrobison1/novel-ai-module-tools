#!/usr/bin/env python3
# Assists in text curation by identifying sections which
# fall below a configurable regex match threshold
import json
import os
import re
from sys import argv
from colorama import Fore
from colorama import Style
from config import *
import textwrap
import numpy as np

from matplotlib import pyplot
import matplotlib
import PySimpleGUI as sg
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
matplotlib.use('TkAgg')


# Get score
def get_score(text, pattern):
    print("Computing score for text")
    match_count = len(pattern.findall(text))
    word_count = len(text.split())
    print(f"Number of matches: [{match_count}]. Word count: [{word_count}]")

    # If the text is too short
    if (word_count < MATCH_WORD_COUND_THRESHOLD):
        return 0
    
    # Match count per 1000 words
    return (match_count * 1000) / word_count

def get_file():
    filename = argv[1]
    with open(filename) as f:
        file_text = f.read()
    f.close()

    return filename, file_text

def match_count():
    filename, file_text = get_file()
    primary_pattern = re.compile(PRIMARY_PATTERN, re.IGNORECASE)
    secondary_pattern = re.compile(SECONDARY_PATTERN, re.IGNORECASE)

    all_paragraphs_primaries_scores = []
    all_paragraphs_secondaries_scores = []
    section_primary_scores = []
    section_secondary_scores = []

    paragraphs = file_text.splitlines()
    for paragraph in paragraphs:
        paragraph_primary_score = get_score(paragraph, primary_pattern)
        paragraph_secondary_score = get_score(paragraph, secondary_pattern)

        all_paragraphs_primaries_scores.append(paragraph_primary_score)
        all_paragraphs_secondaries_scores.append(paragraph_secondary_score)

    sections = file_text.split("***")
    for section in sections:
        section = section.strip()
        section_primary_score = get_score(section, primary_pattern)
        section_secondary_score = get_score(section, secondary_pattern)


        if (section_primary_score < PRIMARY_SCORE_FIRST_THRESHOLD and section_secondary_score < SECONDARY_SCORE_FIRST_THRESHOLD) or (section_primary_score < PRIMARY_SCORE_SECOND_THRESHOLD and  section_secondary_score < SECONDARY_SCORE_SECOND_THRESHOLD):
            P_COLOR = Fore.RED if section_primary_score < PRIMARY_SCORE_FIRST_THRESHOLD / 2 else Fore.BLUE
            S_COLOR = Fore.RED if section_secondary_score < SECONDARY_SCORE_FIRST_THRESHOLD / 2 else Fore.LIGHTMAGENTA_EX
            print("============================")
            print(f"{P_COLOR}P[{section_primary_score:.2f}], {S_COLOR}S[{section_secondary_score:.2f}]{Style.RESET_ALL}")
            print(f"Section beginning with: [{Fore.YELLOW}{section[:30]}{Style.RESET_ALL}]")

        section_primary_scores.append(section_primary_score)
        section_secondary_scores.append(section_secondary_score)

    # Total book scores
    book_primary_score = get_score(file_text, primary_pattern)
    book_secondary_score = get_score(file_text, secondary_pattern)
    print(f"Book Primaries score: [{book_primary_score}]")
    print(f"Book Secondaries score: [{book_secondary_score}]")

    # Section graph
    section_range = list(range(0, len(sections)))
    __, sectAx = pyplot.subplots()
    sectAx.plot(section_range, section_primary_scores, label = "primaries")
    sectAx.plot(section_range, section_secondary_scores, label = "secondaries")
    sectAx.set_xlabel('Section Number')
    sectAx.set_ylabel('Pattern matches per 1000 words')
    sectAx.set_title(f"Sections: {os.path.basename(filename)}\nPrimaries: [{book_primary_score:.2f}], Secondaries: [{book_secondary_score:.2f}]")
    sectAx.legend(loc = 'best')

    # Paragraph primary matches graph
    paragraph_range = list(range(0, len(paragraphs)))
    __, para_prim_ax = pyplot.subplots()
    para_prim_ax.plot(paragraph_range, all_paragraphs_primaries_scores, label="primaries")
    para_prim_ax.set_xlabel("Paragraph number")
    para_prim_ax.set_ylabel("Pattern matches per 1000 words")
    para_prim_ax.set_title(f"Paragraphs (Primaries): {os.path.basename(filename)}\nPrimaries: [{book_primary_score:.2f}], Secondaries: [{book_secondary_score:.2f}]")
    para_prim_ax.legend(loc = 'best')

    # Paragraph secondary matches graph
    __, para_sec_ax = pyplot.subplots()
    para_sec_ax.plot(paragraph_range, all_paragraphs_secondaries_scores, color='orange', label="secondaries")
    para_sec_ax.set_xlabel("Paragraph number")
    para_sec_ax.set_ylabel("Pattern matches per 1000 words")
    para_sec_ax.set_title(f"Paragraphs (Secondaries): {os.path.basename(filename)}\nPrimaries: [{book_primary_score:.2f}], Secondaries: [{book_secondary_score:.2f}]")
    para_sec_ax.legend(loc = 'best')

    pyplot.show()

def draw_figure(canvas, figure):
    figure_canvas_agg = FigureCanvasTkAgg(figure, canvas)
    figure_canvas_agg.draw()
    figure_canvas_agg.get_tk_widget().pack(side='top', fill='both', expand=1)
    return figure_canvas_agg


def delete_figure_agg(figure_agg):
    figure_agg.get_tk_widget().forget()
    pyplot.close('all')


primary_pattern = re.compile(PRIMARY_PATTERN, re.IGNORECASE) 
secondary_pattern = re.compile(SECONDARY_PATTERN, re.IGNORECASE)

file_name, file_text = get_file()
full_section_text = file_text
section_text = full_section_text.split("***")
section_index = 0
first_section = section_text[section_index]

def get_paragraph_scores_figure(section_text):
    paragraphs = section_text.splitlines()
    paragraph_scores = []
    secondary_scores = []
    for paragraph in paragraphs:
        paragraph_scores.append(get_score(paragraph, primary_pattern))
        secondary_scores.append(get_score(paragraph, secondary_pattern))

    # Paragraph primary matches graph
    paragraph_range = list(range(0, len(paragraphs)))
    para_fig, para_prim_ax = pyplot.subplots()
    para_prim_ax.plot(paragraph_range, paragraph_scores, label="primaries")
    para_prim_ax.plot(paragraph_range, secondary_scores, label="secondaries")
    para_prim_ax.set_xlabel("Paragraph number")
    para_prim_ax.set_ylabel("Pattern matches per 1000 words")
    para_prim_ax.legend(loc = 'best')

    return para_fig

book_primary_score = get_score(file_text, primary_pattern)
book_secondary_score = get_score(file_text, secondary_pattern)
book_original_primary_score = book_primary_score
book_original_secondary_score = book_secondary_score

print(f"Book Primaries score: [{book_primary_score}]")
print(f"Book Secondaries score: [{book_secondary_score}]")

primary_score = get_score(first_section, primary_pattern)
secondary_score = get_score(first_section, secondary_pattern)

# Define the window's contents
layout = [[sg.Text("Section", font=("courier", 20)), sg.Text("Book", font=("courier", 20), justification="right", pad=(400, 0))],
          [sg.Text(f"Primary: {primary_score:2f}", font=("courier", 20), key="primary_score"), sg.Text(f"{book_primary_score:.2f} ({(book_primary_score - book_original_primary_score):.2f})", font=("courier",20), key="book_primary_score", justification="right", pad=(400, 0)) ],
          [sg.Text(f"Secondary: {secondary_score:2f}", font=("courier", 20), key="secondary_score"), sg.Text(f"{book_secondary_score:.2f} ({(book_secondary_score - book_original_secondary_score):.2f})", font=("courier",20), key="book_secondary_score", justification="right", pad=(400, 0))],
        #   [sg.Text(f"Total book primary score: {book_primary_score:.2f}", font=("courier",16), key="book_primary_score")],
        #   [sg.Text(f"Total book secondary score: {book_secondary_score:.2f}", font=("courier",16), key="book_secondary_score")],
          [sg.Multiline(first_section, size=(120,20), font=("courier", 20), auto_size_text=False, key='textbox')],
          [sg.Button('Keep', size=(15, 15), key="keep"), sg.Button('Trash', size=(15,15), key="trash"), sg.Canvas(key="canvas")]]

# Create the window
window = sg.Window('Match Count', layout, finalize=True, size=(1280, 800))
para_fig = get_paragraph_scores_figure(first_section)
fig_canvas_agg = draw_figure(window["canvas"].TKCanvas, para_fig)

# Display and interact with the Window using an Event Loop
while True:
    event, values = window.read()
    delete_figure_agg(fig_canvas_agg)

    # See if user wants to quit or window was closed
    if event == sg.WINDOW_CLOSED or event == 'Quit':
        break

    if section_index == len(section_text) - 1:
        # Write file out
        with open("write_out.txt", "w") as f:
            f.write(temp_full_text)
        f.close()

        break

    if (event == "keep"):
        section_text[section_index] = window["textbox"].get()

    if event == "trash":
        section_text[section_index] = "***"

    temp_full_text = ""
    for section in section_text:
        if len(section.split()) > 1:
            temp_full_text = temp_full_text + section.strip().replace("*", "").replace("\t", "").replace("\n\n", "\n") + "\n***\n"

    book_primary_score = get_score(temp_full_text, primary_pattern)
    book_secondary_score = get_score(temp_full_text, secondary_pattern)

    section_index = section_index + 1


    next_section = section_text[section_index]
    section_with_tabs = ""
    paragraphs = next_section.splitlines()
    for paragraph in paragraphs:
        paragraph = "\t" + paragraph + "\n\n"
        section_with_tabs += paragraph
    
    window["primary_score"].update(f"{get_score(next_section, primary_pattern):.2f}")
    window["secondary_score"].update(f"{get_score(next_section, secondary_pattern):.2f}")
    # Output a message to the window
    window["book_primary_score"].update(f"{book_primary_score:.2f} ({(book_primary_score - book_original_primary_score):.2f})")
    window["book_secondary_score"].update(f"{book_secondary_score:.2f} ({(book_secondary_score - book_original_secondary_score):.2f})")
    window['textbox'].update(section_with_tabs)
    para_fig = get_paragraph_scores_figure(next_section)
    fig_canvas_agg = draw_figure(window["canvas"].TKCanvas, para_fig)   

    # Finish up by removing from the screen
    window.close()