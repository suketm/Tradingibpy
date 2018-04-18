

''' Only for historical data '''

''' Libraries '''
from datetime import timedelta, datetime

# External files
import variable


tm_mday = None
tm_mon = None
tm_year = None
tm_hour = None
tm_min = None
tm_sec = None

def make_list():

	temp_ls = []
	key = []
	for i in range(0,2*variable.memory+1):
		dd = timedelta(minutes = i)
		temp_time = (datetime.now() - dd).strftime('%Y%m%d %H:%M:%S')
		temp_time = temp_time[0:8]+' '+temp_time[8:len(temp_time)-2] + '00'
		temp_ls.append({temp_time:[]})
		key.append(temp_time)
	return temp_ls,key
