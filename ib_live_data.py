
''' File to collect live data '''

''' Libraries '''

from ib.opt.connection import Connection
from ib.ext.Contract import Contract
from ib.ext.Order import Order
from ib.opt import message
from time import localtime, sleep

# External files
import variable as v


''' ib_live_data starts '''

def hist_handler(message):
	if message.date in keys:
		temp_ls[message.date].append(message.close)


def get_hist_data(tickerID, contract, end, dur, tick_size, temp_list, temp_key):
	global temp_ls, keys
	temp_ls = temp_list
	keys = temp_key
	v.connection.reqHistoricalData(tickerId = tickerID, contract = contract, endDateTime = end, durationStr = dur, barSizeSetting = tick_size, whatToShow = 'ASK', useRTH = 0, formatDate = 1)
	sleep(3)
	v.connection.reqHistoricalData(tickerId = tickerID, contract = contract, endDateTime = end, durationStr = dur, barSizeSetting = tick_size, whatToShow = 'BID', useRTH = 0, formatDate = 1)
	sleep(3)
	v.connection.cancelHistoricalData(tickerId = tickerID)
	return temp_ls


def establish_connection():
	
	v.connection = Connection.create(clientId = v.clientID)

	v.connection.register(error_handler, message.Error)
	v.connection.register(hist_handler, message.historicalData)
	v.connection.register(data_handler_price,message.tickPrice)
	v.connection.register(next_valid_ID, message.nextValidId)
	v.connection.register(commission_handler, message.commissionReport)
	v.connection.register(exec_handler, message.execDetails)
	v.connection.register(account_handler, message.updateAccountValue)

	v.connection.connect()
	sleep(1)
	v.start_time = localtime()


def error_handler(message):
	v.err_msg.append([localtime(),message])
	if message.errorCode == 2104:
		v.connection_status = 1
	elif message.errorCode == 1100:
		v.connection_status = 0
	elif message.errorCode == 1101:
		get_live_data()
	elif message.errorCode == 1102:
		v.connection_status = 1


def data_handler_price(message):
	if message.price > 0:
		v.data = {'tickID': message.tickerId, 'price': message.price,'field': message.field}


def next_valid_ID(message):
	v.orderID = int(message.orderId)


def commission_handler(message):
	v.commission.append({'commisison': message.commissionReport.m_commission,'comm. cny': message.commissionReport.m_currency })


def exec_handler(message):
	v.execution.append({'orderID': message.execution.m_orderId, 'price': message.execution.m_price, 'side': message.execution.m_side, 'qty': message.execution.m_shares})


def make_contract(sym, sec_Type, exchange, currency):
	contract = Contract()
	contract.m_symbol = sym
	contract.m_secType = sec_Type
	contract.m_exchange =  exchange
	contract.m_currency = currency
	return contract


def make_order(action, qty):
	order = Order()
	order.m_orderId = v.orderID
	order.m_clientId = v.clientID
	order.m_action = action
	order.m_totalQuantity = qty
	order.m_orderType = "MKT"
	# Limit Order: if Price == None:
	return order


def place_order(action, qty, contract):
	v.orderID += 1
	order = make_order(action, qty)
	v.connection.placeOrder(id = v.orderID, contract = contract, order = order)


def terminate_connection():
	v.connection.disconnect()


def account_handler(message):
	if message.key =='TotalCashValue':
		if v.initialTotalCash == None:
			v.initialTotalCash = float(message.value)
		else:
			v.currentTotalCash = message.value
	elif message.key=='TotalCashBalance':
		if message.currency in list(v.cashBalanceInitial.keys()):
			v.cashBalance[message.currency] = float(message.value)
		else:
			v.cashBalanceInitial[message.currency] = float(message.value)
	elif message.key == 'ExchangeRate':
		v.exchRate[message.currency] = float(message.value)