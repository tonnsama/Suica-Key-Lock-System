import binascii
import nfc
from key_move import lock
from key_move import unlock
import time, os, sys

filename_normal_cards = "/home/pi/key/data/normal_cards.dat"
filename_auto_close_cards = "/home/pi/key/data/auto_close_cards.dat"

def add_card():
	clf = nfc.ContactlessFrontend('usb')
	# 212F(FeliCa)
	target_req = nfc.clf.RemoteTarget("212F")
	# 0003(Suica)
	target_req.sensf_req = bytearray.fromhex("0000030000")

	print("Touch a Card")
	args = sys.argv

	while True:
		if args.len() != 2 or args[1] != "n" or args[1] != "a":
			print("Please set your option n for normal or a for auto close")
			break

		target_res = clf.sense(target_req, iterations=10, interval=0.01)
		if target_res != None:

			card = binascii.hexlify(target_res.sensf_res) + '\n'
			normal_cards = open(filename_normal_cards, 'r')
			auto_close_cards = open(filename_auto_close_cards, 'r')
			flag = True

			# Check if it's in "normal_cards.dat"
			for line in normal_cards:
				if card == line:
					print("This card is already registered as a Normal Card")
					flag = False
					break

			# Check if it's in "auto_close_cards.dat"
			for line in auto_close_cards:
				if card == line:
					print("This card is already registerd as an Auto Close Card")
					flag = False
					break

			if flag:
				# Add the card as a Normal Card
				if args[1] == "n":
					with open(filename_normal_cards, 'a') as f:
						f.write(card)
					f.close()
					print("Added as a Normal Card")

				# Add the card as an Auto Close Card
				if args[1] == "a":
					with open(filename_auto_close_cards, 'a') as f:
						f.write(card)
					f.close()
					print("Added as an Auto Close Card")

			normal_cards.close()
			auto_close_cards.close()
			break
	clf.close()

if __name__ == '__main__':
	os.system("sudo systemctl stop key")
	add_card()
	time.sleep(2)
	os.system("sudo systemctl start key")
