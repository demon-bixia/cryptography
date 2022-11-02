"""caesar2.py"""

# every possible symbol that can be encrypted
LETTERS_UPPERCASE = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
LETTERS_LOWERCASE = 'abcdefghijklmnopqrstuvwxyz'
NUMBERS = '0123456789'
SYMBOLS = ' !"#$%&\'()*+,-./:;[\\]^_`{|}~<=>?@'


def get_symbol_group(symbol: str) -> str:
    """
    return the symbol group the symbol belongs to
    """
    if symbol.isnumeric():
        return NUMBERS
    if symbol.islower():
        return LETTERS_LOWERCASE
    if symbol.isupper():
        return LETTERS_UPPERCASE

    return SYMBOLS


def cesar(message: str, key: int = 3, mode: str = "encrypt") -> str:
    """
    encrypt / decrypt messages using cesar cypher
    """
    # stores the encrypted/decrypted form of the message
    translated = ''

    # run the encryption/decryption code on each symbol in the message string
    for symbol in message:
        # get the symbol group the character belongs to
        group = get_symbol_group(symbol)

        if symbol in group:
            # get the encrypted (or decrypted) number for this symbol
            index = group.find(symbol)  # get the number of the symbol

            if mode == 'encrypt':
                index = index + key
            elif mode == 'decrypt':
                index = index - key

            # handle the wrap-around if num is larger than the length of
            # LETTERS or less than 0
            if index >= len(group):
                index = index % len(group)
            elif index < 0:
                index = index % len(group)

            # add encrypted/decrypted number's symbol at the end of translated
            translated = translated + group[index]

        else:
            # just add the symbol without encrypting/decrypting
            translated = translated + symbol

    # return the translated message
    return translated


def main() -> None:
    """
    run cesar2.py app
    """
    # the string to be encrypted/decrypted
    plaintext = input('Enter the message you want to encrypt: ')
    # the encryption/decryption key
    key = int(input('enter The encryption key: '))

    # encrypt messages using cesar cypher
    cyphertext = cesar(plaintext, key=key, mode="encrypt")
    # print the encrypted message
    print("encrypted message: ", cyphertext)

    # decrypted messages using cesar cypher
    plaintext = cesar(cyphertext, key=key, mode="decrypt")
    # print the decrypted message
    print("decrypted message: ", plaintext)


if __name__ == '__main__':
    main()
