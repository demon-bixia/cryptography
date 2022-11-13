import os
from reverse import reverse
from cesar2 import cesar
from playfair import playfair

ciphers = {
    '1': cesar,
    '2': reverse,
    '3': playfair,
}

while True:
    # select cipher 
    select_choice_text = "select the encryption algorithm:\n\
      1. ceaser cipher \n\
      2. reverse cipher \n\
      3. playfair cipher\n\
      4. exit\n"    
    choice = input(select_choice_text)

    os.system('clear')

    # exit if choice is 4
    if choice == '4':
      break
    
    # if choice not in dict print error and continue
    if choice not in ciphers:
      print('please select a choice from the menu !\n')
      continue

    # select mode
    select_mode_text = "select the algorithm mode:\n\
    1. encrypt\n\
    2. decrypt\n"
    mode = int(input(select_mode_text)) == '2' if choice != '2' else None

    # enter arguments
    input_text = input("enter the text you want to encrypt: ")
    key = int(input("enter the encryption key: ")) if choice != '2' else None

    # run cipher and print result
    output_text = ciphers[choice](input_text, key, mode) if choice != '2' else ciphers[choice](input_text)
    print('\noutput: ', output_text, '\n')