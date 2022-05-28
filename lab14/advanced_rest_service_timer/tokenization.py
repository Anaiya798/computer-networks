import random
import string

TOKEN_LENGTH = 6

tokens = []


def generate_token():
    letters_and_digits = string.ascii_letters + string.digits
    token = ''.join(random.sample(letters_and_digits, TOKEN_LENGTH))
    tokens.append(token)
    print(token)
    return token
