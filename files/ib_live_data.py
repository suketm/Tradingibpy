''' File to collect live data '''

''' Libraries '''

from ib.opt.connection import Connection
from ib.ext.Contract import Contract
from ib.ext.Order import Order
from ib.opt import message
from time import sleep
from datetime import datetime

# External files
from strategy import Strategy


''' ib_live_data starts '''

clientID = Strategy.clientID
orderID = None
connection = None
connection_status = None		# 0: Paused/ 1: active
start_time = None
last_time = None
current_time = None

def establish_connection():

	global connection, clientId, start_time, connection_status
	
	connection = Connection.create(clientId = clientID)

	connection.register(error_handler, message.Error)
	connection.register(hist_handler, message.historicalData)
	connection.register(data_handler_price,message.tickPrice)
	connection.register(next_valid_ID, message.nextValidId)
	connection.register(commission_handler, message.commissionReport)
	connection.register(exec_handler, message.execDetails)

	connection.connect()
	sleep(1)
	connection_status = 1
	start_time = datetime.now()


def error_handler(message):

	global connection_status, last_time

	Strategy.err_msg.append([datetime.now(), message])
	if message.errorCode == 1100:
		connection_status = 0
	elif message.errorCode == 1101:
		establish_connection()
	elif message.errorCode == 1102:
		last_time = datetime.now()
		connection_status = 1



def hist_handler(message):
	
	if 'finished' not in message.date:
		date = datetime.strptime(message.date,'%Y%m%d %H:%M:%S')
		if date not in Strategy.hist_data:
			Strategy.hist_data[date] = {}
		if message.reqId not in Strategy.hist_data[date]:
			Strategy.hist_data[date][message.reqId] = []
		Strategy.hist_data[date][message.reqId].append(message.close)


def get_hist_data(tickerID, contract, end, dur, tick_size):

	global connection, clientId, start_time, connection_status

	connection.reqHistoricalData(tickerId = tickerID, contract = contract, endDateTime = end, durationStr = dur, barSizeSetting = tick_size, whatToShow = 'ASK', useRTH = 0, formatDate = 1)
	sleep(3)
	connection.reqHistoricalData(tickerId = tickerID, contract = contract, endDateTime = end, durationStr = dur, barSizeSetting = tick_size, whatToShow = 'BID', useRTH = 0, formatDate = 1)
	sleep(3)
	connection.cancelHistoricalData(tickerId = tickerID)


def data_handler_price(message):

	if message.price > 0:
		Strategy.live_data[message.tickerId][message.field] = message.price


def get_live_data(tickerId, contract):

	global connection

	connection.reqMarketDataType(marketDataType = 1)
	connection.reqMktData(tickerId = tickerId, contract = contract, genericTickList = "", snapshot = False)


def next_valid_ID(message):

	global orderID

	orderID = int(message.orderId)


def commission_handler(message):
	temp_comm = {}
	temp_comm['commission'] = message.commissionReport.m_commission
	temp_comm['currency'] = message.commissionReport.m_currency
	temp_comm['ExecID'] = message.commissionReport.m_execId
	Strategy.comm_msg.append(temp_comm)


def exec_handler(message):
	temp_exec = {}
	temp_exec['orderID'] = message.execution.m_orderId
	temp_exec['price'] = message.execution.m_price
	temp_exec['side'] = message.execution.m_side
	temp_exec['qty'] = message.execution.m_shares
	temp_exec['ExecID'] = message.execution.m_execId
	Strategy.exec_msg.append(temp_exec)


def make_contract(sym, sec_Type, exchange, currency):
	contract = Contract()
	contract.m_symbol = sym
	contract.m_secType = sec_Type
	contract.m_exchange =  exchange
	contract.m_currency = currency
	return contract


def make_order(action, quantity):

	global orderID, clientID

	order = Order()
	order.m_orderId = orderID
	order.m_clientId = clientID
	order.m_action = action
	order.m_totalQuantity = quantity
	order.m_orderType = "MKT"
	return order


def place_order(action, quantity, contract):

	global orderID, connection

	orderID += 1
	order = make_order(action, quantity)
	connection.placeOrder(id = orderID, order = order, contract = contract)


def terminate_connection():

	global connection

	connection.disconnect()