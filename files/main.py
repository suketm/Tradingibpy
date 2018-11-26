

''' ------------------- Main File ------------------- '''




''' Libraries '''

from datetime import datetime
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

#External files
import ib_live_data as ib
from strategy import Strategy

''' Connection '''

ib.establish_connection()
s = Strategy()


cont = ''

try:
	while cont == '':

		ib.current_time = datetime.now()

		if ib.connection_status == 1:

			if ib.current_time.minute != ib.last_time.minute:

				ib.last_time = ib.current_time

				s.update_live_variables()
				s.exit()
				s.enter()
				s.display()

				if ib.last_time.minute == 0:
					s.write_files()


except KeyboardInterrupt:
	s.write_files()

ib.terminate_connection()