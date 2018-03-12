import bcrypt
import string
import random
import os

# -----
# Utils
# -----


def str_to_bytes(strng):
    return str.encode(strng)


def bytes_to_str(byts):
    return byts.decode()


# ----------------
# Crypto functions
# ----------------

def hashpw(password):
    # str to bytes array
    passwd = str_to_bytes(password)

    # hash password
    hashed = bcrypt.hashpw(passwd, bcrypt.gensalt())

    # bytes to str
    return bytes_to_str(hashed)


def checkpw(password, hashed):
    # str to bytes array
    passwd = str_to_bytes(password)
    hashwd = str_to_bytes(hashed)

    if bcrypt.checkpw(passwd, hashwd):
        return True
    else:
        return False


def gentoken():
    alpha = string.ascii_uppercase + string.digits + string.ascii_lowercase
    return ''.join(random.choice(alpha) for _ in range(32))
