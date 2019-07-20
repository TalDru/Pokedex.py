#!/usr/bin/env python3
"""
A simple pokedex implemented in python using the tkinter library

Author: Tal Druzhinin
"""

# Imports
from io import BytesIO
from tkinter import *
import requests
from PIL import Image as PILImage, ImageTk

# Constants

# The Background image's height and width
HEIGHT = 575
WIDTH = 324

# Constant colors
TEAL = "#0FF"
GREY = "#666"
BLACK = "#000"

# Constant strings
NAME_MESSAGE = "Search the name or ID of any pokémon"

# The API service for the pokedex
API = "https://pokeapi.co/api/v2/pokemon/"


def main():
    # Root TK object
    root = Tk()
    root.title("Pokédex")

    # Disable resizing to keep the correct resolution
    root.resizable(False, False)

    # Canvas with the dimensions of the BG image
    canvas = Canvas(root, height=HEIGHT, width=WIDTH)
    canvas.pack()

    # Background image
    background_image = PhotoImage(file='Background.ppm')
    background_label = Label(root, image=background_image)
    background_label.place(relwidth=1, relheight=1)

    # Search bar frame
    frame_name = Frame(root, bg=TEAL)
    frame_name.place(anchor='n', relx=0.497, rely=0.853, relwidth=0.81, relheight=0.09)

    # Search bar entry
    entry_pokemon_name = Entry(frame_name, bg=TEAL, borderwidth=0, selectbackgroun=TEAL, font=('Courier', 9, 'bold'))
    entry_pokemon_name.place(relwidth=1, relheight=1)
    entry_name_init(entry_pokemon_name)
    entry_pokemon_name.bind('<FocusOut>', entry_name_filler)
    entry_pokemon_name.bind('<FocusIn>', entry_name_cleaner)

    frame_display = Frame(root, bg=TEAL)
    frame_display.place(anchor='n', relx=0.5, rely=0.4, relwidth=0.8, relheight=0.355)

    # Image frame
    image_pokemon_img = Label(frame_display, bg=TEAL)
    image_pokemon_img.place(anchor='n', relx=0.2, rely=0.35, relwidth=0.3, relheight=0.4)

    # Info table frame, containing frames for each of the parameters' label and content
    frame_info = Frame(frame_display, bg=TEAL)
    frame_info.place(anchor='n', relx=0.7, rely=0.2, relwidth=0.55, relheight=0.75)

    label_type_title = Label(frame_info, bg=TEAL, font=('Courier', 13, 'bold'), text="TYPE:")
    label_type_title.place(anchor='n', relx=0.5, rely=0.05, relwidth=0.5, relheight=0.1)

    label_type_content = Label(frame_info, bg=TEAL, font=('Courier', 10, 'bold'))
    label_type_content.place(anchor='n', relx=0.5, rely=0.15, relwidth=0.9, relheight=0.1)

    label_height_title = Label(frame_info, bg=TEAL, font=('Courier', 13, 'bold'), text="HEIGHT:")
    label_height_title.place(anchor='n', relx=0.5, rely=0.3, relwidth=0.5, relheight=0.1)

    label_height_content = Label(frame_info, bg=TEAL, font=('Courier', 13, 'bold'))
    label_height_content.place(anchor='n', relx=0.5, rely=0.4, relwidth=0.9, relheight=0.1)

    label_weight_title = Label(frame_info, bg=TEAL, font=('Courier', 13, 'bold'), text="WEIGHT:")
    label_weight_title.place(anchor='n', relx=0.5, rely=0.55, relwidth=0.5, relheight=0.1)

    label_weight_content = Label(frame_info, bg=TEAL, font=('Courier', 13, 'bold'))
    label_weight_content.place(anchor='n', relx=0.5, rely=0.65, relwidth=0.9, relheight=0.1)

    # Pokemon's name and ID frame
    label_name = Label(frame_display, bg=TEAL, font=('Courier', 13, 'bold'))
    label_name.place(anchor='n', relx=0.5, rely=0, relwidth=0.5, relheight=0.1)

    label_id = Label(frame_display, bg=TEAL, font=('Courier', 9, 'bold'))
    label_id.place(anchor='n', relx=0.5, rely=0.1, relwidth=0.2, relheight=0.1)

    # Search button frame
    frame_search = Frame(root, bg=TEAL)
    frame_search.place(anchor='n', relx=0.175, rely=0.11, relwidth=0.16, relheight=0.06)

    # Search button
    button_search = Button(frame_search, font=('Courier', 9, 'bold'), text="SEARCH", bg=TEAL, borderwidth=0,
                           activebackground=TEAL, activeforeground=GREY,
                           command=lambda: get_pokemon(entry_pokemon_name, label_name, label_id, image_pokemon_img,
                                                       label_type_content, label_height_content, label_weight_content))
    button_search.place(relwidth=1, relheight=1)

    entry_pokemon_name.bind('<Return>', lambda enter_pressed: button_search.invoke())

    # Finalize the GUI
    root.mainloop()


