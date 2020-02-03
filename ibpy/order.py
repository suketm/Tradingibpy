

''' 
		Code to place an order using ibpy
		Steps:
			1. Creat a connection
			2. Register Error message handler (very important)
			3. Register commission and execution report handler
			5. Get the next valid ID
			6. Make a contract
			7. Make an order
			8. connect to TWS 
			9. place order
			10. disconnect

'''



from ib.ext.Contract import Contract
from ib.ext.Order import Order
from ib.opt.connection import Connection
from ib.opt import message
from time import sleep

def error_handler(message):
	err_msg.append(message)


def commission_report(message):
	msg_commission = message.commissionReport
	commission_msg.append([message,msg_commission.m_execId, msg_commission.m_commission, msg_commission.m_currency, msg_commission.m_realizedPNL])


def exec_report(message):
	msg_exec = message.execution
	exec_msg.append([msg_exec.m_orderId, msg_exec.m_clientId, msg_exec.m_execId, msg_exec.m_time, msg_exec.m_acctNumber, msg_exec.m_exchange, \
	msg_exec.m_side, msg_exec.m_shares, msg_exec.m_price])


def next_valid_id(message):
	next_order_ID = message.orderId


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


def make_order(o_Id, c_Id, action, qty, Price=None):
	order = Order()
	order.m_orderId = o_Id
	order.m_clientId = c_Id
	order.m_action = action
	order.m_totalQuantity = qty
	if Price==None:
		order.m_orderType = "MKT"
	else:
		order.m_orderType = "LMT"
		order.m_lmtPrice = float(Price)
	return order


def place_order(o_Id, sym, curr, action, qty, sec_type='CASH', exch='IDEALPRO', c_Id=4032):
	connection = Connection.create(clientId = c_Id)
	connection.register(error_handler, message.Error)
	connection.register(commission_report, message.commissionReport)
	connection.register(exec_report, message.execDetails)
	connection.register(next_valid_id, message.nextValidId)
	contract = make_contract(sym, sec_type, exch, curr)
	order = make_order(o_Id, c_Id, action, qty)
	connection.connect()
	sleep(1)
	connection. placeOrder(	id = o_Id, contract = contract, order = order)
	sleep(2)
	connection.disconnect()


# Main starts...
def main():
	order_Id = None

	symbol = 'EUR'
	currency = 'USD'
	action = 'BUY'
	quantity = 50000


	err_msg=[]
	commission_msg=[]
	exec_msg=[]

	place_order(order_Id, symbol, currency, action, quantity)


if __name__ == '__main__':
	main()