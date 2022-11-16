import os
from reverse import reverse
from cesar2 import cesar
from playfair import playfair

ciphers = {
    '1': cesar,
    '2': reverse,
    '3': playfair,
}

os.system('cls')

while True:

    try:

        # select cipher
        select_choice_text = "select the encryption algorithm:\n\
		1. ceaser cipher \n\
		2. reverse cipher \n\
		3. playfair cipher\n\
		4. exit\n"
        choice = input(select_choice_text)

        # clear screen
        os.system('cls')

        # exit if choice is 4
        if choice == '4':
            break

        # select mode
        select_mode_text = "select the algorithm mode:\n\
		1. encrypt\n\
		2. decrypt\n"
        mode = input(select_mode_text) == '2' if choice != '2' else None
        # clear screen
        os.system('cls')

        # enter arguments
        input_text = input("enter the text you want to encrypt: ")
        key = input("enter the encryption key: ") if choice != '2' else None
        # clear screen
        os.system('cls')

        # cesar uses int keys
        if choice == '1':
            key = int(key)

        # run cipher and print result
        output_text = ciphers[choice](
            input_text, key, mode) if choice != '2' else ciphers[choice](input_text)
        print('\noutput: ', output_text, '\n')

    except:
        print("somthing went worng please try again")
