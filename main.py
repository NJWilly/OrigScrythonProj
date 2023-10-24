# This is a sample Python script to test scrython
import requests
import scrython
# from scrython import ScryfallError
import re
import getdeckimage
from mtg_tools import get_card_price
# import Pillow
from PIL import Image
from PIL import ImageFilter
from PIL import ImageDraw


def get_price():
    # ask for the name of an MTG card and print the price

    mtg_card = input("Enter the name of a MTG card:  ")
    print(get_card_price(mtg_card))


def list_all_sets(print_it=False):
    # list all Mtg sets
    import scrython
    mtg_set = scrython.sets.Sets()
    if print_it:
        print("\nList of all MTG Sets")
        for cur_set in reversed(mtg_set.data()):
            print(cur_set["name"] + " (" + cur_set["code"].upper() + ")")
        print("\nThere are " + str(mtg_set.data_length()) + " sets.")
    return mtg_set


def list_all_cards():
    # print a list of cardS and mana cost in a given MTG set
    import scrython
    set_to_lookup = input("What set: ")
    mtg_cards = scrython.cards.Search(q="e:" + set_to_lookup + " -t:basic")
    for selected_card in mtg_cards.data():
        if "mana_cost" in selected_card:
            if len(selected_card["mana_cost"]) != 0:
                print(selected_card["name"] + " (" + selected_card["mana_cost"] + ")")
            else:
                print(selected_card["name"])
        else:
            print(selected_card["name"])


def mtg_body_text_info():
    # print a list of cardS and mana cost in a given MTG set
    import scrython
    from statistics import mean
    set_to_lookup = input("What set: ")
    mtg_cards = scrython.cards.Search(q="e:" + set_to_lookup + " -t:basic")
    oracle_text_len = []
    len_120_or_less = 0
    for selected_card in mtg_cards.data():
        if "oracle_text" in selected_card:
            oracle_text_len.append(len(selected_card["oracle_text"]))
            print(selected_card["oracle_text"])
            if len(selected_card["oracle_text"]) <= 120:
                len_120_or_less += 1
        else:
            oracle_text_len.append(0)
    print(f"\nMaximum characters: {max(oracle_text_len)}."
          f"\nAverage characters: {mean(oracle_text_len):.2f}."
          f"\nNumber of cards with 120 or less characters: {len_120_or_less}.")


def list_multifaced_cards():
    # print a list of cardS and mana cost in a given MTG set
    import scrython
    set_to_lookup = input("From what set would you like to see a list of multi-faced cards: ")
    mtg_cards = scrython.cards.Search(q="e:" + set_to_lookup + " -t:basic")
    card_count = 0
    for selected_card in mtg_cards.data():
        if "card_faces" in selected_card:
            # print(selected_card)
            card_count += 1
            print(selected_card["name"] + " (" + selected_card["card_faces"][0]["mana_cost"] + ")")
    print("There were " + str(card_count) + " multi-faced cards found in the set " + set_to_lookup.upper() + ".")


def mtg_set_instant_quiz():
    # present a quiz from a selected MTG set.
    # Instants only, give random card name and three wrong mana costs from the set and one correct mana cost
    # Ask the user to identify the correct mana cost.  Let the user know if they were correct
    import scrython
    from random import randrange
    print("\n\nInstant Quiz - Given a MTG set, you will be presented with a quiz about Instant cards' mana costs.")
    set_to_lookup = input("\nFrom what set would you like to be quizzed: ")
    mtg_cards = scrython.cards.Search(q="e:" + set_to_lookup + " t:instant")
    card_count = 0
    instant_questions = []
    for selected_card in mtg_cards.data():
        if "card_faces" in selected_card:
            # load from first card face
            q = [selected_card["card_faces"][0]["name"], selected_card["card_faces"][0]["mana_cost"]]
        else:
            # load from card
            q = [selected_card["name"], selected_card["mana_cost"]]
        instant_questions.append(q)
        card_count += 1

    selected_question = randrange(0, card_count-1)
    distractors = []
    distractors_ct = 0
    while distractors_ct <= 3:
        selected_distractor = randrange(0, card_count-1)
        if instant_questions[selected_distractor][1] != instant_questions[selected_question][1]:
            distractors.append(instant_questions[selected_distractor][1])
            distractors_ct += 1
    correct_answer = randrange(0, 3)
    distractors[correct_answer] = instant_questions[selected_question][1]
    print("What is the casting cost of \"" + instant_questions[selected_question][0] + "\"?\n")
    for idx, i in enumerate(distractors):
        print("\t" + chr(97 + idx) + ") " + i)
    guess = input("\nYour answer: ")
    if guess.lower() == chr(97 + correct_answer):
        print("Correct!")
    else:
        print("Incorrect!  The correct answer was \"" + chr(97 + correct_answer) + "\"")