def entry_name_init(entry):
    """
    Initialize the search bar to display the instruction message
    """
    entry.insert(0, NAME_MESSAGE)
    entry.config(fg=GREY)


def entry_name_filler(event):
    """
    Reinsert the instruction message in case the search bar was cleared
    """
    # Get the search bar
    entry = event.widget

    # If the search bar is clear, insert message and color it grey
    if not entry.get():
        entry.insert(0, NAME_MESSAGE)
        entry.config(fg=GREY)


def entry_name_cleaner(event):
    """
    Clear the instruction message in case the user clicked on the search bar
    """
    # Get the search bar
    entry = event.widget

    # If the search bar displays the instruction message, clear it and color it black
    if entry.get() == NAME_MESSAGE:
        entry.delete(0, END)
        entry.config(fg=BLACK)


def get_pokemon(entry, name_view, id_view, image_view, type_view, height_view, weight_view):
    """
    Get the pokemon info from the API and pass the information to the GUI
    """
    # TODO make the code more OOP
    # TODO print if a pokemon was not found or no pokemon name was passed

    # Get the pokemon's name (or ID)
    pokemon = entry.get().lower()

    # If search bar was clear and no pokemon was
    if not pokemon:
        print("No Pokemon Passed")
        # TODO display that to the user
        return

    # Send a request to the API with the given pokemon
    response = requests.get(API + pokemon)

    # Try to parse the JSON
    try:
        pokedex_entry = response.json()
        parsed = {'id': pokedex_entry['id'], 'name': pokedex_entry['name'].capitalize(),
                  'image': pokedex_entry['sprites']['front_default'], 'height': (pokedex_entry['height'] * 10),
                  'weight': (pokedex_entry['weight'] // 10),
                  'type': [x['type']['name'] for x in pokedex_entry['types']]}
        # TODO OOP - class for a pokemon entry

        set_data(parsed, name_view, id_view, image_view, type_view, height_view, weight_view)

    except ValueError:
        # If the parsing failed it means the object returned wasn't a JSON
        # This can happen only in case the API did not find the pokemon
        print("Not Found")
        # TODO display that to the user
        return


def set_data(parsed_entry, name_view, id_view, image_view, type_view, height_view, weight_view):
    """
    Set the data parsed from the API to the respective views
    """
    # TODO again, OOP both for the api and the views

    # Set name
    name_view['text'] = parsed_entry['name']

    # Set ID
    id_view['text'] = '#' + str(parsed_entry['id'])

    # Set image
    image = image_from_url(parsed_entry['image'])
    image_view['image'] = image
    image_view.photo = image

    # Set types
    type_view['text'] = parsed_entry['type'][0].capitalize() + (
        '|' + parsed_entry['type'][1].capitalize() if len(parsed_entry['type']) > 1 else "")
    # TODO OPTIONAL: color different types

    # Set height
    height_view['text'] = parsed_entry['height'], "CM"

    # Set weight
    weight_view['text'] = parsed_entry['weight'], "KG"


def image_from_url(image_url):
    """
    Get the image from the URL passed by the API
    """
    # Fetch image data from URL
    response = requests.get(image_url)
    image_data = BytesIO(response.content)

    # Convert image into a PhotoImage using PIL
    image = ImageTk.PhotoImage(PILImage.open(image_data))

    return image


if __name__ == '__main__':
    main()
