def format_seconds_to_mmss(seconds):
    minutes = seconds // 60
    seconds %= 60
    return "%02i:%02i" % (minutes, seconds)


def format_bytes(size):
    # 2**10 = 1024
    power = 2**10
    n = 0
    power_labels = {0: '', 1: 'K', 2: 'M', 3: 'G', 4: 'T'}
    while size > power:
        size /= power
        n += 1
    return f"{size:.2f} {power_labels[n]}B"


def get_deck_images():
    from sys import getsizeof
    import json
    import requests
    import time

    start_db_load = time.time()
    with open('./venv/all-cards.json', 'r', encoding='utf-8') as f:
        cards = json.load(f)
    end_db_load = time.time()
    elapsed_time = end_db_load - start_db_load

    print("DB load time: " + format_seconds_to_mmss(elapsed_time))
    print(f"DB memory size: {format_bytes(getsizeof(cards))}")

    with open('./venv/Deck.txt') as f:
        deck = f.readlines()

    for item in deck:
        current_card = item[2:].strip()
        print(current_card)
        found = 0

        for card in cards:
            if card['name'] == current_card and card['lang'] == 'en' and found == 0:
                r = requests.get(card['image_uris']['large'])
                card_name = card["collector_number"] + "_" + card['name'] + '.jpg'
                open(card_name, 'wb').write(r.content)
                found = 1

        if found == 0:
            print(current_card + 'not found')
