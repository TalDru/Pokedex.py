#!/usr/bin/env python3

import base64
from tkinter import *
import requests
from urllib.request import urlopen

HEIGHT = 575
WIDTH = 324
TEAL = "#01FFFF"
NAME_MESSAGE = "Search the name or ID of any pokémon"
API = "https://pokeapi.co/api/v2/pokemon/"


def main():
    root = Tk()
    root.resizable(False, False)
    root.title("Pokédex")

    canvas = Canvas(root, height=HEIGHT, width=WIDTH)
    canvas.pack()

    background_image = PhotoImage(file='Background.ppm')
    background_label = Label(root, image=background_image)
    background_label.place(relwidth=1, relheight=1)

    frame_name = Frame(root, bg=TEAL)
    frame_name.place(anchor='n', relx=0.497, rely=0.853, relwidth=0.81, relheight=0.09)

    entry_pokemon_name = Entry(frame_name, bg=TEAL, borderwidth=0, selectbackgroun=TEAL, font=('Courier', 9, 'bold'))
    entry_pokemon_name.place(relwidth=1, relheight=1)
    entry_name_init(entry_pokemon_name)
    entry_pokemon_name.bind('<FocusOut>', entry_name_filler)
    entry_pokemon_name.bind('<FocusIn>', entry_name_cleaner)

    frame_display = Frame(root, bg=TEAL)
    frame_display.place(anchor='n', relx=0.5, rely=0.4, relwidth=0.8, relheight=0.355)

    image_pokemon_img = Label(frame_display, bg='green')
    image_pokemon_img.place(anchor='n', relx=0.2, rely=0.35, relwidth=0.3, relheight=0.4)

    # TODO region info table

    frame_info = Frame(frame_display)
    frame_info.place(anchor='n', relx=0.7, rely=0.2, relwidth=0.55, relheight=0.75)

    label_type_title = Label(frame_info, bg='lime', font=('Courier', 13, 'bold'), text="TYPE:")
    label_type_title.place(anchor='n', relx=0.5, rely=0.05, relwidth=0.5, relheight=0.1)

    label_type_content = Label(frame_info, bg='lime', font=('Courier', 10, 'bold'), text="TYPE1 | TYPE2")
    label_type_content.place(anchor='n', relx=0.5, rely=0.15, relwidth=0.9, relheight=0.1)

    label_height_title = Label(frame_info, bg='lime', font=('Courier', 13, 'bold'), text="HEIGHT:")
    label_height_title.place(anchor='n', relx=0.5, rely=0.3, relwidth=0.5, relheight=0.1)

    label_height_content = Label(frame_info, bg='lime', font=('Courier', 13, 'bold'), text="000 CM")
    label_height_content.place(anchor='n', relx=0.5, rely=0.4, relwidth=0.9, relheight=0.1)

    label_weight_title = Label(frame_info, bg='lime', font=('Courier', 13, 'bold'), text="WEIGHT:")
    label_weight_title.place(anchor='n', relx=0.5, rely=0.55, relwidth=0.5, relheight=0.1)

    label_weight_content = Label(frame_info, bg='lime', font=('Courier', 13, 'bold'), text="000 KG")
    label_weight_content.place(anchor='n', relx=0.5, rely=0.65, relwidth=0.9, relheight=0.1)

    # TODO endregion

    label_name = Label(frame_display, bg=TEAL, font=('Courier', 13, 'bold'))
    label_name.place(anchor='n', relx=0.5, rely=0, relwidth=0.5, relheight=0.1)

    label_id = Label(frame_display, bg=TEAL, font=('Courier', 9, 'bold'))
    label_id.place(anchor='n', relx=0.5, rely=0.1, relwidth=0.2, relheight=0.1)

    frame_search = Frame(root, bg=TEAL)
    frame_search.place(anchor='n', relx=0.175, rely=0.11, relwidth=0.16, relheight=0.06)

    button_search = Button(frame_search, font=('Courier', 9, 'bold'), text="SEARCH", bg=TEAL, borderwidth=0,
                           activebackground=TEAL, activeforeground="Grey50",
                           command=lambda: get_pokemon(entry_pokemon_name, label_name, label_id, image_pokemon_img,
                                                       label_type_content, label_height_content, label_weight_content))
    button_search.place(relwidth=1, relheight=1)

    entry_pokemon_name.bind('<Return>', lambda enter_pressed: button_search.invoke())

    root.mainloop()


def entry_name_init(entry):
    entry.insert(0, NAME_MESSAGE)
    entry.config(fg='Grey40')


def entry_name_filler(event):
    entry = event.widget
    if not entry.get():
        entry.insert(0, NAME_MESSAGE)
        entry.config(fg='Grey40')


def entry_name_cleaner(event):
    entry = event.widget
    if entry.get() == NAME_MESSAGE:
        entry.delete(0, END)
        entry.config(fg='black', )


def get_pokemon(entry, name_view, id_view, image_view, type_view, height_view, weight_view):
    pokemon = entry.get().lower()

    if not pokemon:
        print("No Pokemon Passed")
        return

    response = requests.get(API + pokemon)
    try:
        pokedex_entry = response.json()
        parsed = {'id': pokedex_entry['id'], 'name': pokedex_entry['name'].capitalize(),
                  'image': pokedex_entry['sprites']['front_default'], 'height': (pokedex_entry['height'] * 10),
                  'weight': (pokedex_entry['weight'] // 10),
                  'type': [x['type']['name'] for x in pokedex_entry['types']]}

        set_data(parsed, name_view, id_view, image_view, type_view, height_view, weight_view)

    except ValueError:
        print("Not Found")
        return


def set_data(parsed_entry, name_view, id_view, image_view, type_view, height_view, weight_view):
    name_view['text'] = parsed_entry['name']
    id_view['text'] = '#' + str(parsed_entry['id'])
    # TODO images
    type_view['text'] = parsed_entry['type'][0].capitalize() + (
        '|' + parsed_entry['type'][1].capitalize() if len(parsed_entry['type']) > 1 else "")
    height_view['text'] = parsed_entry['height'], "CM"
    weight_view['text'] = parsed_entry['weight'], "KG"


def image_by_url(image_url):
    image_byt = urlopen(image_url).read()
    image_b64 = base64.encodebytes(image_byt)
    photo = PhotoImage(data=image_b64)
    return photo


if __name__ == '__main__':
    main()

# TODO pass types
# TODO make images appear
# TODO make printing aligned
# TODO print if a pokemon was not found or no pokemon name was passed
# TODO set all texts to the currier font and correct background colors
# TODO comment
# TODO OPTIONAL: color different types
# TODO OPTIONAL: move image to the left and info to the right
