import binascii
import nfc
from key_move import lock
from key_move import unlock
from key_move import wrongCard
from sensor import measure
import os, time, sys

OPEN_TIME = 5 # second
CLOSE_TIME = 60 # second
OPEN_DISTANCE = 7
CLOSE_DISTANCE = 4

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
				auth = False
				is_excard = False
				data = open('/home/pi/key/suica.dat', 'r')
				excards = open('/home/pi/key/excard.dat', 'r')

				for line in excards:
					if card == line:
						is_excard = True

				# if the Card is excard and Key is locked
				if is_excard:
					print("Express card ")
				if key_state:
					print("Current key state is Locked")
				else:
					print("Current key state is Unlocked")

				if is_excard and key_state:
					print("Express Card : the Key will be Locked Automatically")
					unlock()
					print("Unlocked the key")

					start_time = time.time()
					# Waiting for Opening the Door
					print("Open the door")
					time.sleep(2)
					while True:
						distance = measure()
						elapsed_time = time.time() - start_time
					#	print(distance)
						if distance > OPEN_DISTANCE or elapsed_time > OPEN_TIME:
							break
						time.sleep(0.1)

					print("Close the door")
					time.sleep(2)
					# Winting for Closing the Door
					while True:
						distance = measure()
						elapsed_time = time.time() - start_time
					#	print(distance)
						if distance < CLOSE_DISTANCE or elapsed_time > CLOSE_TIME:
							time.sleep(1)
							lock()
							print("Locked the key")
							break
						time.sleep(0.1)

					continue

				# if the Card is not an excard or Key is unlocked
				else:
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
