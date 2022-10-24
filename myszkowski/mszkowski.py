"""mszkowski.py"""
from utils import encrypt, decrypt


def main():
    """
    run misyzkowski program
    """
    cypher = encrypt("Common sense is not so common.", 8)
    print(cypher, '\n')

    print(decrypt(cypher, 8))


if __name__ == '__main__':
    main()
