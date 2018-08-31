
''' Strategy 1: Mean Reversion Eur/Gbp	'''

''' Libraries '''
from ib.opt.connection import Connection
from ib.ext.Contract import Contract
from ib.ext.Order import Order
from datetime import timedelta, datetime
from time import localtime, strftime, sleep
import numpy as np
import pandas as pd
from sklearn import svm

# External files
import ib_live_data as ib
import variable as v

''' strategy starts '''

class Strategy1(object):

	''' variables '''
	
	#Quant Parameters
	memory = 30
	histN = 60		# length of historical data
	Z_const = 1.5
	Z_rebound = 0.05
	gap_mean_vol_const = 0.00006
	quantity = 2000000

	#live variables
	current_eur_usd_ask = None
	current_eur_usd_bid = None
	current_gbp_usd_ask = None
	current_gbp_usd_bid = None
	current_eur_gbp_ask = None
	current_eur_gbp_bid = None
	current_gbp_usd_exch = 1.4

	#strategy variables
	tradeStatus = 0
	price = None
	commission = None
	commCurr = None
	gap_mean_vol = 0
	unrlzdPnL = None
	writeData = 1
		
	#data
	ls_strategy = []
	enter_details = {}
	exit_details = {}
	ls_date = []
	ls_time = []
	ls_vol = []
	ls_eur_usd_ask = []
	ls_eur_usd_bid = []
	ls_gbp_usd_ask = []
	ls_gbp_usd_bid = []
	ls_eur_gbp_ask = []
	ls_eur_gbp_bid = []
	ls_eur_usd_mid = []
	ls_gbp_usd_mid = []
	ls_gap =[]
	ls_gap_Z = []
	ls_gap_mean = []
	ls_gap_vol = []
	

	#interactive brokers (contract and ticker Id for each contract)
	tickerId_EUR_GBP = 873
	tickerId_EUR_USD = 874
	tickerId_GBP_USD = 875
	contract1 = None
	contract2 = None
	contract3 = None
	
	def __init__(self):

		# create contracts, update historical data & set them with current variables, and request live market data

		self.contract1 = ib.make_contract(sym = 'EUR', sec_Type = 'CASH', exchange = 'IDEALPRO', currency = 'GBP')
		self.contract2 = ib.make_contract(sym = 'EUR', sec_Type = 'CASH', exchange = 'IDEALPRO', currency = 'USD')
		self.contract3 = ib.make_contract(sym = 'GBP', sec_Type = 'CASH', exchange = 'IDEALPRO', currency = 'USD')

		# process: make a dictionary of list, keys = date; format of date is same as dates coming from historical data; time must be more 15 secs
		while 1 > 0:
			if localtime().tm_sec < 30 and localtime().tm_sec > 20:
				temp_ls = {}
				keys = []
				for i in range(59,-1,-1):
					dd = timedelta(minutes = i)
					temp_time = (datetime.now() - dd).strftime('%Y%m%d %H:%M:%S')
					temp_time = temp_time[0:8]+' '+temp_time[8:len(temp_time)-2] + '00'
					temp_ls[temp_time] = []
					keys.append(temp_time)
				endTime = strftime('%Y%m%d %H:%M:%S')
				temp_ls = ib.get_hist_data(tickerID = self.tickerId_EUR_GBP, contract = self.contract1, end = endTime, dur = '1 D', tick_size = '1 min', temp_list = temp_ls, temp_key = keys)
				temp_ls = ib.get_hist_data(tickerID = self.tickerId_EUR_USD, contract = self.contract2, end = endTime, dur = '1 D', tick_size = '1 min', temp_list = temp_ls, temp_key = keys)
				temp_ls = ib.get_hist_data(tickerID = self.tickerId_GBP_USD, contract = self.contract3, end = endTime, dur = '1 D', tick_size = '1 min', temp_list = temp_ls, temp_key = keys)
				for k in keys:
					v.current_time = k
					self.current_eur_usd_ask = temp_ls[k][2]
					self.current_eur_usd_bid = temp_ls[k][3]
					self.current_gbp_usd_ask = temp_ls[k][4]
					self.current_gbp_usd_bid = temp_ls[k][5]
					self.current_eur_gbp_ask = temp_ls[k][0]
					self.current_eur_gbp_bid = temp_ls[k][1]
					self.update_variables()
				v.last_time_min = localtime().tm_min
				break

		v.connection.reqMarketDataType(marketDataType = 1)
		v.connection.reqMktData(tickerId = self.tickerId_EUR_GBP, contract = self.contract1, genericTickList = "", snapshot = False)
		v.connection.reqMktData(tickerId = self.tickerId_EUR_USD, contract = self.contract2, genericTickList = "", snapshot = False)
		v.connection.reqMktData(tickerId = self.tickerId_GBP_USD, contract = self.contract3, genericTickList = "", snapshot = False)
		sleep(1)


	def update_live_variables(self):
		temp_data = v.data.copy()
		if temp_data['tickID'] == self.tickerId_EUR_GBP and temp_data['field'] == 2:
			self.current_eur_gbp_ask = temp_data['price']
		elif temp_data['tickID'] == self.tickerId_EUR_GBP and temp_data['field'] == 1:
			self.current_eur_gbp_bid = temp_data['price']
		elif temp_data['tickID'] == self.tickerId_EUR_USD and temp_data['field'] == 2:
			self.current_eur_usd_ask = temp_data['price']
		elif temp_data['tickID'] == self.tickerId_EUR_USD and temp_data['field'] == 1:
			self.current_eur_usd_bid = temp_data['price']
		elif temp_data['tickID'] == self.tickerId_GBP_USD and temp_data['field'] == 2:
			self.current_gbp_usd_ask = temp_data['price']
		elif temp_data['tickID'] == self.tickerId_GBP_USD and temp_data['field'] == 1:
			self.current_gbp_usd_bid = temp_data['price']

		if 'GBP' in list(v.exchRate.keys()):
			current_gbp_usd_exch = v.exchRate['GBP']


	def update_variables(self):

		current_eur_usd_mid = float(self.current_eur_usd_ask + self.current_eur_usd_bid)/2
		current_gbp_usd_mid = float(self.current_gbp_usd_ask + self.current_gbp_usd_bid)/2
		current_gap = current_gbp_usd_mid - current_eur_usd_mid

		if type(v.current_time) == str:
			self.ls_date.append(v.current_time[0:9])
			self.ls_time.append(v.current_time[10:len(v.current_time)])
		else:
			temp_date = str(v.current_time.tm_year)
			temp_time = ''
			for temp_info in [v.current_time.tm_mon,v.current_time.tm_mday]:
				if len(str(temp_info)) == 1:
					temp_date += '0'+str(temp_info)
				else:
					temp_date += str(temp_info)
			for temp_info in [v.current_time.tm_hour, v.current_time.tm_min, v.current_time.tm_sec]:
				if len(str(temp_info)) == 1:
					temp_time += '0'+str(temp_info)+':'
				else:
					temp_time += str(temp_info)+':'
			self.ls_date.append(temp_date)
			self.ls_time.append(temp_time[0:8])
		
		self.ls_eur_usd_ask.append(self.current_eur_usd_ask)
		self.ls_eur_usd_bid.append(self.current_eur_usd_bid)
		self.ls_gbp_usd_ask.append(self.current_gbp_usd_ask)
		self.ls_gbp_usd_bid.append(self.current_gbp_usd_bid)
		self.ls_eur_gbp_ask.append(self.current_eur_gbp_ask)
		self.ls_eur_gbp_bid.append(self.current_eur_gbp_bid)
		self.ls_eur_usd_mid.append(current_eur_usd_mid)
		self.ls_gbp_usd_mid.append(current_gbp_usd_mid)
		self.ls_gap.append(current_gap)

		self.n = len(self.ls_date)

		gap_Z = 0.0
		gap_mean = 0.0
		gap_vol  = 0.0
		vol_eur_gbp = 0.0

		if self.n == self.memory:
			gap_mean = np.mean(self.ls_gap[0:self.n])
			gap_vol = np.std(self.ls_gap[0:self.n])
			gap_Z = float(self.ls_gap[self.n-1] - gap_mean)/gap_vol

		elif self.n > self.memory:
			
			gap_mean = ( self.ls_gap[self.n-1] + (self.memory-1)*self.ls_gap_mean[self.n-1-1] ) / self.memory
			gap_vol = ( ((self.ls_gap[self.n-1]-gap_mean)**2 + (self.memory-1)*self.ls_gap_vol[self.n-1-1]**2 )/self.memory)**0.5
			gap_Z = float(self.ls_gap[self.n-1] - gap_mean)/gap_vol

			vol_eur_gbp = np.std( [ (self.ls_eur_gbp_ask[i]+self.ls_eur_gbp_bid[i])/2 for i in range(self.n-self.memory,self.n) ] )
			
		self.ls_gap_mean.append(gap_mean)
		self.ls_gap_vol.append(gap_vol)
		self.ls_gap_Z.append(gap_Z)
		self.ls_vol.append(vol_eur_gbp)


	def take_position(self):
		if self.tradeStatus == 0 and self.n > self.histN:
			if self.ls_gap_Z[self.n-1] > self.Z_const:			# Gap is GBP-EUR
				self.tradeStatus = +1
				ib.place_order(action = 'BUY', qty = self.quantity, contract = self.contract1)
				sleep(1)
				self.get_prices()
				self.update_enter_details()
			elif self.ls_gap_Z[self.n-1] < -1*self.Z_const:
				self.tradeStatus = -1
				ib.place_order(action = 'SELL', qty = self.quantity, contract = self.contract1)
				sleep(1)
				self.get_prices()
				self.update_enter_details()


	def exit_position(self):
		
		if self.tradeStatus == 1 and self.n > self.enter_details['nIn']:
			self.unrlzdPnL = round((self.current_eur_gbp_ask - self.enter_details['priceIn'])*self.quantity - 2*self.enter_details['commIn']/self.current_gbp_usd_exch)
			self.gap_mean_vol = np.std(self.ls_gap_mean[ self.enter_details['nIn'] - 1: self.n ])/(self.n - self.enter_details['nIn'])**0.5
			if (self.gap_mean_vol > self.gap_mean_vol_const) or (self.ls_gap_Z[self.n - 1] < -1* self.Z_rebound and self.ls_gap[self.n - 1] < self.ls_gap[self.enter_details['nIn']]):
				ib.place_order(action = 'SELL', qty = self.quantity, contract = self.contract1)
				sleep(1)
				self.get_prices()
				self.update_exit_details()

		elif self.tradeStatus == -1 and self.n > self.enter_details['nIn']:
			self.unrlzdPnL = round((self.enter_details['priceIn'] - self.current_eur_gbp_ask)*self.quantity - 2*self.enter_details['commIn']/self.current_gbp_usd_exch)
			self.gap_mean_vol = np.std(self.ls_gap_mean[ self.enter_details['nIn'] - 1: self.n ])/(self.n - self.enter_details['nIn'])**0.5
			if (self.gap_mean_vol > self.gap_mean_vol_const) or (self.ls_gap_Z[self.n - 1] > 1* self.Z_rebound and self.ls_gap[self.n - 1] > self.ls_gap[self.enter_details['nIn']]):
				ib.place_order(action = 'BUY', qty = self.quantity, contract = self.contract1)
				sleep(1)
				self.get_prices()
				self.update_exit_details()


	def get_prices(self):
		condition1 = 0
		condition2 = 0
		while condition1 == 0 or condition2 == 0:
			if len(v.execution) > 0:
				if v.execution[len(v.execution)-1]['orderID'] == v.orderID:
					condition1 = 1
				if len(v.commission) == len(v.execution):
					condition2 = 1
				if condition1 == 1 and condition2 == 1:
					sleep(1)	# to get prices after sending the order, there can be delay in an event of low liquidity
		self.price = 0
		self.commission = 0
		self.commCurr = ''
		q = 0
		for i in range(len(v.execution)):
			if v.execution[i]['orderID'] == v.orderID:
				self.price += v.execution[i]['price']*v.execution[i]['qty']
				q += v.execution[i]['qty']
				self.commission += v.commission[i]['commisison']
				self.commCurr = v.commission[i]['comm. cny']
		if q != self.quantity:
			self.get_prices()
		else:
			self.price = float(self.price)/q


	def update_enter_details(self):
		self.enter_details['Type']  = self.tradeStatus
		self.enter_details['nIn']  = self.n
		self.enter_details['DateIn']  = self.ls_date[self.n-1]
		self.enter_details['TimeIn']  = self.ls_time[self.n-1]
		self.enter_details['Gap_Z_In']  = self.ls_gap_Z[self.n-1]
		self.enter_details['priceIn'] = self.price
		self.enter_details['priceCurrIn'] = 'GBP'
		self.enter_details['commIn'] = self.commission
		self.enter_details['commCurrIn'] = self.commCurr
		self.enter_details['slipIn'] = round((self.price - float([ self.ls_eur_gbp_bid[self.n-1] if self.tradeStatus == 1 else self.ls_eur_gbp_ask[self.n-1]][0]))*self.quantity)


	def update_exit_details(self):
		self.exit_details['nOut'] = self.n
		self.exit_details['DateOut'] = self.ls_date[self.n-1]
		self.exit_details['TimeOut'] = self.ls_time[self.n-1]
		self.exit_details['priceOut'] = self.price
		self.exit_details['commOut'] = self.commission
		self.enter_details['commCurrOut'] = self.commCurr
		self.exit_details['slipOut'] = round((self.price - float([ self.ls_eur_gbp_ask[self.n-1] if self.tradeStatus == 1 else self.ls_eur_gbp_bid[self.n-1]][0]))*self.quantity)
		self.exit_details['Gap_Z_Out']  = self.ls_gap_Z[self.n-1]
		self.exit_details['Gap_mean_vol'] = self.gap_mean_vol
		self.exit_details['Time Diff'] = self.exit_details['nOut'] - self.enter_details['nIn']
		self.exit_details['PnL'] = (self.tradeStatus*( self.exit_details['priceOut'] - self.enter_details['priceIn']))*self.quantity
		self.exit_details['DD'] = float([(self.enter_details['priceIn'] - min(self.ls_eur_gbp_ask[self.enter_details['nIn']:self.n]))*100/self.enter_details['priceIn'] if self.tradeStatus == 1 else \
		(max(self.ls_eur_gbp_ask[self.enter_details['nIn']:self.n]) - self.enter_details['priceIn'])*100/self.enter_details['priceIn'] ][0])

		self.tradeStatus = 0
		temp_dict = {}
		temp_dict.update(self.enter_details)
		temp_dict.update(self.exit_details)
		self.ls_strategy.append(temp_dict)


	def display(self):
		
		print ("\n\n")
		print ('\tN: ',self.n,'\tTime: ',self.ls_time[self.n-1],'\tCurrent Pos.: ',self.tradeStatus,'\tCurr Gap Z: ',round(self.ls_gap_Z[self.n-1],2),'\tCurr Eur/Gbp vol.(*10^-6): ',round(self.ls_vol[self.n-1]*1000000))
		
		if len(self.ls_strategy) > 0:
			pnl = round(sum([s['PnL'] for s in self.ls_strategy]))
			comm = round(sum([ c['commisison'] for c in v.commission]))
			maxDD = round(max([ s['DD'] for s in self.ls_strategy]),2)
			s = self.ls_strategy
			n = len(self.ls_strategy)-1
			x = len([s for s in self.ls_strategy if s['PnL'] > 0])
			y = n+1-x
		
			print ('\tPnL (GBP): ',pnl,'\tTotal Commission (',v.commission[len(v.commission)-1]['comm. cny'],'): ',comm,'\tMax DD: ',maxDD,'\tInitial Total Cash: ',v.initialTotalCash)
			print ('\tLast Trade PnL:',round(s[n]['PnL']),'\tSlip In: ',s[n]['slipIn'],'\tSlip Out: ',s[n]['slipOut'],'\t\tCurrent Total Cash: ',v.currentTotalCash)
			print ('\tTotal Trades: ',n+1,'\tTotal Pos. trades: ',x,'\tTotal Neg. trades: ',y)
		
		if self.tradeStatus != 0:
			print ('\tTime In: ',self.enter_details['TimeIn'],'\tUnrlzd. PnL: ',self.unrlzdPnL,'\tSlipg.In: ',self.enter_details['slipIn'],'\tEnt. Price: ',self.enter_details['priceIn'])
			print ('\tGap mean: ',round(self.ls_gap_mean[self.n-1],5),'\tvol.(*10^-6): ',round(self.ls_gap_vol[self.n-1]*1000000),'\tmean vol(*10^-4): ',round(self.gap_mean_vol*10000,2),'\tEnt. Z: ',round(self.enter_details['Gap_Z_In'],2))
		
		self.writeData = 1


	def write_files(self):
		data = []
		err_msg = []
	
		for i in range(self.n):
			temp = {}
			temp['Date'] = self.ls_date[i]
			temp['Time'] = self.ls_time[i]
			temp['Eur_Usd_Ask'] = self.ls_eur_usd_ask[i]
			temp['Eur_Usd_Bid'] = self.ls_eur_usd_bid[i]
			temp['Gbp_Usd_Ask'] = self.ls_gbp_usd_ask[i]
			temp['Gbp_Usd_Bid'] = self.ls_gbp_usd_bid[i]
			temp['Eur_Gbp_Ask'] = self.ls_eur_gbp_ask[i]
			temp['Eur_Gbp_Bid'] = self.ls_eur_gbp_bid[i]
			temp['Eur_Usd_mid'] = self.ls_eur_usd_mid[i]
			temp['Gbp_Usd_mid'] = self.ls_gbp_usd_mid[i]
			temp['gap'] = self.ls_gap[i]
			temp['gap_mean'] = self.ls_gap_mean[i]
			temp['gap_vol'] = self.ls_gap_vol[i]
			temp['gap_Z'] = self.ls_gap_Z[i]
			data.append(temp)

		for error in v.err_msg:
			temp = {}
			temp['time'] = str(error[0].tm_year)+'/'+str(error[0].tm_mon)+'/'+str(error[0].tm_mday)+'  '+str(error[0].tm_hour)+':'+str(error[0].tm_min)+':'+str(error[0].tm_sec)
			temp['errorCode'] = error[1].errorCode
			temp['errorMsg'] = error[1].errorMsg
			err_msg.append(temp)

		df1 = pd.DataFrame(self.ls_strategy)
		df2 = pd.DataFrame(data)
		df3 = pd.DataFrame(err_msg)

		temp_month = str(v.start_time.tm_mon)
		temp_date = str(v.start_time.tm_mday)
		temp_hour = str(v.start_time.tm_hour)
		if len(temp_month) == 1:
			temp_month = '0'+temp_month
		if len(temp_date) == 1:
			temp_date = '0'+temp_date
		if len(temp_hour) == 1:
			temp_hour = '0'+temp_hour
		timestamp = str(v.start_time.tm_year)+temp_month+temp_date+'_'+temp_hour
		
		df1.to_csv(timestamp+'strat.csv')
		df2.to_csv(timestamp+'data.csv')
		df3.to_csv(timestamp+'ERROR.csv')

		self.writeData = 0
