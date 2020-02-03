

''' 
		Code to get live quotes using ibpy
		Steps:
			1. Creat a connection
			2. Register Error message handler (very important)
			3. Register live price handler
			4. Make a contract
			6. connect to TWS 
			7. request market data
			8. cancel market data
			9. disconnect

'''
from ib.ext.Contract import Contract
from ib.opt.connection import Connection
from ib.opt import message
from time import sleep

def error_handler(message):
	err_msg.append(message)


def data_handler_price(message):
	if message.field == 1:
		print "Bid: ",message.price
	elif message.field == 2:
		print "Ask: ",message.price


def make_contract(sym, sec_type, exch, curr):
	contract = Contract()
	contract.m_symbol = sym
	contract.m_secType = sec_type
	#contract.m_expiry = 
	#contract.m_strike = float()
	contract.m_exchange =  exch
	contract.m_currency = curr
	#contract.m_tradingClass =
	#contract.m_primaryExch =  #  pick a non-aggregate (ie not the SMART exchange) exchange that the contract trades on.  DO NOT SET TO SMART.
	return contract


def get_live_data(sym, curr, duration, sec_type='CASH', exch='IDEALPRO', c_Id=4032, t_Id=900):
	connection = Connection.create(clientId = c_Id)
	connection.register(error_handler, message.Error)
	connection.register(data_handler_price,message.tickPrice)
	contract = make_contract(sym, sec_type, exch, curr)
	connection.connect()
	sleep(1)
	connection.reqMarketDataType(1)
	connection.reqMktData(873,contract,"",False)
	sleep(duration)
	connection.cancelMktData(tickerId = t_Id)
	connection.disconnect()


# Main Starts...

def main():
	symbol = 'EUR'
	currency = 'USD'
	duration = 	10		# for sleep

	err_msg=[]

	get_live_data(symbol, currency, duration)


if __name__ == '__main__':
	main()