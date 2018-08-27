

''' ------------------- Main File ------------------- '''




''' Libraries '''

from time import localtime
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

#External files
import ib_live_data as ib
import variable as v
from strategy1 import Strategy1

''' Connection '''

ib.establish_connection()
s1 = Strategy1()
#s2 = 

while v.cont == '':

	v.current_time = localtime()


	# update live variables + trade (In/Exit)
	s1.update_live_variables()
	s1.exit_position()
	s1.take_position()


	if v.connection_status == 1 and v.last_time_min !=  v.current_time.tm_min:

		v.last_time_min =  v.current_time.tm_min

		# update variables
		s1.update_variables()

		# display
		s1.display()

	if s1.writeData == 1 and v.current_time.tm_min == 0:
		s1.write_files()


ib.terminate_connection()