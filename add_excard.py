import binascii
import nfc
from key_move import lock
from key_move import unlock
import time, os

def add_card():
	clf = nfc.ContactlessFrontend('usb')
	# 212F(FeliCa)
	target_req = nfc.clf.RemoteTarget("212F")
	# 0003(Suica)
	target_req.sensf_req = bytearray.fromhex("0000030000")

	print("Touch a Card")

	while True:
		target_res = clf.sense(target_req, iterations=10, interval=0.01)
		if target_res != None:
			card = binascii.hexlify(target_res.sensf_res) + '\n'
			data = open('/home/pi/key/excard.dat', 'r')
			flag = True
			for line in data:
				if card == line:
					print("This card has been already added")
					flag = False
					break

			if flag:
				with open('/home/pi/key/excard.dat', 'a') as f:
					f.write(card)
				f.close()
				print("added successfully")

			data.close()
			break
	clf.close()

if __name__ == '__main__':
	os.system("sudo systemctl stop key")
	add_card()
	time.sleep(2)
	os.system("sudo systemctl start key")
