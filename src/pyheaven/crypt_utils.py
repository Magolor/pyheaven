from .misc_utils import RandString
from .file_utils import *
import hashlib
import string
import random
import base64

def Encrypt(bytes:bytearray, password:str=""):
	"""Encrypting a bytearray object with a password.

	This is a simple method of encryption, which does not guarantee security. Please do not encrypt important personal data via this.

	Args:
		bytes (bytearray): The bytearray to be encrypted.
		password (str): The password string.
	Returns:
		str: Return the cipher.
	"""
	random_state = random.getstate()
	h = hashlib.sha512(); h.update(password.encode("utf-8")); p = h.hexdigest(); assert(len(p)==128)
	b = list(base64.b64encode(bytes).decode('ascii'))
	base64charset = string.ascii_uppercase+string.ascii_lowercase+string.digits+"+/"
	for i in range(8):
		hexseed = p[i*16:(i+1)*16]; seed = int(hexseed, base=16); random.seed(seed)
		s = RandString(64,charset=base64charset); b.extend(s)
	for i in range(8):
		hexseed = p[i*16:(i+1)*16]; seed = int(hexseed, base=16)
		random.seed(seed); random.shuffle(b)
	random.setstate(random_state)
	return "".join(b)

def Decrypt(cipher:str, password:str=""):
	"""Decrypting a cipher, which was a bytearray object encrypted by `Encrypt` with the same password.

	Args:
		bytes (bytearray): The cipher to be decrypted.
		password (str): The password string.
	Returns:
		str: Return the decrypted bytearray object.
	"""
	try:
		random_state = random.getstate()
		h = hashlib.sha512(); h.update(password.encode("utf-8")); p = h.hexdigest(); assert(len(p)==128)
		k = [i for i in range(len(cipher))]; b = ["0" for _ in range(len(cipher))]
		for i in range(8):
			hexseed = p[i*16:(i+1)*16]; seed = int(hexseed, base=16)
			random.seed(seed); random.shuffle(k)
		for i,c in zip(k,cipher):
			b[i] = c
		random.setstate(random_state)
		b = ("".join(b))[:-512].encode('ascii')
		return base64.b64decode(b)
	except:
		raise Exception("Incorrect password or corrupted cipher!")
