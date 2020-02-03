

''' 
		Code to download historical prices using ibpy
		Steps:
			1. Creat a connection
			2. Register Error message handler (very important)
			3. Register historical price function to store historical prices
			4. Make a contract
			5. Make an order
			6. connect to TWS
			7. req historical prices
			8. cancel request
			9. disconnect

'''



from ib.opt import message
from ib.opt.connection import Connection
from ib.ext.Contract import Contract
from time import sleep, strftime


def error_handler(message):
	err_msg.append(message)


def hist_handler(message):
	hist_data.append({"reqID": message.reqId, "date": message.date, "open": message.open, "high": message.high, "low": message.low, "close": message.close,})
	#"volume": message.volume, "count": message.count, "WAP": message.WAP, "hashGaps": message.hasGaps})


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


def get_hist_data(sym, curr, end_date_time, duration, tick_size, data_type, sec_type='CASH', exch='IDEALPRO', c_Id=4032, t_Id=1):
	connection = Connection.create(clientId=c_Id)
	connection.register(error_handler, message.Error)
	connection.register(hist_handler, message.historicalData)
	contract = make_contract(sym, sec_type, exch, curr)
	connection.connect()
	sleep(1)
	connection.reqHistoricalData(tickerId = t_Id, contract = contract, endDateTime = end_date_time, durationStr = duration, barSizeSetting = tick_size, whatToShow = data_type, useRTH = 0, formatDate = 1)
	sleep(5)
	connection.disconnect()



# Main starts...

def main():
	symbol = 'EUR'
	currency = 'USD'

	# Look the link for different time formats http://xavierib.github.io/twsapidocs/historical_data.html
	end_date_time = strftime('%Y%m%d %H:%M:%S') 
	duration = '1 W'
	tick_size = '1 min'
	data_type = 'MIDPOINT'


	err_msg=[]
	hist_data=[]

	get_hist_data(symbol, currency, end_date_time, duration, tick_size, data_type)

if __name__ == '__main__':
	main()