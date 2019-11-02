import binascii
import nfc
from key_move import lock
from key_move import unlock
from key_move import wrongCard
from sensor import measure
import os, time, sys


def main():

	os.system("sudo servod --p1pins=11")
	clf = nfc.ContactlessFrontend('usb')
	# 212F(FeliCa)
	target_req = nfc.clf.RemoteTarget("212F")
	# 0003(Suica)
	target_req.sensf_req = bytearray.fromhex("0000030000")

	key_state = True # lock position

	while True:
		try:
			target_res = clf.sense(target_req, iterations=10, interval=0.01)

			if target_res != None:

				card = binascii.hexlify(target_res.sensf_res) + '\n'
				data = open('/home/pi/key/suica.dat', 'r')
				excards = open('/home/pi/key/excard.dat', 'r')
				auth = False
				is_excard = False

				for line in excards:
					if card == line:
						print("Express Card : the Key will be Locked Automatically")
						is_excard = True
						unlock()
						print("Unlocked the key")

						print("Open the door")
						time.sleep(2)
						while True:
							distance = measure()
						#	print(distance)
							if distance > 20:
								break
							time.sleep(0.1)

						print("Close the door")
						time.sleep(2)
						while True:
							distance = measure()
						#	print(distance)
							if distance < 4:
								time.sleep(1)
								lock()
								print("Locked the key")
								break
							time.sleep(0.1)

				if is_excard:
					continue

				# check the card
				for line in data:
					# if the Card is Registered
					if card == line:
						print("Successiful")
						auth = True
						if key_state: # if Locked
							unlock()
							print("Unlocked the key")
							key_state = False
						else:	      # if Unlocked
							lock()
							print("Locked the key")
							key_state = True
						break

				# if the card is WRONG
				if not auth:
					print("Wrong Card")
					wrongCard(key_state)

				data.close()

		except KeyboardInterrupt:
			pass
			print("exit: Keyboard Intterrupt")
			lock()
			os.system("sudo killall servod")
			break

		except IOError:
			pass
			print("exit: IO Error")
			lock()
			os.system("sudo killall servod")
			break

		time.sleep(0.05)


	clf.close()

if __name__ == '__main__':
	main()
