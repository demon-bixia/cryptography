def reverse(plaintext: str):
    """
    reverse the word
    """
    return plaintext[::-1]


def main():
    """
    run the reverse cipher program
    """
    plaintext = input('enter plain text: ')

    ciphertext = reverse(plaintext)
    print('cipertext: ', ciphertext, '\n')

    plaintext = reverse(ciphertext)
    print('plaintext: ', plaintext, '\n')


if __name__ == "__main__":
    main()
