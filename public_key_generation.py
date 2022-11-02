"""public_key_generation.py"""
import random
import os
import prime_numbers
import crypto_math


def generate_key(keySize):
    """
    Creates a public/private key pair with keys that are keySize bits in
    size. This function may take a while to run.
    """

    # Step 1: Create two prime numbers, p and q. Calculate n = p * q.
    print('Generating p prime...')
    p = prime_numbers.generate_large_prime(keySize)
    print('Generating q prime...')
    q = prime_numbers.generate_large_prime(keySize)
    n = p * q

    # Step 2: Create a number e that is relatively prime to (p-1)*(q-1).
    print('Generating e that is relatively prime to (p-1)*(q-1)...')
    while True:
        # Keep trying random numbers for e until one is valid.
        e = random.randrange(2 ** (keySize - 1), 2 ** (keySize))
        if crypto_math.gcd(e, (p - 1) * (q - 1)) == 1:
            break

    # Step 3: Calculate d, the mod inverse of e.
    print('Calculating d that is mod inverse of e...')
    d = crypto_math.find_modular_inverse(e, (p - 1) * (q - 1))

    public_key = (n, e)
    private_key = (n, d)

    print('Public key:', public_key)
    print('Private key:', private_key)

    return (public_key, private_key)


def make_key_files(name, key_size):
    """
    Creates two files 'x_pubkey.txt' and 'x_privkey.txt' (where x is the
    value in name) with the the n,e and d,e integers written in them,
    delimited by a comma.

    Our safety check will prevent us from overwriting our old key files:
    """
    if os.path.exists(f'{name}_pubkey.txt') or os.path.exists(f'{name}_privkey.txt'):
        raise Exception(
            f'WARNING: The file {name}_pubkey.txt or {name}_privkey.txt already exists!\
            Use a different name or delete these files and re-run this program.')

    public_key, private_key = generate_key(key_size)

    print(
        f'The public key is a {len(str(public_key[0]))} and a {len(str(public_key[1]))} digit number.')
    print(f'Writing public key to file {name}_pubkey.txt...\n')
    fo = open(f'{name}_pubkey.txt', 'w')
    fo.write(f'{key_size},{public_key[0]},{public_key[1]}')
    fo.close()

    print(
        f'The private key is a {len(str(public_key[0]))} and a {len(str(public_key[1]))} digit number. \n')
    print(f'Writing private key to file {name}_privkey.txt...')
    fo = open(f'{name}_privkey.txt', 'w')
    fo.write(f'{key_size},{private_key[0]},{private_key[1]}')
    fo.close()


def main():
    """
    create a public/private keypair with 1024 bit keys
    """
    print('Making key files...')
    make_key_files('al_sweigart', 1024)
    print('Key files made.')


if __name__ == '__main__':
    main()
