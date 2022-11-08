"""playfair.py"""
import string

# Save the indexs where bogus were added
BOGUS_LOCATIONS = []


def remove_bogus_location(plain_text: str):
    """
    remove location
    """
    plain_text_list = list(plain_text)

    for index in BOGUS_LOCATIONS:
        plain_text_list[index] = ''

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

    index = 0

    while index < len(plain_text):
        first_letter = plain_text[index]
        if (index + 1) == len(plain_text):
            second_letter = 'x'
            BOGUS_LOCATIONS.append(index + 2)
        else:
            second_letter = plain_text[index + 1]

        if first_letter != second_letter:
            plain_text_pairs.append(first_letter + second_letter)
            index += 2
        else:
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


def encrypt(plain_text: str, key: str):
    """
    encrypt plaintext using playfair cypher.
    """
    plain_text_pairs = []
    cipher_text_pairs = []

    key_grid = create_keys(key)

    text = plain_text.replace(' ', '')
    text = text.lower()

    plain_text_pairs = split_plain_text(text)

    for pair in plain_text_pairs:
        flag = False
        for row in key_grid:
            if pair[0] in row and pair[1] in row:
                row_index_1 = row.find(pair[0])
                row_index_2 = row.find(pair[1])
                cipher_text_pair = row[(row_index_1 + 1) %
                                       5] + row[(row_index_2 + 1) % 5]
                cipher_text_pairs.append(cipher_text_pair)
                flag = True

        if flag:
            continue

        for letter in range(5):
            col = "".join([key_grid[i][letter] for i in range(5)])
            if pair[0] in col and pair[1] in col:
                col_index_1 = col.find(pair[0])
                col_index_2 = col.find(pair[1])
                cipher_text_pair = col[(col_index_1 + 1) %
                                       5] + col[(col_index_2 + 1) % 5]
                cipher_text_pairs.append(cipher_text_pair)
                flag = True

        if flag:
            continue

        col_index_1 = 0
        col_index_2 = 0
        row_index_1 = 0
        row_index_2 = 0

        for index in range(5):
            row = key_grid[index]
            if pair[0] in row:
                col_index_1 = index
                row_index_1 = row.find(pair[0])
            if pair[1] in row:
                col_index_2 = index
                row_index_2 = row.find(pair[1])
        cipher_text_pair = key_grid[col_index_1][row_index_2] + \
            key_grid[col_index_2][row_index_1]
        cipher_text_pairs.append(cipher_text_pair)

    return "".join(cipher_text_pairs)


def decrypt(cipher_text, key):
    """
    decrypt playfair cypher ciphertext.
    """
    cipher_text = cipher_text.lower()
    plain_text_pairs = []
    cipher_text_pairs = []
    key_grid = create_keys(key)

    cipher_text_pairs = split_cipher_text(cipher_text)

    for pair in cipher_text_pairs:
        flag = False
        for row in key_grid:
            if pair[0] in row and pair[1] in row:
                row_index_1 = row.find(pair[0])
                row_index_2 = row.find(pair[1])
                plain_text_pair = row[(row_index_1 + 4) %
                                      5] + row[(row_index_2 + 4) % 5]
                plain_text_pairs.append(plain_text_pair)
                flag = True

        if flag:
            continue

        for counter in range(5):
            col = "".join([key_grid[index][counter] for index in range(5)])

            if pair[0] in col and pair[1] in col:
                col_index_1 = col.find(pair[0])
                col_index_2 = col.find(pair[1])
                plain_text_pair = col[(col_index_1 + 4) %
                                      5] + col[(col_index_2 + 4) % 5]
                plain_text_pairs.append(plain_text_pair)
                flag = True

        if flag:
            continue

        col_index_1 = 0
        col_index_2 = 0
        row_index_1 = 0
        row_index_2 = 0

        for index in range(5):
            row = key_grid[index]
            if pair[0] in row:
                col_index_1 = index
                row_index_1 = row.find(pair[0])
            if pair[1] in row:
                col_index_2 = index
                row_index_2 = row.find(pair[1])

        plain_text_pair = key_grid[col_index_1][row_index_2] + \
            key_grid[col_index_2][row_index_1]

        plain_text_pairs.append(plain_text_pair)

    return "".join(plain_text_pairs)


def main():
    """
    run playfiar program
    """
    plain_text = "hello world"
    key = "abcde"

    cipher_text = encrypt(plain_text, key)
    print(cipher_text)

    plain_text = remove_bogus_location(decrypt(cipher_text, key))
    print(plain_text)


if __name__ == "__main__":
    main()
