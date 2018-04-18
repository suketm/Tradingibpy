
''' File to collect live data '''

''' Libraries '''

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from time import sleep, localtime

# External files
import variable
import ib_live_data

''' update variables '''

def update_variables():

	variable.ls_date.append({'date': variable.current_time.tm_mday, 'month': variable.current_time.tm_mon, 'year': variable.current_time.tm_year})
	variable.ls_time.append({'H': variable.current_time.tm_hour, 'M': variable.current_time.tm_min,'S': variable.current_time.tm_sec})	
	variable.ls__ask.append(variable.current__ask)
	variable.ls__bid.append(variable.current__bid)
	variable.ls__ask.append(variable.current__ask)
	variable.ls__bid.append(variable.current__bid)
	variable.ls__ask.append(variable.current__ask)
	variable.ls__bid.append(variable.current__bid)
	
	variable.n = len(variable.ls_date)

	
	if variable.n == variable.memory:
		''' Learn from prevoius '''

	elif variable.n > variable.memory:
		
	''' Now start execution '''
	


def trade_signal():

	
def take_position():

	if variable.current_pos == 1:
		variable.posType = 1
		ib_live_data.place_order('BUY')
		update_enter_details()
		
	elif variable.current_pos == -1:
		variable.posType = 1
		ib_live_data.place_order('SELL')
		update_enter_details()
		

def exit_position():

	n_in = variable.enter_details['nIn']
	n_out = variable.n-1
	

	if :
		variable.posType = 0
		ib_live_data.place_order('SELL')
		if :
			variable.exitSigType = 'SL'
			variable.nSL += 1
		else:
			variable.exitSigType = 'TP'
			variable.nTP += 1
		update_exit_details()

	elif :
		
		variable.posType = 0
		ib_live_data.place_order('BUY')
		if:
			variable.exitSigType = 'SL'
			variable.nSL += 1
		else:
			variable.exitSigType = 'TP'
			variable.nTP += 1
		update_exit_details()
	

def getPrices(type):

	if variable.lastGBP == None:
		variable.lastGBP = variable.initialGBP

	if type == 1:
		while type == 1:
			if variable.currentGBP != variable.lastGBP and len(variable.price_enter) == variable.ns + 1:
				break
	elif type == 2:
		while type == 2:
			if variable.currentGBP != variable.lastGBP and len(variable.price_exit) == variable.ns + 1:
				break


def get_dd():

	temp = [ (variable.ls__ask[i] + variable.ls__bid[i])/2 for i in range(variable.enter_details['nIn']+1, variable.exit_details['nOut']+1)]
	dd = 0
	if variable.current_pos == 1 and temp != []:
		dd = ((variable.enter_details['Enter Price'] - min(temp))/variable.enter_details['Enter Price'])*100
	elif  variable.current_pos == -1 and temp != []:
		dd = ((max(temp) - variable.enter_details['Enter Price'])/variable.enter_details['Enter Price'])*100
	variable.dd.append(dd)
	variable.exit_details['DD'] = dd
	variable.max_dd = max(variable.dd)


def update_enter_details():

	getPrices(1)
	n = variable.n
	ns = variable.ns		#it is not yet updated
	entered_price = variable.price_enter[ns]
	commission =  variable.commission_enter[ns]
	if variable.current_pos == 1:
		expected_price = variable.ls__ask[n-1]
		variable.slippage_enter.append((expected_price - entered_price[2])*variable.quantity)

	elif  variable.current_pos == -1:
		expected_price = variable.ls__bid[n-1]
		variable.slippage_enter.append((entered_price[2] - expected_price)*variable.quantity)

	variable.enter_details['Current_GBP_enter'] = variable.lastGBP  # to be grabbed before
	variable.enter_details['Type'] = variable.current_pos
	variable.enter_details['DateIn'] = variable.ls_date[n-1]
	variable.enter_details['TimeIn'] = variable.ls_time[n-1]
	variable.enter_details['nIn'] = n-1
	variable.enter_details['Exp. Enter Price'] = expected_price
	variable.enter_details['Enter Price'] = entered_price[2]
	variable.enter_details['SlippageIn'] = variable.slippage_enter[ns]
	variable.enter_details['CommissionIn'] = commission[1]
	variable.enter_details['Comm Curr.'] = commission[2]
	variable.enter_details['ActionIn'] = entered_price[3]
	

