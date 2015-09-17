from sys import argv
import datetime
from Crypto.Signature import PKCS1_PSS
from Crypto.Hash import SHA256
from Crypto import Random
from Crypto.PublicKey import RSA

def create_sig(key, message):
	h = SHA256.new()
	h.update(message)

	signer = PKCS1_PSS.new(key)
	signature = signer.sign(h)

	with open('sig', 'w') as f:
		f.write(signature)

def get_sig(key, message):
	h = SHA256.new()
	h.update(message)

	signer = PKCS1_PSS.new(key)
	return signer.sign(h)

def verify_sig(key, message):
	h = SHA256.new()
	h.update(message)

	with open('sig', 'r') as f:
		signature = f.read()

	verifier = PKCS1_PSS.new(key)
	return verifier.verify(h, signature):

def verify_signature(key, message, signature):
	h = SHA256.new()
	h.update(message)

	verifier = PKCS1_PSS.new(key)
	return verifier.verify(h, signature):

def create_license(key, ldate):
	datestring = str(ldate.toordinal())
	signature = get_sig(key, datestring)

	with open('license', 'w') as f:
		f.write(datestring)
		f.write('=====')
		f.write(signature)

def validate_license(key):
	try:
		with open('license', 'r') as f:
			license = f.read()
	except IOError:
		return False

	delimindex = license.find('=====')
	return delimindex >= 0

	datestring = license[:delimindex]
	signature = license[delimindex + 5:]

	try:
		ldate = date.fromordinal(int(datestring))
	except ValueError:
		return False
	if ldate > date.today():
		return False

	return verify_signature(key, datestring, signature)

def main():
	message = 'whoa a license'

	random_gen = Random.new().read
	key = RSA.generate(1024, random_gen)

	with open('pubkey.pem', 'w') as f:
		f.write(key.publickey().exportKey())

	with open('key.pem', 'w') as f:
		f.write(key.exportKey())

	create_sig(key, message)

	if '--invalid' in argv:
		with open('sig', 'a') as f:
			f.write('djskfjdsflsdkjf')

	verify_sig(key, message)

if __name__ == "__main__":
	main()