def mtg_set_instant_quiz_list(mtg_set):
    # Return a list of instant quiz questions from given MTG set
    #
    import scrython
    from random import randrange
    from random import shuffle
    # loop through card populating question and mana cost lists
    questions = []
    mana_costs = []
    question = []
    mtg_cards = scrython.cards.Search(q="e:" + mtg_set + " t:instant")
    for selected_card in mtg_cards.data():
        if "card_faces" in selected_card:
            # load from first card face
            question.append("What is the mana cost of <b>" + selected_card["card_faces"][0]["name"] + "</b>.")
            mana_costs.append(selected_card["card_faces"][0]["mana_cost"])
        else:
            # load from card
            question.append("What is the mana cost of <b>" + selected_card["name"] + "</b>")
            mana_costs.append(selected_card["mana_cost"])

    # loop across questions
    for idx, (quest, mana) in enumerate(zip(question, mana_costs)):
        distractors_ct = 0  # number of distractors chosen
        distractors = []  # list of 4 distractors chosen

        # populate distractors
        while distractors_ct <= 3:
            # select a random distractor
            selected_distractor = randrange(0, len(mana_costs) - 1)
            # if the distractor is not the correct answer, select it
            if mana_costs[selected_distractor] != mana:
                distractors.append(mana_costs[selected_distractor])
                distractors_ct += 1

        # choose a location for the correct answer
        correct_answer_location = randrange(0, 4)
        # replace the random distractor with the correct one
        distractors[correct_answer_location] = mana

        # assemble the full kahoot string
        kahoot_line = [quest, distractors[0], distractors[1], distractors[2], distractors[3],
                       30, correct_answer_location + 1]
        # append to list of kahoot questions
        questions.append(kahoot_line)
        shuffle(questions)
    return questions


def make_kahoot_quiz():
    set_to_lookup = input("What set: ")
    questions = mtg_set_instant_quiz_list(set_to_lookup)

    # open Excel file
    import xlsxwriter  # see https://xlsxwriter.readthedocs.io/
    workbook = xlsxwriter.Workbook("venv/Kahoot-Quiz-" + set_to_lookup + ".xlsx")
    worksheet = workbook.add_worksheet()

    # place header row
    with open("venv/KahootHeaders.txt") as file:
        start_cell = "A"
        while line := file.readline().rstrip():
            worksheet.write(start_cell + "1", line)
            start_cell = chr(ord(start_cell) + 1)

    # loop for each row
    for row, question in enumerate(questions):
        # loop for each column
        start_cell = "A"
        for col, cell_item in enumerate(question):
            # write cell data
            my_row = str(row + 2)
            my_col = chr(ord(start_cell) + col)
            current_cell = my_col + my_row
            worksheet.write(current_cell, cell_item)
    workbook.close()


def write_to_kahoot_excel_file():
    import xlsxwriter  # see https://xlsxwriter.readthedocs.io/
    workbook = xlsxwriter.Workbook('venv/Kahoot-Quiz-Blank.xlsx')
    worksheet = workbook.add_worksheet()
    with open("venv/KahootHeaders.txt") as file:
        start_cell = "A"
        while line := file.readline().rstrip():
            worksheet.write(start_cell + "1", line)
            start_cell = chr(ord(start_cell) + 1)
    workbook.close()


