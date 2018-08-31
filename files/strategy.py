
''' Strategy 

	DESCRIPTION

				'''

''' Libraries '''
from ib.opt.connection import Connection
from ib.ext.Contract import Contract
from ib.ext.Order import Order
from datetime import timedelta, datetime
from time import localtime, strftime

# External files
import ib_live_data as ib
import variable as v

''' strategy starts '''

class Strategy(object):

	''' variables '''
	#Quant Parameters
	#live variables
	#strategy variables
	#data
	#interactive brokers (contract and ticker Id for each contract)

	def __init__():
		# create contracts, update historical data & set them with current variables, and request live market data
		# process: make a dictionary of list, keys = date; format of date is same as dates coming from historical data; time must be more 18 secs; time interval...
		# ...should not be very large, otherwise for next strategy it will get less time.
		sleep(1) # for properly establish connection



	def update_live_variables():
	
	def update_variables():

	def take_position():

		sleep(1) # for proper execution of order

	def exit_position():

		sleep(1) # for proper execution of order

	def get_prices():

		sleep(1) # to get prices after sending the order, there can be delay in some events.

	def update_enter_details():


	def update_exit_details():


	def display():
		# always print volatiltiy of asset. It will give you rough idea about my tp. My tp should be around vol - spread - commission


	def write_files():
