import binascii
import nfc
import os, time, sys, datetime as dt

# User Python fuction
# from python_pkg.key_move import *
from keymodule.keyLock import *
from keymodule.sensor import *


filename_normal_cards = os.path.dirname(os.path.abspath(__file__)) + "/data/cards/normal.dat"
filename_auto_close_cards = os.path.dirname(os.path.abspath(__file__)) + "/data/cards/auto_close.dat"
filename_log_1 = os.path.dirname(os.path.abspath(__file__)) + "/data/key-1.log"
filename_log_2 = os.path.dirname(os.path.abspath(__file__)) + "/data/key-2.log"

def openLogFile(tmp_logfile_name, tmp_date):
	today = dt.date.today()
	if tmp_date == today:
		rt_logfile_name = tmp_logfile_name
		logfile = open(rt_logfile_name, mode='a')
	else:
		if tmp_logfile_name == filename_log_1:
			rt_logfile_name = filename_log_2
			logfile = open(rt_logfile_name, mode='w')
		else:
			rt_logfile_name = filename_log_1
			logfile = open(rt_logfile_name, mode='w')

	return logfile, rt_logfile_name

def closeLogFile(logfile):
	logfile.close()


def writeLog(s, logfile):
	now = dt.datetime.now()
	logfile.write(str(now) + ': ' + s + '\n')


def main():
	tmp_date = dt.date.today()
	tmp_logfile_name = filename_log_1
	key_state = True # lock position

	# os.system("sudo servod --p1pins=11")
	clf = nfc.ContactlessFrontend('usb')
	# 212F(FeliCa)
	target_req = nfc.clf.RemoteTarget("212F")
	# 0003(Suica)
	target_req.sensf_req = bytearray.fromhex("0000030000")

	lock()

	while True:
		try:

			target_res = clf.sense(target_req, iterations=10, interval=0.01)

			if target_res != None: # A Card is Touched

				card = binascii.hexlify(target_res.sensf_res) + '\n'
				is_normal_card = False
				is_auto_card = False
				normal_cards = open(filename_normal_cards, 'r')
				auto_close_cards = open(filename_auto_close_cards, 'r')

				logfile, tmp_logfile_name = openLogFile(tmp_logfile_name, tmp_date)

				for line in auto_close_cards:
					if card == line:
						is_auto_card = True

				# Auto Close Card or Normal Card
				if is_auto_card:
					s = "****** Auto Close Card ******"
					writeLog(s, logfile)
				else:
					s = "******   Normal Card   ******"
					writeLog(s, logfile)

				# Key is Locked or Unlocked
				if key_state:
					s = "Current key state is Locked"
					writeLog(s, logfile)
				else:
					s = "Current key state is Unlocked"
					writeLog(s, logfile)



				'''
					Auto Card and Locked
				'''
				if is_auto_card and key_state:
					s = "Auto Card: Lock Automatically"
					writeLog(s, logfile)

					unlock() # UNLOCK the Key

					s = "Unlocked the key"
					writeLog(s, logfile)


					# Waiting for Opening the Door
					s = "Open the door"
					writeLog(s, logfile)
					while isClosed():
						time.sleep(0.1)

					s = 'The door is opened. Close the door'
					writeLog(s, logfile)


					time.sleep(2)
					# Waiting for Closing the Door
					while not isClosed():
						time.sleep(0.1)

					time.sleep(1)

					lock() # LOCK the Key

					s = "Locked the key"
					writeLog(s, logfile)

					continue


				else:
					'''
						Normal Card or Key is Unlocked
					'''
					for line in normal_cards:
						# if the Card is Registered
						if card == line:
							s = "Successiful"
							writeLog(s, logfile)
							is_normal_card = True

							if key_state: # if Locked
								unlock()
								s = "Unlocked the key"
								writeLog(s, logfile)
								key_state = False

							else:	      # if Unlocked
								lock()
								s = "Locked the key"
								writeLog(s, logfile)
								key_state = True
							break


				'''
					Not Registered
				'''
				if not is_normal_card:
					s = "Wrong Card"
					writeLog(s, logfile)
					wrongCard(key_state)

				tmp_date = dt.date.today()
				closeLogFile(logfile)
				normal_cards.close()
				auto_close_cards.close()




		except KeyboardInterrupt:
			pass
			logfile, tmp_logfile_name = openLogFile(tmp_logfile_name, tmp_date)
			s = "exit: Keyboard Intterrupt"
			writeLog(s, logfile)
			closeLogFile(logfile)

			lock()
			# os.system("sudo killall servod")
			break


		except IOError as e:
			pass
			logfile, tmp_logfile_name = openLogFile(tmp_logfile_name, tmp_date)
			s ="exit: IO Error"
			writeLog(s, logfile)
			writeLog(str(e), logfile)
			closeLogFile(logfile)

			lock()
			# os.system("sudo killall servod")
			break

		time.sleep(0.1)

	clf.close()

if __name__ == '__main__':
	main()