def print_removal():
    # Return a list of mtg cards from a set tagged as removal
    #
    import scrython

    # loop through card populating question and mana cost lists
    mtg_set = "ISD"
    mtg_cards = scrython.cards.Search(q="s:" + mtg_set + " otag:removal")

    for selected_card in mtg_cards.data():
        if "card_faces" in selected_card:
            # load from first card face
            print(selected_card["card_faces"][0]["name"], end="")
            if len(selected_card["card_faces"][0]["mana_cost"]) > 0:
                print(" (" + selected_card["card_faces"][0]["mana_cost"] + ")")
            else:
                print("")
        else:
            # load from card
            print(selected_card["name"], end="")
            if len(selected_card["mana_cost"]) > 0:
                print(" (" + selected_card["mana_cost"] + ")")
            else:
                print("")
    print(f'\nThere were {mtg_cards.total_cards()} cards found tagged as removal in the MTG set: {mtg_set}.')


def get_removal_data_on_all_sets():
    import scrython
    import time

    # open Excel file
    import xlsxwriter  # see https://xlsxwriter.readthedocs.io/
    workbook = xlsxwriter.Workbook("RemovalData.xlsx")
    worksheet = workbook.add_worksheet()

    # write header data
    worksheet.write("A1", "Name")
    worksheet.write("B1", "Abv")
    worksheet.write("B3", "Removal")
    worksheet.write("B4", "Total")

    mtg_sets = scrython.sets.Sets()
    time.sleep(.001)
    cur_row = 2
    for mtg_set in mtg_sets.data():
        if mtg_set['set_type'] == 'core' or mtg_set['set_type'] == 'expansion':
            search_str = "e:" + mtg_set["code"] + " -t:basic"
            mtg_cards = scrython.cards.Search(q=search_str)
            time.sleep(.001)
            mtg_removal_cards = scrython.cards.Search(q="s:" + mtg_set["code"] + " otag:removal")
            time.sleep(.001)
            worksheet.write("A" + str(cur_row), mtg_set["name"])
            worksheet.write("B" + str(cur_row), mtg_set["code"].upper())
            worksheet.write("C" + str(cur_row), mtg_removal_cards.total_cards())
            worksheet.write("D" + str(cur_row), mtg_cards.total_cards())
            cur_row += 1
            print(f'In set {mtg_set["name"]} ({mtg_set["code"].upper()}) - '
                  f'{mtg_removal_cards.total_cards()}/{mtg_cards.total_cards()} cards are removal')
    workbook.close()


# when using an image as mask only the alpha channel is important
solid_fill = (50, 50, 50, 255)


def create_rounded_rectangle_mask(rectangle, radius):
    # create mask image. all pixels set to translucent
    i = Image.new("RGBA", rectangle.size, (0, 0, 0, 0))

    # create corner
    corner = Image.new('RGBA', (radius, radius), (0, 0, 0, 0))
    draw = ImageDraw.Draw(corner)
    # added the fill = . you only drew a line, no fill
    draw.pieslice((0, 0, radius * 2, radius * 2), 180, 270, fill=solid_fill)

    # max_x, max_y
    mx, my = rectangle.size

    # paste corner rotated as needed
    # use corners alpha channel as mask

    i.paste(corner, (0, 0), corner)
    i.paste(corner.rotate(90), (0, my - radius), corner.rotate(90))
    i.paste(corner.rotate(180), (mx - radius, my - radius), corner.rotate(180))
    i.paste(corner.rotate(270), (mx - radius, 0), corner.rotate(270))

    # draw both inner rects
    draw = ImageDraw.Draw(i)
    draw.rectangle([(radius, 0), (mx - radius, my)], fill=solid_fill)
    draw.rectangle([(0, radius), (mx, my - radius)], fill=solid_fill)

    return i


