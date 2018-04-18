


''' ------------------- Main File ------------------- '''




''' Libraries '''

from time import localtime
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

#External files
import ib_live_data
import variable
import core

''' Connection '''

ib_live_data.get_live_data()


while variable.cont == '':

	variable.current_time = localtime()
	variable.current_time_minute = variable.current_time.tm_min

	if (variable.current_time_minute - variable.last_time == variable.time_gap or variable.current_time_minute - variable.last_time == variable.time_gap - 60) and variable.connection_status == 1:

		variable.last_time = variable.current_time_minute
		core.update_variables()

		if variable.current_pos != 0:
			core.exit_position()
			
		else:
			core.trade_signal()
			core.take_position()
		
		core.display()

	if variable.current_time_minute == 0 and variable.writeData == 1:
		core.write_files()


ib_live_data.terminate_live_data()
