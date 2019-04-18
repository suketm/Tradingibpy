
''' Strategy 

	DESCRIPTION

				'''

''' Libraries '''
from ib.opt.connection import Connection
from ib.ext.Contract import Contract
from ib.ext.Order import Order
from datetime import datetime
from time import sleep, strftime
import numpy as np
import pandas as pd

# External files
import ib_live_data as ib


''' strategy starts '''

class Strategy(object):

	''' variables '''
	#Quant Parameters
	currency1 = 'AUD'
	currency2 = 'NZD'
	clientID = 
	pip_size = 
	memory = 
	

	quantity = 100000

	''' For same strategy, below code should remian same '''

	#live variables
	n = 0
	current_time = None
	ask = None
	bid = None
	price1_ask = None
	price1_bid = None
	price2_ask = None
	price2_bid = None
	
	#strategy variables
	current_pos = 0
	current_pos_type = None
	gap_mean_vol = None
	tp = 0
	sl = 0
	exit_type = None
	total_pnl = 0
	total_commission = 0
	last_exec = None
	avg_exec = None
	enter_details = []
	exit_details = []
	strategy = []


	#data
	hist_time_start = 25
	hist_time_end = 30
	hist_data = {}

	ls_time = []
	ls_ask = []
	ls_bid = []
	ls_price1_ask = []
	ls_price1_bid = []
	ls_price2_ask = []
	ls_price2_bid = []

	#indicators
	ls_spread = []
	ls_price = []
	ls_price_Z = []
	ls_price_mean = []
	ls_price_vol = []
	ls_gap =[]
	ls_gap_Z = []
	ls_gap_mean = []
	ls_gap_vol = []

	#interactive brokers (contract and ticker Id for each contract)
	ticker_ls = {,}

	tickerId_price = ticker_ls[currency1+'_'+currency2]
	tickerId_price1 = ticker_ls[currency1+'_'+currencyBase]
	tickerId_price2 = ticker_ls[currency2+'_'+currencyBase]
	contract = None
	contract1 = None
	contract2 = None
	err_msg = []
	exec_msg = []
	comm_msg = []
	live_data = {tickerId_price: {1: None, 2: None}, tickerId_price1: {1: None, 2: None}, tickerId_price2: {1: None, 2: None}}


	def __init__(self):

		# create contracts, update historical data & set them with current variables, and request live market data
		self.contract = ib.make_contract(sym = self.currency1, sec_Type = 'CASH', exchange = 'IDEALPRO', currency = self.currency2)
		self.contract1 = ib.make_contract(sym = self.currency1, sec_Type = 'CASH', exchange = 'IDEALPRO', currency = self.currencyBase)
		self.contract2 = ib.make_contract(sym = self.currency2, sec_Type = 'CASH', exchange = 'IDEALPRO', currency = self.currencyBase)

		while self.n == 0:

			if self.hist_time_end > datetime.now().time().second > self.hist_time_start:
				endTime = strftime('%Y%m%d %H:%M:%S')
				ib.get_hist_data(tickerID = self.tickerId_price, contract = self.contract, end = endTime, dur = '1 D', tick_size = '1 min')
				ib.get_hist_data(tickerID = self.tickerId_price1, contract = self.contract1, end = endTime, dur = '1 D', tick_size = '1 min')
				ib.get_hist_data(tickerID = self.tickerId_price2, contract = self.contract2, end = endTime, dur = '1 D', tick_size = '1 min')

				temp_keys = list(self.hist_data.keys())
				for time in temp_keys[-6*self.memory-1:]:

					self.current_time = time
					self.ask = self.hist_data[time][self.tickerId_price][0]
					self.bid = self.hist_data[time][self.tickerId_price][1]
					self.price1_ask = self.hist_data[time][self.tickerId_price1][0]
					self.price1_bid = self.hist_data[time][self.tickerId_price1][1]
					self.price2_ask = self.hist_data[time][self.tickerId_price2][0]
					self.price2_bid = self.hist_data[time][self.tickerId_price2][1]
					self.update_variables()
				ib.last_time = datetime.now()

		ib.get_live_data(tickerId = self.tickerId_price, contract = self.contract)
		ib.get_live_data(tickerId = self.tickerId_price1, contract = self.contract1)
		ib.get_live_data(tickerId = self.tickerId_price2, contract = self.contract2)
		sleep(3)


	def update_live_variables(self):

		self.current_time = ib.current_time

		self.ask = self.live_data[self.tickerId_price][2]
		self.bid = self.live_data[self.tickerId_price][1]
		self.price1_ask = self.live_data[self.tickerId_price1][2]
		self.price1_bid = self.live_data[self.tickerId_price1][1]
		self.price2_ask = self.live_data[self.tickerId_price2][2]
		self.price2_bid = self.live_data[self.tickerId_price2][1]

		self.update_variables()


	def update_variables(self):

		self.ls_time.append(self.current_time)
		self.n = len(self.ls_time)

		self.ls_ask.append(self.ask)
		self.ls_bid.append(self.bid)
		self.ls_price1_ask.append(self.price1_ask)
		self.ls_price1_bid.append(self.price1_bid)
		self.ls_price2_ask.append(self.price2_ask)
		self.ls_price2_bid.append(self.price2_bid)

		price1_mid = float(self.price1_ask + self.price1_bid)/2
		price2_mid = float(self.price2_ask + self.price2_bid)/2
		gap = price2_mid - price1_mid

		self.ls_gap.append(gap)
		self.ls_price.append((self.ask+self.bid)/2)
		self.ls_spread.append(self.ask-self.bid)

		gap_Z = 0.0
		gap_mean = 0.0
		gap_vol  = 0.0

		price_Z = 0.0
		price_mean = 0.0
		price_vol = 0.0
		price_vol_Z = 0.0

		if self.n == self.memory:

			
			
		elif self.n > self.memory:

			
		


	
	def display(self):

		if self.ls_gap_Z[-1] >= 0:
			vol_up = round((1 - self.ls_gap_Z[-1]/ self.vol_slope)* self.vol_up* 10**self.pip_size,2)
		elif self.ls_gap_Z[-1] < 0:
			vol_up = round((1 + self.ls_gap_Z[-1]/ self.vol_slope)* self.vol_up* 10**self.pip_size,2)

		print ('\n')
		print ('\tN:', self.n, '\tTime:',self.current_time.time().strftime("%H:%M:%S"),'\tCurrent Pos.:',self.current_pos,\
			'\tPrice Vol (*10^',self.pip_size,'):',round(self.ls_price_vol[-1]*10**self.pip_size,2),'\tVol Range(',round(self.ls_gap_Z[-1],2),'):',self.vol_low*10**self.pip_size,'-',vol_up)		
		print('\tTotal PnL (',self.currency2,'):',round(self.total_pnl,2),'\tTotal Comm. (USD):',round(self.total_commission,2),'\tTP:SL::',self.tp,':',self.sl,'\tTotal Trades:',len(self.strategy))
		print('\t',self.currency1,'.',self.currency2,'ask:',self.ls_ask[-1],'\t',self.currency1,'.',self.currencyBase,'ask:',self.ls_price1_ask[-1],'\t',self.currency2,'.',self.currencyBase,'ask:',self.ls_price2_ask[-1])
		print('\t',self.currency1,'.',self.currency2,'bid:',self.ls_bid[-1],'\t',self.currency1,'.',self.currencyBase,'bid:',self.ls_price1_bid[-1],'\t',self.currency2,'.',self.currencyBase,'bid:',self.ls_price2_ask[-1])
		
		if len(self.enter_details) > 0:

			if self.enter_details[-1]['Status'] == 0:

				enter = self.enter_details[-1]
				temp_enter = {}

				temp_enter['Price'] = enter['PriceIn']
				temp_enter['Type'] = enter['Type']
				temp_enter['TimeIn'] = enter['TimeIn'].time().strftime("%H:%M:%S")
				temp_enter['nIn'] = enter['nIn']
				temp_enter['Slip. In'] = round(enter['SlippageIn'],2)
				temp_enter['gap_Z'] = round(enter['gap_Z_In'],2)
				temp_enter['price_vol (*10',self.pip_size,')'] =  round(enter['price_vol']*10**self.pip_size,2)
				temp_enter['SpreadIn (*10',self.pip_size,')'] = round(enter['SpreadIn']*10**self.pip_size,2)

				if enter['Type'] == 1:
					temp_enter['Unrlzd PnL'] = round(((self.ls_bid[-1]-enter['PriceIn'])*self.base*self.quantity - self.tp_pnl )*100/self.margin,2)
					temp_enter['sl_price_vol'] = round((self.ls_bid[-1]-self.ls_ask[enter['nIn']])/self.ls_price_vol[-1],2)
					temp_enter['sl_vol_ratio'] = round(self.ls_price_vol[-1]/self.ls_price_vol[enter['nIn']]*np.sign(self.ls_gap_Z[-1]/self.ls_gap_Z[enter['nIn']]),2)

				elif enter['Type'] == -1:
					temp_enter['Unrlzd PnL'] = round(((enter['PriceIn']-self.ls_ask[-1])*self.base*self.quantity-self.tp_pnl )*100/self.margin,2)
					temp_enter['sl_price_vol'] = round((self.ls_bid[enter['nIn']]-self.ls_ask[-1])/self.ls_price_vol[-1],2)
					temp_enter['sl_vol_ratio'] = round(self.ls_price_vol[-1]/self.ls_price_vol[enter['nIn']]*np.sign(self.ls_gap_Z[-1]/self.ls_gap_Z[enter['nIn']]),2)
	
				self.enter_details[-1]['Unrlzd PnL'] = temp_enter['Unrlzd PnL']
				self.enter_details[-1]['sl_price_vol'] = temp_enter['sl_price_vol']
				self.enter_details[-1]['sl_vol_ratio'] = temp_enter['sl_vol_ratio']

				print('\tPrice:',temp_enter['Price'],'\tType:',temp_enter['Type'],'\tN:',temp_enter['nIn'],'\tTime:',temp_enter['TimeIn'],'\tGap_Z',temp_enter['gap_Z'])
				print('\tUnrlzd PnL:',temp_enter['Unrlzd PnL'],'\tSlip. In:',temp_enter['Slip. In'],'\tPrice_Vol:',temp_enter['sl_price_vol'],'\tVol R.:',temp_enter['sl_vol_ratio'],'\t')


	def write_files(self):

		data = []
		err_msg = []

		timestamp = ib.start_time.strftime('%Y%m%d'+'_'+'%H')

		name = self.currency1+'.'+self.currency2
		name1 = self.currency1+'.'+self.currencyBase
		name2 = self.currency2+'.'+self.currencyBase

		for i in range(self.n):
			temp = {}
			temp['Time'] = self.ls_time[i]
			temp[name+'_ask'] = self.ls_ask[i]
			temp[name+'_bid'] = self.ls_bid[i]
			temp[name1+'_ask'] = self.ls_price1_ask[i]
			temp[name1+'_bid'] = self.ls_price1_bid[i]
			temp[name2+'_ask'] = self.ls_price2_ask[i]
			temp[name2+'_bid'] = self.ls_price2_bid[i]
			temp['Spread'] = self.ls_spread[i]
			temp['price'] = self.ls_price[i]
			temp['price_mean'] = self.ls_price_mean[i]
			temp['price_vol'] = self.ls_price_vol[i]
			temp['price_Z'] = self.ls_price_Z[i]
			temp['gap'] = self.ls_gap[i]
			temp['gap_Z'] = self.ls_gap_Z[i]
			temp['gap_mean'] = self.ls_gap_mean[i]
			temp['gap_vol'] = self.ls_gap_vol[i]
			data.append(temp)

		for error in self.err_msg:
			temp = {}
			temp['time'] = error[0]
			temp['errorCode'] = error[1].errorCode
			temp['errorMsg'] = error[1].errorMsg
			err_msg.append(temp)

		df1 = pd.DataFrame(self.strategy)
		df2 = pd.DataFrame(data)
		df3 = pd.DataFrame(err_msg)
		df4 = pd.DataFrame(self.enter_details)

		df1.to_csv(timestamp+'strat.csv')
		df2.to_csv(timestamp+'data.csv')
		df3.to_csv(timestamp+'ERROR.csv')
		df4.to_csv(timestamp+'Enter.csv')






	'''' 			Main starts 			'''



	def exit(self):

		if self.current_pos != 0:

			enter = self.enter_details[-1]

			if enter['Status'] == 0:

				if enter['Type'] == 1:
					if self.ls_spread[-1] < 0.0005:

						condition_tp = 
						condition_sl_1 = 
						condition_sl_2 = 
						condition_sl_3 = 
						condition_sl_4 = 
						condition_sl_5 = 
						temp_sl = [condition_sl_1, condition_sl_2, condition_sl_3, condition_sl_4, condition_sl_5]
						temp_sl_dict = {0: 'SL_1', 1: 'SL_2', 2: 'SL_3', 3: 'SL_4',4: 'SL_5'}

						if condition_tp == 1:
							ib.place_order(action = 'SELL', quantity = self.quantity, contract = self.contract)
							self.tp += 1
							self.exit_type = 'TP'
							enter['Status'] = 1
							self.current_pos -= 1
							self.current_pos_type = 0
							self.update_exit(enter)
						elif condition_sl_1 == 1 or condition_sl_2 == 1 or condition_sl_3 == 1 or condition_sl_4 == 1 or condition_sl_5 == 1:
							ib.place_order(action = 'SELL', quantity = self.quantity, contract = self.contract)
							self.sl += 1
							self.exit_type = temp_sl_dict[temp_sl.index(1)]
							enter['Status'] = 1
							self.current_pos -= 1
							self.current_pos_type = 0
							self.update_exit(enter)

				elif enter['Type'] == -1:
					if self.ls_spread[-1] < 0.0005:

						condition_tp = 
						condition_sl_1 = 
						condition_sl_2 = 
						condition_sl_3 = 
						condition_sl_4 = 
						condition_sl_5 = 
						temp_sl = [condition_sl_1, condition_sl_2, condition_sl_3, condition_sl_4, condition_sl_5]
						temp_sl_dict = {0: 'SL_1', 1: 'SL_2', 2: 'SL_3', 3: 'SL_4',4: 'SL_5'}
						
						if condition_tp == 1:
							ib.place_order(action = 'BUY', quantity = self.quantity, contract = self.contract)
							self.tp += 1
							self.exit_type = 'TP'
							enter['Status'] = 1
							self.current_pos -= 1
							self.current_pos_type = 0
							self.update_exit(enter)
						elif condition_sl_1 == 1 or condition_sl_2 == 1 or condition_sl_3 == 1 or condition_sl_4 == 1 or condition_sl_5 == 1:
							ib.place_order(action = 'BUY', quantity = self.quantity, contract = self.contract)
							self.sl += 1
							self.exit_type = temp_sl_dict[temp_sl.index(1)]
							enter['Status'] = 1
							self.current_pos -= 1
							self.current_pos_type = 0
							self.update_exit(enter)


	def enter(self):

		if self.current_pos == 0:

			self.trade_signal()

			if self.current_pos_type == 1:
				ib.place_order(action = 'BUY', quantity = self.quantity, contract = self.contract)
				self.current_pos += 1
				self.update_enter()

			elif self.current_pos_type == -1:
				ib.place_order(action = 'SELL', quantity = self.quantity, contract = self.contract)
				self.current_pos += 1
				self.update_enter()



	def trade_signal(self):

		if self.n > self.memory:

			if :

				self.current_pos_type = 1

			elif :

				self.current_pos_type = -1


	def get_prices(self):

		quantity = 0
		price = []
		commission = []
		commission_currency = None

		while quantity < self.quantity:

			if len(self.exec_msg) == 0:
				sleep(1)
			elif self.exec_msg[-1]['orderID'] == ib.orderID:
				sleep(2)
				quantity = 0
				price = []
				commission = []
				exec_id = [] 
				for e in self.exec_msg:
					if e['orderID'] == ib.orderID:
						price.append(e['price']*e['qty'])
						exec_id.append(e['ExecID'])
						quantity += e['qty']
				for c in self.comm_msg:
					if c['ExecID'] in exec_id:
						commission.append(c['commission'])
						commission_currency = c['currency']
			else:
				sleep(3)

		return sum(price)/quantity, sum(commission), commission_currency


	def update_exit(self, temp_enter):

		temp_exit = {}

		price, commission, commission_currency = self.get_prices()

		temp_exit['PriceOut'] = price
		temp_exit['CommissionOut'] = commission
		temp_exit['Comm Curr.'] = commission_currency

		temp_exit['TimeOut'] = self.ls_time[-1]
		temp_exit['nOut'] = self.n-1

		if temp_enter['Type'] == 1:
			temp_exit['PriceOutExp'] = self.ls_bid[-1]
			temp_exit['SlippageOut'] = (temp_exit['PriceOut'] - temp_exit['PriceOutExp'])*self.quantity
			temp_exit['PnL'] = (temp_exit['PriceOut'] - temp_enter['PriceIn'])*self.quantity

		elif temp_enter['Type'] == -1:
			temp_exit['PriceOutExp'] = self.ls_ask[-1]
			temp_exit['SlippageOut'] = (temp_exit['PriceOutExp'] - temp_exit['PriceOut'])*self.quantity
			temp_exit['PnL'] = (temp_enter['PriceIn'] - temp_exit['PriceOut'])*self.quantity

		temp_exit['gap_Z_Out'] = self.ls_gap_Z[-1]
		temp_exit['price_vol'] = self.ls_price_vol[-1]
		temp_exit['SpreadOut'] = self.ls_spread[-1]

		temp_exit['TimeDiff'] = temp_exit['nOut'] - temp_enter['nIn']
		temp_exit['PnL Curr.'] = self.currency2
		temp_exit['ExitType'] = self.exit_type

		self.avg_exec = np.mean([float(s['TimeDiff']) for s in self.strategy]+[temp_exit['TimeDiff']])
		self.last_exec = temp_exit['TimeDiff']
		self.total_pnl += temp_exit['PnL']	
		self.total_commission += temp_exit['CommissionOut']+temp_enter['CommissionIn']

		self.exit_details.append(temp_exit)
		temp_dict = {}
		temp_dict['Total PnL'] = self.total_pnl
		temp_dict.update(temp_enter)
		temp_dict.update(temp_exit)
		self.strategy.append(temp_dict)		


	def update_enter(self):

		temp_enter = {}

		price, commission, commission_currency = self.get_prices()

		temp_enter['PriceIn'] = price
		temp_enter['CommissionIn'] = commission
		temp_enter['Comm Curr.'] = commission_currency

		temp_enter['Type'] = self.current_pos_type
		temp_enter['TimeIn'] = self.ls_time[-1]
		temp_enter['nIn'] = self.n-1

		if self.current_pos_type == 1:
			temp_enter['PriceInExp'] = self.ls_ask[-1]
			temp_enter['SlippageIn'] = (temp_enter['PriceInExp'] - temp_enter['PriceIn'])*self.quantity


		elif self.current_pos_type == -1:
			temp_enter['PriceInExp'] = self.ls_bid[-1]
			temp_enter['SlippageIn'] = (temp_enter['PriceIn'] - temp_enter['PriceInExp'])*self.quantity

		temp_enter['Status'] = 0

		temp_enter['gap_Z_In'] = self.ls_gap_Z[-1]
		temp_enter['price_vol'] = self.ls_price_vol[-1]
		temp_enter['SpreadIn'] = self.ls_spread[-1]

		self.enter_details.append(temp_enter)
