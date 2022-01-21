from tkinter import *
from tkinter import Tk

from main import list_all_sets

root = Tk()
root.title("MTG test program")
root.geometry("400x400")


def get_price(mtg_card, my_window):
    # get the price of a given card
    import scrython

    card = scrython.cards.Named(fuzzy=mtg_card)
    print(card)
    card_price = str(card.prices("usd"))
    print(card_price)
    if card_price == "None":
        output_label_text = "Card price not found"
    else:
        output_label_text = "The price of " + mtg_card + " is " + str(card_price)
    output_label = Label(my_window, text=output_label_text)
    output_label.grid(row=3, column=0, columnspan=2, sticky="W")


def list_all_mtg_sets_window():
    window = Tk()
    window.title("list all MTG sets")
    window.geometry("400x400")
    mtg_set = list_all_sets()
    options = []
    for cur_set in mtg_set.data():
        options.append(cur_set["name"])

    # Dropdown box

    clicked = StringVar()
    clicked.set(options[0])
    print(options[0])
    drop = OptionMenu(window, clicked, *options)
    drop.grid(row=0, column=1, sticky="E")
    drop_label = Label(window, text="Select a MTG set")
    drop_label.grid(row=0, column=0)


def card_price_window():
    price_window = Toplevel()
    price_window.geometry("400x400")
    price_window.title("Get a MTG card price")

    input_label = Label(price_window, text="Enter the name of a MTG card")
    input_label.grid(row=0, column=0)
    e = Entry(price_window, width=50)
    e.grid(row=1, column=0, sticky="W")

    fetch_price_button = Button(price_window, text="Get price", command=lambda: get_price(e.get(), price_window))
    fetch_price_button.grid(row=2, column=0, columnspan=2)


card_price_button = Button(root, text="Get the price of a MTG card", command=card_price_window)
card_price_button.grid(row=0, column=0, sticky="W")

all_sets_button = Button(root, text="Get all MTG sets", command=list_all_mtg_sets_window)
all_sets_button.grid(row=1, column=0, pady=10, sticky="W")


root.mainloop()
