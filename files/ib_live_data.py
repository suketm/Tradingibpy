
''' File to collect live data '''

''' Libraries '''

from ib.opt.connection import Connection
from ib.ext.Contract import Contract
from ib.ext.Order import Order
from ib.opt import message
from time import sleep, strftime, localtime

# External files
import variable
import hist_time
import core

import pandas as pd

''' strategy based function '''

def hist_handler(message):

	global key_ls, templ_ls

	if message.date in key_ls:
		temp_dict = temp_ls[key_ls.index(message.date)]
		temp_dict[message.date]= temp_dict[message.date] + [message.close]
		temp_ls[key_ls.index(message.date)] = temp_dict


def get_hist_data():
	global temp_ls, key_ls
	variable.connection.register(hist_handler, message.historicalData)
	cont = ''

	while cont == '':

		if localtime().tm_sec < 30 and localtime().tm_sec > 15: 			# Since reading each data takes around 3-45 seconds
			current_time = localtime()
			dur = '1 D'
			end = strftime('%Y%m%d %H:%M:%S')
			tick_size = '1 min'
			temp_ls, key_ls = hist_time.make_list()
			
			
			variable.connection.reqHistoricalData(tickerId = variable.tickerId_, contract = variable.contract1, endDateTime = end, durationStr = dur, barSizeSetting = tick_size, whatToShow = 'ASK', useRTH = 0, formatDate = 1)
			sleep(3)
			'''
			all histroical data '''
			variable.current_time = hist_time
			temp_ls.reverse()
			for current_details in temp_ls:
				key = list(current_details.keys())[0]
				items = current_details[key]
				variable.current_time.tm_mday = int(key[6:8])
				variable.current_time.tm_mon = int(key[4:6])
				variable.current_time.tm_year = int(key[0:4])
				variable.current_time.tm_hour = int(key[10:12])
				variable.current_time.tm_min = int(key[13:15])
				variable.current_time.tm_sec = int(key[16:18])
				variable.current_ask = items[0]
				variable.current_bid = items[1]
				core.update_variables()
			variable.current_time = None
			variable.last_time = localtime().tm_min
			variable.connection.cancelHistoricalData(tickerId = variable.tickerId_EUR_USD)
			variable.connection.cancelHistoricalData(tickerId = variable.tickerId_GBP_USD)
			variable.connection.cancelHistoricalData(tickerId = variable.tickerId_EUR_GBP)
			break


def data_handler_price(message):

	if message.tickerId == variable.tickerId_:
		if message.field == 1:
			variable.current_bid = message.price
		elif message.field == 2:
			variable.current_ask = message.price
	
	elif message.tickerId == variable.tickerId_:
		if message.field == 1:
			variable.current_bid = message.price
		elif message.field == 2:
			variable.current_ask = message.price

	elif message.tickerId == variable.tickerId_:
		if message.field == 1:
			variable.current_bid = message.price
		elif message.field == 2:
			variable.current_ask = message.price


def portfolio_message_handler(message):
	contract = message.contract
	if contract.m_symbol == 'EUR' and contract.m_currency == 'GBP':
		variable.unrealizedPNL = message.unrealizedPNL


def account_handler(message):
	if message.key =='TotalCashValue':
		if variable.initialTotalCash == None:
			variable.initialTotalCash = float(message.value)
		else:
			variable.currentTotalCash = message.value
	elif message.key=='TotalCashBalance' and message.currency == 'GBP':
		if variable.initialGBP == None:
			variable.initialGBP = float(message.value)
		else:
			variable.currentGBP = float(message.value)
	elif message.key=='TotalCashBalance' and message.currency == 'EUR':
		if variable.initialEUR == None:
			variable.initialEUR = float(message.value)
		else:
			variable.currentEUR = float(message.value)
	elif message.key=='TotalCashBalance' and message.currency == 'USD' and float(message.value) > 0:
		if variable.initialUSD == None:
			variable.initialUSD = float(message.value)
		else:
			variable.currentUSD = float(message.value)
	elif message.key == 'ExchangeRate' and message.currency == 'GBP':
		variable.exchangeGBP = float(message.value)
	elif message.key == 'ExchangeRate' and message.currency == 'EUR':
		variable.exchangeEUR = float(message.value)
	elif message.key == 'ExchangeRate' and message.currency == 'USD':
		variable.exchangeUSD = float(message.value)


