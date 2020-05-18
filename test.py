import datetime as dt

filename_log_1 = "/home/pi/key/data/test-1.log"
filename_log_2 = "/home/pi/key/data/test-2.log"


def writeLog(s, tmp_date, tmp_logfile):
	today = dt.date.today()
	now = dt.datetime.now()
	rt_filename = tmp_logfile

	if tmp_date == today:
		logfile = open(tmp_logfile, mode='a')

	else:
		if tmp_logfile == filename_log_1:
			rt_filename = filename_log_2
		else:
			rt_filename = filename_log_1

		logfile = open(rt_filename, mode='w')

	logfile.write(str(now) + ': ' + s + '\n')
	logfile.close()

	return rt_filename


if __name__ == '__main__':
	tmp_date = dt.date.today() - dt.timedelta(days=1)
	tmp_logfile = filename_log_1
	s = "******   Normal Card   ******"
	tmp_logfile = writeLog(s, tmp_date, tmp_logfile)
	tmp_logfile = writeLog(s, tmp_date, tmp_logfile)
	tmp_logfile = writeLog(s, tmp_date, tmp_logfile)
	tmp_logfile = writeLog(s, tmp_date, tmp_logfile)

	print(tmp_logfile)
