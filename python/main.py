import binascii
import nfc
import os, time, sys, datetime as dt

# User Python fuction
from key_move import lock
from key_move import unlock
from key_move import wrongCard
from sensor import measure


OPEN_TIME = 3 # second
CLOSE_TIME = 60 # second
OPEN_DISTANCE = 7 # cm
CLOSE_DISTANCE = 4 # cm

filename_normal_cards = "/home/pi/key/data/normal_cards.dat"
filename_auto_close_cards = "/home/pi/key/data/auto_close_cards.dat"
filename_log = "/home/pi/key/data/key.log"




def main():

	os.system("sudo servod --p1pins=11")
	clf = nfc.ContactlessFrontend('usb')
	# 212F(FeliCa)
	target_req = nfc.clf.RemoteTarget("212F")
	# 0003(Suica)
	target_req.sensf_req = bytearray.fromhex("0000030000")



	tmp_date = dt.date.today()
	key_state = True # lock position

	while True:
		try:

			# Open Log file
			today = dt.date.today()
			if today == tmp_date:
				logfile = open(filename_log, mode="a")
			else:
				logfile = open(filename_log, mode="w")


			target_res = clf.sense(target_req, iterations=10, interval=0.01)

			# s = "Touch your Card...\n"
			# print(s)
			# logfile.writelines(s)

			if target_res != None:

				card = binascii.hexlify(target_res.sensf_res) + '\n'
				auth = False
				is_auto_card = False
				normal_cards = open(filename_normal_cards, 'r')
				auto_close_cards = open(filename_auto_close_cards, 'r')

				for line in auto_close_cards:
					if card == line:
						is_auto_card = True

				# if it is an Auto Close Card and Key is Locked
				if is_auto_card:
					s = "Auto Close Card"
					print(s)
					logfile.write(s)

				if key_state:
					s = "Current key state is Locked"
					print(s)
					logfile.write(s)
				else:
					s = "Current key state is Unlocked"
					print(s)
					logfile.write(s)

				if is_auto_card and key_state:
					s = "Express Card : the Key will be Locked Automatically"
					print(s)
					logfile.write(s)

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

					tmp_date = today
					logfile.close()
					continue


				# if it is Normal Card or Key is Unlocked
				else:
					# check the card
					for line in normal_cards:
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

				normal_cards.close()




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
