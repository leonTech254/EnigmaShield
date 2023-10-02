import random
import numpy as np
# Constants
ALPHABET_SIZE = 26

def generate_key_matrix(key, n):
    """Generate a key matrix for Hill Cipher."""
    key_matrix = np.zeros((n, n), dtype=int)
    k = 0
    for i in range(n):
        for j in range(n):
            key_matrix[i][j] = ord(key[k]) % ALPHABET_SIZE
            k += 1
    return key_matrix

def hill_cipher_encrypt(plain_text, key_matrix):
    """Encrypt a plain text using Hill Cipher."""
    n = len(key_matrix)
    plain_text = ''.join(filter(str.isalpha, plain_text.upper()))

    if len(plain_text) % n != 0:
        plain_text += 'X' * (n - len(plain_text) % n)

    cipher_text = ""
    for i in range(0, len(plain_text), n):
        block = np.array([ord(char) % ALPHABET_SIZE for char in plain_text[i:i+n]])
        result = np.dot(key_matrix, block) % ALPHABET_SIZE
        cipher_text += ''.join([chr(val + 65) for val in result])

    return cipher_text

def prepare_playfair_key(key):
    """Prepare the key matrix for Playfair Cipher."""
    key = key.upper().replace('J', 'I')
    unique_chars = sorted(set(key), key=key.index)

    # Pad the array if needed
    while len(unique_chars) % 5 != 0:
        unique_chars.append('X')

    playfair_matrix = np.array(list(unique_chars)).reshape(5, -1)
    return playfair_matrix


def playfair_cipher_encrypt(plain_text, key_matrix):
    """Encrypt a plain text using Playfair Cipher."""
    plain_text = plain_text.upper().replace('J', 'I')
    cipher_text = ""
    for i in range(0, len(plain_text), 2):
        pair = plain_text[i:i + 2]
        
        row1, col1 = np.where(key_matrix == pair[0])
        row2, col2 = np.where(key_matrix == pair[1])

        if row1.size > 0 and row2.size > 0 and col1.size > 0 and col2.size > 0:
            if row1 == row2:
                cipher_text += key_matrix[row1, (col1 + 1) % 5][0] + key_matrix[row2, (col2 + 1) % 5][0]
            elif col1 == col2:
                cipher_text += key_matrix[(row1 + 1) % 5, col1][0] + key_matrix[(row2 + 1) % 5, col2][0]
            else:
                cipher_text += key_matrix[row1, col2][0] + key_matrix[row2, col1][0]

    return cipher_text


def polygram_substitution_cipher_encrypt(plain_text, polygram_mapping):
    cipher_text = ""
    i = 0
    while i < len(plain_text):
        if i + 2 <= len(plain_text):
            polygram = plain_text[i:i+2]
            if polygram in polygram_mapping:
                cipher_text += polygram_mapping[polygram]
                i += 2
            else:
                cipher_text += plain_text[i]
                i += 1
        else:
            cipher_text += plain_text[i]
            i += 1

    return cipher_text

def cbc_encrypt(plaintext, key, iv):
    ciphertext = ""
    previous_block = np.array([ord(char) % ALPHABET_SIZE for char in iv])

    for i in range(0, len(plaintext), len(iv)):
        block = np.array([ord(char) % ALPHABET_SIZE for char in plaintext[i:i + len(iv)]])
        
        block ^= previous_block

        encrypted_block = hill_cipher_encrypt(''.join([chr(val + 65) for val in block]), generate_key_matrix(key, len(iv)))

        ciphertext += encrypted_block
        previous_block = np.array([ord(char) % ALPHABET_SIZE for char in encrypted_block])

    return ciphertext

def substitution_cipher_encrypt(text):
    """Encrypt text using a simple substitution cipher."""
    alphabet = list("ABCDEFGHIJKLMNOPQRSTUVWXYZ")
    shuffled_alphabet = list(alphabet)
    random.shuffle(shuffled_alphabet)
    
    substitution_dict = dict(zip(alphabet, shuffled_alphabet))

    encrypted_text = ''.join([substitution_dict.get(char, char) for char in text])
    
    return encrypted_text

def combined_cipher_encrypt(plain_text, hill_key, playfair_key, polygram_mapping, cbc_key, cbc_iv):
    substitution_cipher_text = substitution_cipher_encrypt(plain_text)

    hill_key_matrix = generate_key_matrix(hill_key, 3)
    playfair_matrix = prepare_playfair_key(playfair_key)
    hill_cipher_text = hill_cipher_encrypt(substitution_cipher_text, hill_key_matrix)
    playfair_cipher_text = playfair_cipher_encrypt(hill_cipher_text, playfair_matrix)
    polygram_cipher_text = polygram_substitution_cipher_encrypt(playfair_cipher_text, polygram_mapping)

    cbc_cipher_text = cbc_encrypt(polygram_cipher_text, cbc_key, cbc_iv)

    return cbc_cipher_text

hill_key = "GYBNQKURP"
playfair_key = "KEYWORD"
polygram_mapping = {'TH': 'PL', 'IS': 'AY', 'EX': 'CI', 'AM': 'HE', 'PL': 'TH', 'AY': 'IS', 'CI': 'EX', 'HE': 'AM'}
cbc_key = "CBCKEY"
cbc_iv = "CBCIV"

plaintext = "HELLO"

combined_cipher_text = combined_cipher_encrypt(plaintext, hill_key, playfair_key, polygram_mapping, cbc_key, cbc_iv)
print(f"Plaintext: {plaintext}")
print(f"Combined Encrypted Text: {combined_cipher_text}")

