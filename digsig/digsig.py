from Crypto.Signature import PKCS1_PSS
from Crypto.Hash import SHA256
from Crypto import Random
from Crypto.PublicKey import RSA

message = 'whoa a license'

random_gen = Random.new().read
key = RSA.generate(1024, random_gen)

def create_sig():
	h = SHA256.new()
	h.update(message)

	signer = PKCS1_PSS.new(key)
	signature = signer.sign(h)

	with open('sig', 'w') as f:
	f.write(signature)

def verify_sig():
	h = SHA256.new()
	h.update(message)

	# decrypt signature with public key
	# compare to hash

