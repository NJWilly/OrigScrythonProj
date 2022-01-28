# mtg_tools.py
#
# Contains procedures for manipulating MTG items
#

import scrython
from scrython import ScryfallError


def get_card_price(mtg_card):
    # get the price of a given card
    try:
        card = scrython.cards.Named(fuzzy=mtg_card)
    except ScryfallError:
        card_price = "Card Not Found"
    else:
        card_price = str(card.prices("usd"))

    if card_price == "None":
        return "Price not found"
    else:
        return card_price

