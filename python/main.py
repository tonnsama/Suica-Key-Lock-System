import binascii
import nfc
import os, time, sys, datetime as dt

# User Python fuction
from key_move import *
from sensor import *


OPEN_TIME = 3 # sec
CLOSE_TIME = 30 # sec
OPEN_DISTANCE = 7 # cm
CLOSE_DISTANCE = 4 # cm

filename_normal_cards = "/home/pi/key/data/normal_cards.dat"
filename_auto_close_cards = "/home/pi/key/data/auto_close_cards.dat"
filename_log_1 = "/home/pi/key/data/key-1.log"
filename_log_2 = "/home/pi/key/data/key-2.log"

def write_log(str, tmp_date, tmp_logfile):
	today = dt.date.today()
	now = dt.datetime.now()
	rt_filename = tmp_logfile

	if tmp_date == today:
		logfile = open(tmp_logfile, mode='a')

	else:
		if tmp_logfile == filename_log_1:
			rt_filename = filename_log_1
		else:
			rt_filename = filename_log_2

		logfile = open(rt_filename, mode='w')

	logfile.write(str(now) + str + '\n')
	logfile.close()

	return rt_filename



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

			target_res = clf.sense(target_req, iterations=10, interval=0.01)

			if target_res != None:

				# Open Log file
				today = dt.date.today()
				now = dt.datetime.now()

				if today == tmp_date:
					logfile = open(filename_log_1, mode="a")
					logfile.write(str(now) + "\n")
				else:
					logfile = open(filename_log_1, mode="w")
					logfile.write(str(now) + "\n")


				card = binascii.hexlify(target_res.sensf_res) + '\n'
				auth = False
				is_auto_card = False
				normal_cards = open(filename_normal_cards, 'r')
				auto_close_cards = open(filename_auto_close_cards, 'r')
				tmp_date = today

				for line in auto_close_cards:
					if card == line:
						is_auto_card = True

				# if it is an Auto Close Card and Key is Locked
				if is_auto_card:
					s = "Auto Close Card\n"
					print(s)
					logfile.write(s)

				if key_state:
					s = "Current key state is Locked\n"
					print(s)
					logfile.write(s)
				else:
					s = "Current key state is Unlocked\n"
					print(s)
					logfile.write(s)

				if is_auto_card and key_state:
					s = "Express Card : the Key will be Locked Automatically\n"
					print(s)
					logfile.write(s)

					unlock()
					s = "Unlocked the key\n"
					print(s)
					logfile.write(s)

					start_time = time.time()
					# Waiting for Opening the Door
					s = "Open the door\n"
					print(s)
					logfile.write(s)

					time.sleep(2)
					while True:
						distance = measure()
						elapsed_time = time.time() - start_time
					#	print(distance)
						if distance > OPEN_DISTANCE or elapsed_time > OPEN_TIME:
							s = "distance = " + str(distance) + "\nelapsed time = " + str(elapsed_time) + "\n"
							logfile.write(s)
							break
						time.sleep(0.1)


					s = "Close the door\n"
					print(s)
					logfile.write(s)

					time.sleep(2)
					# Waiting for Closing the Door
					while True:
						distance = measure()
						elapsed_time = time.time() - start_time
					#	print(distance)
						if distance < CLOSE_DISTANCE or elapsed_time > CLOSE_TIME:
							time.sleep(1)
							lock()
							s = "Locked the key\n"
							print(s)
							logfile.write(s)
							# logfile.write(distance)
							s = "distance = " + str(distance) + "\nelapsed time = " + str(elapsed_time) + "\n"
							logfile.write(s)
							break

						time.sleep(0.1)


					logfile.close()
					continue


				# if it is Normal Card or Key is Unlocked
				else:
					# check the card
					for line in normal_cards:
						# if the Card is Registered
						if card == line:
							s = "Successiful\n"
							print(s)
							logfile.write(s)
							auth = True
							if key_state: # if Locked
								unlock()
								s = "Unlocked the key\n"
								print(s)
								logfile.write(s)
								key_state = False
							else:	      # if Unlocked
								lock()
								s = "Locked the key\n"
								print(s)
								logfile.write(s)
								key_state = True
							break

				# if the card is WRONG
				if not auth:
					s = "Wrong Card\n"
					print(s)
					logfile.write(s)
					wrongCard(key_state)

				normal_cards.close()




		except KeyboardInterrupt:
			pass
			s = "exit: Keyboard Intterrupt\n"
			print(s)
			logfile.write(s)

			lock()
			os.system("sudo killall servod")
			break


		except IOError:
			pass
			s ="exit: IO Error\n"
			print(s)
			logfile.write(s)

			lock()
			os.system("sudo killall servod")
			break

		time.sleep(0.05)

	clf.close()

if __name__ == '__main__':
	main()
