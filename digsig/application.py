from sys import exit
from datetime import date
from Crypto.Signature import PKCS1_PSS
from Crypto.Hash import SHA256
from Crypto import Random
from Crypto.PublicKey import RSA

# return values for validate_license
LICENSE_VALID = 0
LICENSE_INVALID = 1
LICENSE_EXPIRED = 2

def verify_signature(key, message, signature):
	h = SHA256.new()
	h.update(message)

	verifier = PKCS1_PSS.new(key)
	return verifier.verify(h, signature)

def validate_license(key, f):
	license = f.read()

	delimindex = license.find('=====')
	if delimindex == -1:
		return LICENSE_INVALID

	datestring = license[:delimindex]
	signature = license[delimindex + 5:]

	if not verify_signature(key, datestring, signature):
		return LICENSE_INVALID

	try:
		ldate = date.fromordinal(int(datestring))
	except ValueError:
		return LICENSE_INVALID
	if ldate < date.today():
		return LICENSE_EXPIRED

	return LICENSE_VALID

def main():
	# import public key
	try:
		with open('pubkey.pem', 'r') as f:
			key = RSA.importKey(f.read())
	except IOError:
		print('Error: "pubkey.pem" not found.')
		exit(1)

	# open license file
	try:
		f = open('license', 'r')
	except IOError:
		print('Error: "license" not found')
		exit(1)

	# validate license
	status = validate_license(key, f)
	if status == LICENSE_INVALID:
		print('Error: invalid license file')
		exit(1)
	elif status == LICENSE_EXPIRED:
		print('Error: license expired')
		exit(1)
	elif status == LICENSE_VALID:
		# run application
		print('PYEEEEEEOUUUUWWWWW application launch!')
		print('pssshhh application finished...')
		exit(0)
	else:
		print('Mysterious error: with useless message')
		exit(1)

if __name__ == '__main__':
	main()
