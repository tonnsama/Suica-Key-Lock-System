import binascii
import nfc
from key_move import lock
from key_move import unlock
import time

def main():
	clf = nfc.ContactlessFrontend('usb')
	# 212F(FeliCa)
	target_req = nfc.clf.RemoteTarget("212F")
	# 0003(Suica)
	target_req.sensf_req = bytearray.fromhex("0000030000")

	while True:
		target_res = clf.sense(target_req, iterations=10, interval=0.01)
		if target_res != None:
			card = binascii.hexlify(target_res.sensf_res)
			print(card)
			break
	clf.close()

if __name__ == '__main__':
	main()
