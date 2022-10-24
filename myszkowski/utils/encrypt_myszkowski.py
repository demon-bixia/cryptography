"""encrypt_myszkowski.py"""


def encrypt(text: str, key: int) -> str:
    """
    transposition algorithm
    """
    cypher = ''

    for column_index in range(key):
        character_index = column_index

        for _ in range(round(len(text)/key)):
            if character_index < len(text):
                cypher = cypher + text[character_index]

            character_index = character_index + key

    return cypher
