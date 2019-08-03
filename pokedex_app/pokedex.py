#!/usr/bin/env python3
"""
A simple pokedex implemented in python using the tkinter library

Author: Tal Druzhinin
"""

# Imports

from tkinter import *
from requests import get as request
from PIL import Image as PILImage, ImageTk
from io import BytesIO

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
API_URL = "https://pokeapi.co/api/v2/pokemon/"


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
    background_image = PhotoImage(file='Background.gif')
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
    image_pokemon_img.place(anchor='n', relx=0.25, rely=0.25, relwidth=0.5, relheight=0.6)

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

    # Error frame
    frame_error = Frame(frame_display, bg=TEAL)
    frame_error.place(anchor='n', relx=0.5, rely=0.8, relwidth=0.9, relheight=0.75)

    label_error = Label(frame_error, bg=TEAL, fg='red', font=('Courier', 13, 'bold'), text="")
    label_error.place(anchor='n', relx=0.5, rely=0.05, relwidth=1, relheight=0.2)

    # Search button frame
    frame_search = Frame(root, bg=TEAL)
    frame_search.place(anchor='n', relx=0.175, rely=0.11, relwidth=0.16, relheight=0.06)

    # Search button
    button_search = Button(frame_search, font=('Courier', 9, 'bold'), text="SEARCH", bg=TEAL, borderwidth=0,
                           activebackground=TEAL, activeforeground=GREY,
                           command=lambda: pokemon_api_request(entry_pokemon_name, label_name, label_id,
                                                               image_pokemon_img,
                                                               label_type_content, label_height_content,
                                                               label_weight_content, label_error))
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


def pokemon_api_request(pokemon_entry, name_view, id_view, image_view, type_view, height_view, weight_view, error_view):
    """
    Get the pokemon info from the API and pass the information to the GUI
    """
    # Clear all previous text
    clear_labels([name_view, id_view, image_view, type_view, height_view, weight_view, error_view])

    # Extract the pokemon's name (or ID) from the entry
    pokemon_text = pokemon_entry.get().lower()

    # Throw an error if no name or ID were passed
    if not pokemon_text or pokemon_text == NAME_MESSAGE.lower():
        error_view['text'] = "Please enter a name or an ID"
        return

    # Fetch the information from the API
    response = request(API_URL + pokemon_text)

    # Try parsing the JSON
    try:
        entry = response.json()
        id_number = entry['id']
        name = entry['name'].capitalize()
        image = image_from_url(entry['sprites']['front_default'])
        height = (entry['height'] * 10)
        weight = (entry['weight'] // 10)
        types = [x['type']['name'] for x in entry['types']]

    except (KeyError, ValueError):
        # If the parsing failed it means the object returned wasn't a JSON or did not contain the right fields
        # This can happen only in case the API did not find the pokemon and returned a 404 or a "pokemon not found" page
        error_view['text'] = "Pokemon not found"
        return

    # If everything is alright, clear error
    error_view['text'] = None

    # Set name
    name_view['text'] = name

    # Set ID
    id_view['text'] = '#' + str(id_number)

    # Set image
    image_view['image'] = image
    image_view.photo = image

    # Set types
    type_view['text'] = types[0].capitalize() + ('|' + types[1].capitalize() if len(types) > 1 else "")
    # TODO color different types

    # Set height
    height_view['text'] = height, "CM"

    # Set weight
    weight_view['text'] = weight, "KG"


def image_from_url(image_url):
    """
    Get the image from the URL passed by the API
    """
    # Fetch image data from URL
    response = request(image_url)
    image_data = BytesIO(response.content)

    # Convert image into a PhotoImage using PIL
    image = ImageTk.PhotoImage(PILImage.open(image_data))

    return image


def clear_labels(label_list):
    """
    Remove all text and images from all labels
    """
    for label in label_list:
        label['text'] = ""
        label.photo = None


if __name__ == '__main__':
    main()
