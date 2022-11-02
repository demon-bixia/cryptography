"""public_key_encryption.py"""
import math

SYMBOLS = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz1234567890 !?.'


def get_blocks_from_text(message, block_size):
    """
    Converts a string message to a list of block integers
    """
    for character in message:
        if character not in SYMBOLS:
            raise Exception(
                f"ERROR: The symbol set does not have the character {character}")

        block_ints = []

    for block_start in range(0, len(message), block_size):
        # Calculate the block integer for this block of text:
        block_int = 0

        for index in range(block_start, min(block_start + block_size, len(message))):
            block_int += SYMBOLS.index(message[index]) * \
                (len(SYMBOLS) ** (index % block_size))

            block_ints.append(block_int)

    return block_ints


def get_text_from_blocks(block_ints, message_length, block_size):
    """
        Converts a list of block integers to the original message string.
        The original message length is needed to properly convert the last
        block integer.
    """
    message = []

    for block_int in block_ints:
        block_message = []

        for index in range(block_size - 1, -1, -1):
            if len(message) + index < message_length:
                char_index = block_int // (len(SYMBOLS) ** index)
                block_int = block_int % (len(SYMBOLS) ** index)

                block_message.insert(0, SYMBOLS[char_index])

        message.extend(block_message)

    return ''.join(message)


def encrypt_message(message, key, block_size):
    """
    Converts the message string into a list of block integers, and then
    encrypts each block integer. Pass the PUBLIC key to encrypt.
    """
    encrypted_blocks = []
    n, e = key

    for block in get_blocks_from_text(message, block_size):
        # ciphertext = plaintext ^ e mod n
        encrypted_blocks.append(pow(block, e, n))

    return encrypted_blocks


def decrypt_message(encrypted_blocks, message_length, key, block_size):
    """
    Decrypts a list of encrypted block ints into the original message
    string. The original message length is required to properly decrypt
    the last block. Be sure to pass the PRIVATE key to decrypt.
    """
    decrypted_blocks = []
    n, d = key

    for block in encrypted_blocks:
        # plaintext = ciphertext ^ d mod n
        decrypted_blocks.append(pow(block, d, n))

    return get_text_from_blocks(decrypted_blocks, message_length, block_size)


def read_key_file(key_filename):
    """
    Given the filename of a file that contains a public or private key,
    return the key as a (n,e) or (n,d) tuple value.
    """
    file_open = open(key_filename)
    content = file_open.read()
    file_open.close()
    key_size, n, e_or_d = content.split(',')
    return (int(key_size), int(n), int(e_or_d))


def encrypt_and_write_to_file(message_filename, key_filename, message, block_size=None):
    """
    Using a key from a key file, encrypt the message and save it to a
    file. Returns the encrypted message string.
    """
    key_size, n, e = read_key_file(key_filename)

    # If blockSize isn't given, set it to the largest
    # size allowed by the key size and symbol set size.
    if block_size is None:
        block_size = int(math.log(2 ** key_size, len(SYMBOLS)))

        # Check that key size is large enough for the block size:
        if not math.log(2 ** key_size, len(SYMBOLS)) >= block_size:
            raise Exception(
                'ERROR: Block size is too large for the key \
                and symbol set size. Did you specify the correct \
                key file and encrypted file?')

    # encrypt the message
    encrypted_blocks = encrypt_message(message, (n, e), block_size)

    # convert the large int values to one string value
    for index, _ in enumerate(encrypted_blocks):
        encrypted_blocks[index] = str(encrypted_blocks[index])

    encrypted_content = ','.join(encrypted_blocks)
    encrypted_content = f'{len(message)}_{block_size}_{encrypted_content}'

    # write the message to file
    file_open = open(message_filename, 'w')
    file_open.write(encrypted_content)
    file_open.close()

    # also return the encrypted string
    return encrypted_content


def read_from_fle_and_decrypt(message_filename, key_filename):
    """
    Using a key from a key file, read an encrypted message from a file
    and then decrypt it. Returns the decrypted message string.
    """
    key_size, n, d = read_key_file(key_filename)

    file_open = open(message_filename)
    content = file_open.read()
    file_open.close()

    message_length, block_size, encrypted_message = content.split('_')
    message_length = int(message_length)
    block_size = int(block_size)

    # Check that key size is large enough for the block size:
    if not math.log(2 ** key_size, len(SYMBOLS)) >= block_size:
        raise Exception("ERROR: Block size is too large for the key and symbol \
        set size. Did you specify the correct key file and encrypted file?'")

    # Convert the encrypted message into large int values:
    encrypted_blocks = []

    for block in encrypted_message.split(','):
        encrypted_blocks.append(int(block))

    # decrypt the large int values
    return decrypt_message(encrypted_blocks, message_length, (n, d), block_size)


def main():
    """
    Runs a test that encrypts a message to a file or decrypts a message from a file.
    """
    filename = f'encrypted_file.txt'
    mode = 'decrypt'

    if mode == 'encrypt':
        message = 'Journalists belong in the gutter because that is where \
                  the ruling classes throw their guilty secrets. Gerald Priestland. \
                  The Founding Fathers gave the free press the protection it must \
                  have to bare the secrets of government and inform the people. \
                  Hugo Black.'

        public_key_filename = 'al_sweigart_pubkey.txt'
        print('Encrypting and writing to {filename}...\n')

        encrypted_text = encrypt_and_write_to_file(
            filename, public_key_filename, message)

        print('encypted text:')
        print(encrypted_text)

    elif mode == 'decrypt':
        privous_key_filename = 'al_sweigart_privkey.txt'
        print(f"reading from {filename} and decrypting...")
        decrypted_text = read_from_fle_and_decrypt(
            filename, privous_key_filename)

        print('decrypted text: ')
        print(decrypted_text)


if __name__ == "__main__":
    main()
