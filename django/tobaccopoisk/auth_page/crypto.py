import bcrypt
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
	# gen random seed
	rand_bytes = os.urandom(16)
	# hash it
	bytes_token = bcrypt.hashpw(rand_bytes, bcrypt.gensalt())
	# decode bytes to str
	str_token = bytes_to_str(bytes_token)
	# return last 32 symbols
	return str_token[-32:]