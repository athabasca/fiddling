from datetime import date
from Crypto.Signature import PKCS1_PSS
from Crypto.Hash import SHA256
from Crypto import Random
from Crypto.PublicKey import RSA

def get_signature(key, message):
	h = SHA256.new()
	h.update(message)

	signer = PKCS1_PSS.new(key)
	return signer.sign(h)

def create_license(key, ldate):
	datestring = str(ldate.toordinal())
	signature = get_signature(key, datestring)

	with open('license', 'w') as f:
		f.write(datestring)
		f.write('=====')
		f.write(signature)

def main():
	# generate key
	random_gen = Random.new().read
	key = RSA.generate(1024, random_gen)

	# export public key
	with open('pubkey.pem', 'w') as f:
		f.write(key.publickey().exportKey())

	# create license file
	expiration = date.today()
	expiration = expiration.replace(year=expiration.year + 2)
	create_license(key, expiration)

if __name__ == '__main__':
	main()