def get_live_data(sec_type='CASH', exch='IDEALPRO'):
	
	variable.connection = Connection.create(clientId = variable.clientID)

	variable.connection.register(error_handler, message.Error)
	variable.connection.register(data_handler_price,message.tickPrice)
	variable.connection.register(next_valid_ID, message.nextValidId)
	variable.connection.register(commission_handler, message.commissionReport)
	variable.connection.register(exec_handler, message.execDetails)
	variable.connection.register(portfolio_message_handler, message.updatePortfolio)
	variable.connection.register(account_handler, message.updateAccountValue)

	variable.contract1 = make_contract(sym = , sec_Type = sec_type, exchange = exch, currency = )
	variable.contract2 = make_contract(sym = , sec_Type = sec_type, exchange = exch, currency = )
	variable.contract3 = make_contract(sym = , sec_Type = sec_type, exchange = exch, currency = )
	
	variable.connection.connect()
	sleep(1)
	variable.connection_status = 1
	get_hist_data()

	variable.connection.reqMarketDataType(marketDataType = 1)
	variable.connection.reqMktData(tickerId = variable.tickerId_, contract = variable.contract1, genericTickList = "", snapshot = False)
	variable.connection.reqMktData(tickerId = variable.tickerId_, contract = variable.contract2, genericTickList = "", snapshot = False)
	variable.connection.reqMktData(tickerId = variable.tickerId_, contract = variable.contract3, genericTickList = "", snapshot = False)
	variable.connection.reqAccountUpdates(subscribe = True, acctCode = variable.accntID)


''' general ibpy function '''

def error_handler(message):
	variable.err_msg.append([localtime(),message])
	if message.errorCode == 1100:
		variable.connection_status = 0
	elif message.errorCode == 1101:
		get_live_data()
	elif message.errorCode == 1102:
		variable.last_time = localtime().tm_min
		variable.connection_status = 1


def exec_handler(message):
	order_id = message.execution.m_orderId
	price = message.execution.m_price
	side = message.execution.m_side
	if variable.posType == 1:
		variable.price_enter.append([variable.n,order_id,price,side])
	elif variable.posType == 0:
		variable.price_exit.append([variable.n,order_id,price,side])
		
		
def commission_handler(message):
	commission = message.commissionReport.m_commission
	currency = message.commissionReport.m_currency
	if variable.posType == 1:
		variable.commission_enter.append([variable.n,commission,currency])
	elif variable.posType == 0:
		variable.commission_exit.append([variable.n,commission,currency])


def next_valid_ID(message):
	variable.orderID = int(message.orderId)


def make_contract(sym, sec_Type, exchange, currency):
	contract = Contract()
	contract.m_symbol = sym
	contract.m_secType = sec_Type
	contract.m_exchange =  exchange
	contract.m_currency = currency
	return contract


def make_order(action):
	order = Order()
	order.m_orderId = variable.orderID
	order.m_clientId = variable.clientID
	order.m_action = action
	order.m_totalQuantity = variable.quantity
	order.m_orderType = "MKT"
	# Limit Order: if Price == None:
	return order


def place_order(action):
	variable.orderID += 1
	order = make_order(action)
	sleep(1)
	variable.connection.placeOrder(id = variable.orderID, contract = variable.contract1, order = order)
	sleep(1)


def terminate_live_data():
	variable.connection.cancelMktData(tickerId = variable.tickerId_)
	variable.connection.cancelMktData(tickerId = variable.tickerId_)
	variable.connection.cancelMktData(tickerId = variable.tickerId_)
	variable.connection.disconnect()