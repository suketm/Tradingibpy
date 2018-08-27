
''' All variables '''

''' Libraries '''

from ib.opt.connection import Connection
from ib.ext.Contract import Contract
from ib.ext.Order import Order
from ib.opt import message


# External files

''' Variables '''

# variables
cont = ''
current_time = None
connection_status = None
start_time = None
current_time = None
last_time_min = None

# live data
data = {'tickID': None, 'price': None,'field': None}
commission = []
execution = []
err_msg = []
initialTotalCash = None
currentTotalCash = None
cashBalanceInitial ={}
cashBalance = {}
exchRate = {}

# ib
clientID = 4032
accntID = 'DU983969'
orderID = None
connection = None
connection_status = None		# 0: Paused/ 1: active