def blur_casting_cost(cc, card_image_fname, show=None):
    # see https://stackoverflow.com/questions/50433000/blur-a-region-shaped-like-a-rounded-rectangle-inside-an-image
    #
    #
    symbol_space = 39
    between_space = 1

    casting_cost = cc
    casting_cost_len = len(casting_cost)
    if casting_cost_len != 0:
        blur_size = symbol_space * casting_cost_len + between_space * (casting_cost_len - 1)
        start_blur = 625 - blur_size

        img = Image.open('temp_images/' + card_image_fname)
        # print(f'Image Shape: {img.size}')

        x, y = start_blur, 44  # start of blur position from the left and from the top
        radius = 25

        # third and fourth parameters is how far right and how far down to blur
        cropped_img = img.crop((x, y, x + blur_size, y + 52))

        # the filter removes the alpha, you need to add it again by converting to RGBA
        blurred_img = cropped_img.filter(ImageFilter.GaussianBlur(20), ).convert("RGBA")

        # paste blurred, uses alphachannel of create_rounded_rectangle_mask() as mask
        # only those parts of the mask that have a non-zero alpha gets pasted
        img.paste(blurred_img, (x, y), create_rounded_rectangle_mask(cropped_img, radius))

        card_image_fname_root = card_image_fname[:card_image_fname.index('.')]
        img.save('temp_images/' + card_image_fname_root + '_CC_blured.jpg')
        if show is not None:
            img.show()


def get_casting_cost_length(card):
    card_raw_cc = card.mana_cost()
    # print(card_raw_cc)
    card_raw_temp = re.sub(r'{?\d?\d}', 'D', card_raw_cc)
    # print(f'{card_raw_temp} should have no double digits')
    card_raw_temp = re.sub(r'{./.}', 'H', card_raw_temp)
    # print(f'{card_raw_temp} should have no hybrid mana')
    card_cc = re.sub(r'{*.}', 'M', card_raw_temp)
    # print(f'There are {len(card_cc)} symbols in the casting cost {card_cc}')

    return card_cc


def test_blur_casting_cost():
    # TODO: make working for double faced cards
    # TODO: make name safe for a filename with a function
    # ask for a card name
    mtg_card = input("Enter the name of a MTG card:  ")

    # get card from Scryfall API
    card = scrython.cards.Named(fuzzy=mtg_card)

    # get card image

    r = requests.get(card.image_uris()['large'])
    card_name = card.collector_number() + "_" + "".join([c for c in card.name() if re.match(r'\w', c)]) + '.jpg'
    open('temp_images/' + card_name, 'wb').write(r.content)

    # get casting cost
    card_cc = get_casting_cost_length(card)

    # blur the casting cost
    blur_casting_cost(card_cc, card_name, show=True)


if __name__ == "__main__":
    print("\n\nMTG Programs - Main Menu\n\n")
    print("1) Get price of a card")
    print("2) List all cards of a set")
    print("3) List all multi-faced cards of a set")
    print("4) Take an instant quiz")
    print("5) List all MTG sets")
    print("6) MTG card body text: Max, Avg")
    print("7) Write sample Kahoot quiz Excel file")
    print("8) Make Kahoot Quiz from instant cards from a set")
    print("9) Download images of cards listed in deck.txt")
    print("10) Print removal cards from a set")
    print("11) Print removal data from all sets")
    print("12) Blur the casting cost for a card")
    print("\n")
    menu_choice = input("Your choice: ")

    if menu_choice == "1":
        get_price()
    elif menu_choice == "2":
        list_all_cards()
    elif menu_choice == "3":
        list_multifaced_cards()
    elif menu_choice == "4":
        mtg_set_instant_quiz()
    elif menu_choice == "5":
        list_all_sets(print_it=True)
    elif menu_choice == "6":
        mtg_body_text_info()
    elif menu_choice == "7":
        write_to_kahoot_excel_file()
    elif menu_choice == "8":
        make_kahoot_quiz()
    elif menu_choice == "9":
        getdeckimage.get_deck_images()
    elif menu_choice == "10":
        print_removal()
    elif menu_choice == "11":
        get_removal_data_on_all_sets()
    elif menu_choice == "12":
        test_blur_casting_cost()
    else:
        print("Not a valid choice!")
