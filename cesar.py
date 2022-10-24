"""cesar.py"""

import string


alphabets = [*string.ascii_lowercase]


def forward(index: int, shift: int) -> int:
    """
    get the index of the next letter in the aplhabet
    """
    next_index = round(index + shift) % 24 if index + \
        shift > 24 else index + shift

    return next_index


def backward(index: int, shift: int) -> int:
    """
    get the index of the original letter in the alphabet
    """
    return round(index - shift) % 24


def cesar(text: str, shift: int, decrypt: bool = False) -> str:
    """
    encypt text using cesar algorithm
    """
    cypher = str()

    for letter in text:
        try:
            index_of_letter = alphabets.index(letter)
            new_letter_index = forward(
                index_of_letter, shift) if not decrypt else backward(index_of_letter, shift)
            cypher = cypher + alphabets[new_letter_index]
        except ValueError:
            cypher = cypher + letter

    return cypher


def hack_cesar(text: str):
    """display a list of every possible decryption"""
    for index in range(len(alphabets)):
        print(cesar(text, index+1, True), '\n')


def main():
    """
    execute ceasar program
    """

    encrypted_cypher = cesar('hello world', 24)
    print('encryption: ', encrypted_cypher, '\n')

    print('decryption: ', cesar(encrypted_cypher, 24, True), '\n')

    print(hack_cesar.__doc__, '\n')
    hack_cesar(encrypted_cypher)


if __name__ == '__main__':
    main()
