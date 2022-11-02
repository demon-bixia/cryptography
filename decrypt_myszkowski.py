"""decrypt_myszkowski.py"""


def book_slots(text: str, key: int) -> list:
    """
    create a number of rows with empty strings
    """
    number_of_rows = round(len(text)/key)

    slots = []

    for _ in range(key):
        slots.append([''] * number_of_rows)

    return slots


def join_message(message_list: list, key: int):
    """combine a list messages into one message"""
    joined_message = ''

    counter = 0

    for _ in range(round(key/2)):

        for item in message_list:
            joined_message += item[counter]

        counter += 1

    return joined_message


def decrypt(text: str, key: int) -> str:
    """
    decrypt the myszkowski cypher
    """
    rows = book_slots(text, key)
    shade = key * round(key/2) - len(text)
    counter = 0

    for row_index, row in enumerate(rows):
        for index in range(round(key/2)):
            if counter < len(text):
                if index == 3 and row_index >= len(rows) - shade:
                    pass
                else:
                    row[index] = text[counter]
                    counter += 1

    return join_message(rows, key)
