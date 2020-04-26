import binascii
import nfc
import os, time, sys, datetime as dt

# User Python fuction
from python_pkg.key_move import *
from python_pkg.sensor import *


filename_normal_cards = "/home/pi/key/data/normal_cards.dat"
filename_auto_close_cards = "/home/pi/key/data/auto_close_cards.dat"
filename_log_1 = "/home/pi/key/data/key-1.log"
filename_log_2 = "/home/pi/key/data/key-2.log"


def write_log(s, tmp_date, tmp_logfile):
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

	logfile.write(str(now) + ': ' + s + '\n')
	logfile.close()

	return rt_filename


def main():

	os.system("sudo servod --p1pins=11")
	clf = nfc.ContactlessFrontend('usb')
	# 212F(FeliCa)
	target_req = nfc.clf.RemoteTarget("212F")
	# 0003(Suica)
	target_req.sensf_req = bytearray.fromhex("0000030000")


	# tmp_date = dt.date.today()
	key_state = True # lock position
	tmp_logfile = filename_log_1



	while True:
		try:

			target_res = clf.sense(target_req, iterations=10, interval=0.01)
			tmp_date = dt.date.today()

			if target_res != None:

				card = binascii.hexlify(target_res.sensf_res) + '\n'
				is_normal_card = False
				is_auto_card = False
				normal_cards = open(filename_normal_cards, 'r')
				auto_close_cards = open(filename_auto_close_cards, 'r')

				for line in auto_close_cards:
					if card == line:
						is_auto_card = True

				# Auto Close Card or Normal Card
				if is_auto_card:
					s = "****** Auto Close Card ******"
					tmp_logfile = write_log(s, tmp_date, tmp_logfile)
				else:
					s = "****** Normal Card ******"
					tmp_logfile = write_log(s, tmp_date, tmp_logfile)

				# Key is Locked or Unlocked
				if key_state:
					s = "Current key state is Locked"
					tmp_logfile = write_log(s, tmp_date, tmp_logfile)
				else:
					s = "Current key state is Unlocked"
					tmp_logfile = write_log(s, tmp_date, tmp_logfile)



				'''
					Auto Card and Locked
				'''
				if is_auto_card and key_state:
					s = "Auto Card: Lock Automatically"
					tmp_logfile = write_log(s, tmp_date, tmp_logfile)

					unlock() # UNLOCK the Key

					s = "Unlocked the key"
					tmp_logfile = write_log(s, tmp_date, tmp_logfile)


					# Waiting for Opening the Door
					s = "Open the door"
					tmp_logfile = write_log(s, tmp_date, tmp_logfile)
					while is_closed():
						time.sleep(0.1)

					s = 'The door is opened. Close the door'
					tmp_logfile = write_log(s, tmp_date, tmp_logfile)


					time.sleep(2)
					# Waiting for Closing the Door
					while not is_closed():
						time.sleep(0.1)

					time.sleep(1)

					lock() # LOCK the Key

					s = "Locked the key"
					tmp_logfile = write_log(s, tmp_date, tmp_logfile)

					continue


				else:
					'''
						Normal Card or Key is Unlocked
					'''
					for line in normal_cards:
						# if the Card is Registered
						if card == line:
							s = "Successiful"
							tmp_logfile = write_log(s, tmp_date, tmp_logfile)
							is_normal_card = True

							if key_state: # if Locked
								unlock()
								s = "Unlocked the key"
								tmp_logfile = write_log(s, tmp_date, tmp_logfile)
								key_state = False

							else:	      # if Unlocked
								lock()
								s = "Locked the key"
								tmp_logfile = write_log(s, tmp_date, tmp_logfile)
								key_state = True
							break


				'''
					Not Registered
				'''
				if not is_normal_card:
					s = "Wrong Card"
					tmp_logfile = write_log(s, tmp_date, tmp_logfile)
					wrongCard(key_state)

				normal_cards.close()
				auto_close_cards.close()




		except KeyboardInterrupt:
			pass
			s = "exit: Keyboard Intterrupt"
			tmp_logfile = write_log(s, tmp_date, tmp_logfile)

			lock()
			os.system("sudo killall servod")
			break


		except IOError:
			pass
			s ="exit: IO Error"
			tmp_logfile = write_log(s, tmp_date, tmp_logfile)

			lock()
			os.system("sudo killall servod")
			break

		time.sleep(0.1)

	clf.close()

if __name__ == '__main__':
	main()