def update_exit_details():

	getPrices(2)
	n = variable.n
	ns = variable.ns		#it is not yet updated
	exit_price =  variable.price_exit[ns]
	commission = variable.commission_exit[ns]
	if variable.current_pos == 1:
		expected_price = variable.ls__bid[n-1]
		variable.slippage_exit.append((exit_price[2] - expected_price)*variable.quantity)

	elif  variable.current_pos == -1:
		expected_price = variable.ls__ask[n-1]
		variable.slippage_exit.append((expected_price - exit_price[2])*variable.quantity)

	variable.exit_details['Current_GBP_exit'] = variable.currentGBP   # to be grabbed after	
	variable.exit_details['DateOut'] = variable.ls_date[n-1]
	variable.exit_details['TimeOut'] = variable.ls_time[n-1]
	variable.exit_details['nOut'] = n-1
	variable.exit_details['Exp. Exit Price'] = expected_price
	variable.exit_details['Exit Price'] = exit_price[2]
	variable.exit_details['SlippageOut'] = variable.slippage_exit[ns]
	variable.exit_details['CommissionOut'] = commission[1]
	variable.exit_details['Comm Curr.'] = commission[2]
	variable.exit_details['ActionOut'] = exit_price[3]
	variable.exit_details['Time Diff'] = variable.exit_details['nOut'] - variable.enter_details['nIn']
	variable.exit_details['PnL'] = variable.exit_details['Current_GBP_exit'] - variable.enter_details['Current_GBP_enter']
	variable.exit_details['PnL Curr'] = 'GBP'
	variable.exit_details['ExitType'] = variable.exitSigType

	get_dd()
	variable.ls_pnl.append(variable.exit_details['PnL'])
	variable.totalPNL = variable.currentGBP - variable.initialGBP
	update_strategy()


def update_strategy():

	temp_dict = {}
	temp_dict.update(variable.enter_details)
	temp_dict.update(variable.exit_details)
	variable.strategy.append(temp_dict)
	variable.avg_exec = np.mean([float(s['Time Diff']) for s in variable.strategy])

	if variable.exit_details['PnL'] > 0:
		variable.strategy_X.append(temp_dict)
		variable.avg_exec_X = np.mean([float(s['Time Diff']) for s in variable.strategy_X])
	elif variable.exit_details['PnL'] < 0:
		variable.strategy_Y.append(temp_dict)
		variable.avg_exec_Y = np.mean([float(s['Time Diff']) for s in variable.strategy_Y])

	variable.last_exec = variable.exit_details['Time Diff']
	variable.ns = len(variable.strategy)
	variable.nx = len(variable.strategy_X)
	variable.ny = len(variable.strategy_Y)
	if variable.ns !=0:
		variable.hitRatio = float(variable.nx)/variable.ns


