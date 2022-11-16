"""playfair.py"""
import string

# Save the indexs where bogus were added
BOGUS_LOCATIONS = []
SPACE_LOCATIONS = []


def remove_bogus_location(plain_text: str):
    """
    remove location
    """
    plain_text_list = list(plain_text)

    for index in BOGUS_LOCATIONS:
        plain_text_list[index] = ''

    return "".join(plain_text_list)


def add_spaces(plain_text: str):
    """
    add spaces back to plaintext
    """
    plain_text_list = list(plain_text)

    for index in SPACE_LOCATIONS:
        plain_text_list.insert(index, ' ')

    return "".join(plain_text_list)


def create_keys(key: str):
    """
    create a 5x5 key grid with the keyword written first
    """
    alphabets = string.ascii_lowercase.replace('j', '.')
    key_grid = ['' for i in range(5)]

    key = key.lower()

    letter_index = 0
    group_index = 0

    for letter in key:
        if letter in alphabets:
            key_grid[letter_index] += letter
            alphabets = alphabets.replace(letter, '.')
            group_index += 1
            if group_index > 4:
                letter_index += 1
                group_index = 0

    for letter in alphabets:
        if letter != '.':
            key_grid[letter_index] += letter

            group_index += 1
            if group_index > 4:
                letter_index += 1
                group_index = 0

    return key_grid


def split_plain_text(plain_text: str):
    """
    split text into pairs and add bugos letters
    """
    index = 0
    plain_text_pairs = []

    while index < len(plain_text):
        first_letter = plain_text[index]
        if (index + 1) == len(plain_text):
            # if the last pair is less than 2 add x
            second_letter = 'x'
            BOGUS_LOCATIONS.append(index + 2)
        else:
            # else add the second letter of the pair
            second_letter = plain_text[index + 1]

        if first_letter != second_letter:
            # if the letters are not equal then add them to plain_text_pairs
            plain_text_pairs.append(first_letter + second_letter)
            index += 2
        else:
            # else if the letter is repeated then add x instead of the second
            # ones
            plain_text_pairs.append(first_letter + 'x')
            BOGUS_LOCATIONS.append(index + 1)
            index += 1

    return plain_text_pairs


def split_cipher_text(cipher_text: str):
    """
    split cipher text into pairs
    """
    cipher_text_pairs = []
    index = 0

    while index < len(cipher_text):
        first_letter = cipher_text[index]
        second_letter = cipher_text[index + 1]
        cipher_text_pairs.append(first_letter + second_letter)
        index += 2

    return cipher_text_pairs


def playfair(plain_text: str, key: str, decrypt: bool = False):
    """
    encrypt plaintext using playfair cypher.
    """
    plain_text_pairs = []
    cipher_text_pairs = []

    # create the key grid
    key_grid = create_keys(key)

    # record the location of white spaces
    for index, letter in enumerate(plain_text):
        if letter == ' ':
            SPACE_LOCATIONS.append(index)

    # remove spaces and convert to lower case
    text = plain_text.replace(' ', '')
    text = text.lower()

    # split plaintext into pairs and add bogus letters
    plain_text_pairs = split_cipher_text(
        text) if decrypt else split_plain_text(text)

    for pair in plain_text_pairs:
        skip = False

        # loop the keygrid rows
        for row in key_grid:
            # if the pair are in the same row
            if pair[0] in row and pair[1] in row:
                pair_1_index = row.find(pair[0])
                pair_2_index = row.find(pair[1])
                if decrypt:
                    # if we are decrypting replace them with the item right to them
                    cipher_text_pair = row[(pair_1_index + 4) %
                                           5] + row[(pair_2_index + 4) % 5]
                else:
                    # if we are encrypting replace them with the item right to them
                    cipher_text_pair = row[(pair_1_index + 1) %
                                           5] + row[(pair_2_index + 1) % 5]

                cipher_text_pairs.append(cipher_text_pair)
                skip = True

        # and skip to the next pair
        if skip:
            continue

        # loop the key grid columns
        for col_index in range(5):
            # extract columns from grid
            col = "".join([key_grid[row_index][col_index]
                          for row_index in range(5)])

            # and if the pairs are in the same columns
            if pair[0] in col and pair[1] in col:
                pair_1_index = col.find(pair[0])
                pair_2_index = col.find(pair[1])
                if decrypt:
                    # if we are decrypting replace replace them with the letters upove them
                    cipher_text_pair = col[(pair_1_index + 4) %
                                           5] + col[(pair_2_index + 4) % 5]
                else:
                    # if we are encrypting replace them with the letters below them
                    cipher_text_pair = col[(pair_1_index + 1) %
                                           5] + col[(pair_2_index + 1) % 5]
                cipher_text_pairs.append(cipher_text_pair)
                skip = True

        # then skip to the next pair
        if skip:
            continue

        letter_1_row_index = 0
        letter_1_col_index = 0

        letter_2_row_index = 0
        letter_2_col_index = 0

        # loop the keygrid rows
        for index, row in enumerate(key_grid):
            # get the position of the 2 letters in the keygrid
            if pair[0] in row:
                letter_1_row_index = index
                letter_1_col_index = row.find(pair[0])
            if pair[1] in row:
                letter_2_row_index = index
                letter_2_col_index = row.find(pair[1])

        # replace the letter with letter in the column index of the second letter index
        cipher_text_pair = key_grid[letter_1_row_index][letter_2_col_index] + \
            key_grid[letter_2_row_index][letter_1_col_index]
        cipher_text_pairs.append(cipher_text_pair)

    cipher_text = "".join(cipher_text_pairs)

    if decrypt:
        cipher_text = add_spaces(remove_bogus_location(cipher_text))
        BOGUS_LOCATIONS = []

    return cipher_text


def main():
    """
    run playfiar program
    """
    plain_text = "hello world"
    key = "abcde"

    cipher_text = playfair(plain_text, key)
    print(cipher_text)

    plain_text = playfair(cipher_text, key, True)
    print(plain_text)


if __name__ == "__main__":
    main()
