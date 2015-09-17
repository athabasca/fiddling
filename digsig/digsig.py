from sys import argv
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

def verify_sig(key, message):
	h = SHA256.new()
	h.update(message)

	with open('sig', 'r') as f:
		signature = f.read()

	verifier = PKCS1_PSS.new(key)
	if verifier.verify(h, signature):
		print 'Valid license'
	else:
		print 'Invalid license'

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