def display():

	n = variable.n
	enter = variable.enter_details 
	exit = variable.exit_details
	current_date = str(variable.ls_date[n-1]['year'])+'/'+str(variable.ls_date[n-1]['month'])+'/'+str(variable.ls_date[n-1]['date'])
	current_time = str(variable.ls_time[n-1]['H'])+':'+str(variable.ls_time[n-1]['M'])+':'+str(variable.ls_time[n-1]['S'])
	comm1 = sum([float(c[1]) for c in variable.commission_enter])
	comm2 = sum([float(c[1]) for c in variable.commission_exit])

	print ("\n\n")
	print ('\tN: ',n,'\tTime: ',current_time,'\tCurrent Pos.: ',variable.current_pos,'\tCurr Gap Z: ',rd_format(variable.ls_gap_Z[n-1],2),'\tPnL (GBP): ',rd_format(variable.totalPNL),'\tTotal Commission (USD):',\
		rd_format(comm1+comm2,2),'\tMax Drawdown (in %): ',rd_format(variable.max_dd,4))
	print ('\tInitial GBP: ',variable.initialGBP,'\tInitial EUR: ',variable.initialEUR,'\tInitial USD: ',variable.initialUSD,'\tInitial Total Cash: ',variable.initialTotalCash)
	print ('\tCurrent GBP: ',variable.currentGBP,'\tCurrent EUR: ',variable.currentEUR,'\tCurrent USD: ',variable.currentUSD,'\tCurrent Total Cash: ',variable.currentTotalCash)
	print ('\tTotal Trades: ',variable.ns,'\tTotal Pos. trades: ',variable.nx,'\tTotal Neg. trades: ',variable.ny,'\tHit Ratio: ',rd_format(variable.hitRatio,2),'\tTP: ',variable.nTP,'\tSL:',variable.nSL)
	print ('\tLast exec time: ',variable.last_exec,'\tAverage holding time:',rd_format(variable.avg_exec,2),'\tAverage holding time for positive: ',rd_format(variable.avg_exec_X,2),'\tAverage holding time for Negative: ',rd_format(variable.avg_exec_Y,2))


	if variable.posType == 1:
		timeIn = str(enter['TimeIn']['H']) + ':' + str(enter['TimeIn']['M']) + ':' +str(enter['TimeIn']['S'])
		print ('\tEntered Time: ',enter['nIn'],'(',timeIn,')','\tEntered price: ',enter['Enter Price'],'\tSlipg.In: ',rd_format(enter['SlippageIn']),'\tComm. (',enter['Comm Curr.'],'): ',enter['CommissionIn'])
		print ('\tUnrealizedPnL: ',variable.unrealizedPNL,'\tEntered Type: ',enter['ActionIn'],'\t\tEntered Gap Z: ',rd_format(enter['gap_Z_In'],2),'\tGap Mean Vol (*10^-4): ',rd_format(variable.gap_mean_vol*10000,2))

	elif variable.posType == 0 and variable.current_pos != 0:
		print ('\tEnter Gap Z: ',rd_format(enter['gap_Z_In'],2),'\tEntered Type: ',enter['ActionIn'],'\tEntered price: ',enter['Enter Price'],'\tSlipg.In: ',rd_format(enter['SlippageIn']),'\tComm. (',enter['Comm Curr.'],') : ',enter['CommissionIn'])
		print ('\tExit Gap Z: ',rd_format(exit['gap_Z_Out'],2),'\tExit Type: ',exit['ActionOut'],'\tExit price: ',exit['Exit Price'],'\t\tSlipg.Out: ',rd_format(exit['SlippageOut']),'\tComm. (',exit['Comm Curr.'],') : ',exit['CommissionOut'])
		print ('\tProfit in GBP: ',rd_format(exit['PnL']),'\t','Execution Time: ',exit['Time Diff'],'\tExit Gap Mean Vol (*10^-4): ',rd_format(variable.gap_mean_vol*10000,2))

	variable.lastGBP = variable.currentGBP
	if variable.posType == 0:
		variable.current_pos = 0
	variable.writeData = 1


