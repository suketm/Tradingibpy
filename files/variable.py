
''' All variables '''

''' Libraries '''

from ib.opt.connection import Connection
from ib.ext.Contract import Contract
from ib.ext.Order import Order
from ib.opt import message
from time import localtime

# External files

''' Fixed variables '''

time_gap = 1	# in minutes
memory = 30		# in mins
cont = ''		# to keep the loop going
current_pos = 0	# No ongoing trade
posType = 0		# 1: Enter , 0: Exit		
n = 0			# Size of input
ns = 0			# Size of strategy
nx = 0			# Size of strategy, positive trades
ny = 0			# Size of strategy, negative trades
nTP = 0			# No. of times SL triggered
nSL = 0			# No. of times SL triggered
hitRatio = 0
gap_mean_vol = 0
writeData = 1
''' Quant Parameters '''



''' Variables '''

current__ask = None
current__bid = None
current__ask = None
current__bid = None
current__ask = None
current__bid = None


current_time = None
current_time_minute = None
last_time = None	# in minutes
max_dd = None
totalPNL = None
unrealizedPNL = None
initialTotalCash = None
currentTotalCash = None
initialGBP = None
lastGBP = None
currentGBP = None
initialEUR = None
currentEUR = None
initialUSD = None
currentUSD = None
exchangeGBP = None
exchangeEUR = None
exchangeUSD = None
last_exec = None
avg_exec = None
avg_exec_X = None
avg_exec_Y = None
exitSigType = None

ls_date = []
ls_time = []

ls_pnl = []

price_enter = []
price_exit = []
commission_enter = []
commission_exit = []
slippage_enter = []
slippage_exit = []
dd = []

strategy = []
strategy_X = []
strategy_Y = []
enter_details = {}
exit_details = {}

''' Variables for IBPY '''

err_msg = []
clientID = 4032
tickerId_ = 873
tickerId_ = 874
tickerId_ = 875
accntID = 'ACCOUNT NUMBER'
quantity = 10000000
orderID = None

# establish connection
connection = None
connection_status = None		# 0: Paused/ 1: active

# contracts
contract1 = None
contract2 = None
contract3 = None