def write_files():
	data = []
	err_msg = []
	x_time = [[x['nIn'],x['nOut']] for x in variable.strategy_X]
	y_time = [[y['nIn'],y['nOut']] for y in variable.strategy_Y]
	timestamp = str(variable.current_time.tm_year)+str(variable.current_time.tm_mon)+str(variable.current_time.tm_mday)+'_'+str(variable.current_time.tm_hour)

	for i in range(variable.n):
		temp = {}
		temp['Date'] = str(variable.ls_date[i]['year'])+str(variable.ls_date[i]['month'])+str(variable.ls_date[i]['date'])
		temp['Time'] = str(variable.ls_time[i]['H'])+':'+str(variable.ls_time[i]['M'])+':'+str(variable.ls_time[i]['S'])
		temp['Eur_Usd_Ask'] = variable.ls_eur_usd_ask[i]
		temp['Eur_Usd_Bid'] = variable.ls_eur_usd_bid[i]
		temp['Gbp_Usd_Ask'] = variable.ls_gbp_usd_ask[i]
		temp['Gbp_Usd_Bid'] = variable.ls_gbp_usd_bid[i]
		temp['Eur_Gbp_Ask'] = variable.ls_eur_gbp_ask[i]
		temp['Eur_Gbp_Bid'] = variable.ls_eur_gbp_bid[i]
		temp['Eur_Usd_mid'] = variable.ls_eur_usd_mid[i]
		temp['Gbp_Usd_mid'] = variable.ls_gbp_usd_mid[i]
		data.append(temp)

	for error in variable.err_msg:
		temp = {}
		temp['time'] = str(error[0].tm_year)+'/'+str(error[0].tm_mon)+'/'+str(error[0].tm_mday)+'  '+str(error[0].tm_hour)+':'+str(error[0].tm_min)+':'+str(error[0].tm_sec)
		temp['errorCode'] = error[1].errorCode
		temp['errorMsg'] = error[1].errorMsg
		err_msg.append(temp)

	df1 = pd.DataFrame(variable.strategy)
	df2 = pd.DataFrame(data)
	df3 = pd.DataFrame(err_msg)
	# strat_X and strat_Y

	df1.to_csv(timestamp+'strat.csv')
	df2.to_csv(timestamp+'data.csv')
	df3.to_csv('ERROR.csv')

	plt.close('all')

	plt.figure(1)
	plt.plot(range(variable.memory,variable.n),variable.ls_eur_gbp_ask[variable.memory:variable.n], color = 'olive',  label = 'Ask')
	plt.plot(range(variable.memory,variable.n),variable.ls_eur_gbp_bid[variable.memory:variable.n], color = 'maroon',  label = 'Bid')
	for t in x_time:
		plt.plot(range(t[0],t[1]+1),variable.ls_eur_gbp_ask[t[0]:t[1]+1], color = 'green')
		plt.plot(range(t[0],t[1]+1),variable.ls_eur_gbp_bid[t[0]:t[1]+1], color = 'green')
	for t in y_time:
		plt.plot(range(t[0],t[1]+1),variable.ls_eur_gbp_ask[t[0]:t[1]+1], color = 'red')
		plt.plot(range(t[0],t[1]+1),variable.ls_eur_gbp_bid[t[0]:t[1]+1], color = 'red')
	plt.xlabel('Time')
	plt.ylabel('Eur/Gbp')
	plt.legend()
	plt.savefig(timestamp+'Eur_Gbp.png')
	plt.figure(2)
	plt.plot(range(variable.memory,variable.n),variable.ls_gap[variable.memory:variable.n], label = 'Gap')
	for t in x_time:
		plt.plot(range(t[0],t[1]+1),variable.ls_gap[t[0]:t[1]+1], color = 'green')
	for t in y_time:
		plt.plot(range(t[0],t[1]+1),variable.ls_gap[t[0]:t[1]+1], color = 'red')
	plt.xlabel('Time')
	plt.ylabel('Gap: Gbp-Eur')
	plt.legend()
	plt.savefig(timestamp+'Gap.png')
	plt.close('all')

	#plt.show(block = False)
	variable.writeData = 0


def rd_format(val, decimal_place = None):

	if val != None:
		if decimal_place != None:
			return round(val,decimal_place)
		else:
			return round(val)