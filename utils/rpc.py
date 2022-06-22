from web3 import Web3
from web3.middleware import geth_poa_middleware

from utils.constants import *

# web3
w3 = Web3(Web3.HTTPProvider(AVAX_RPC))

if not w3.isConnected():
    print("Error web3 can't connect")
w3.middleware_onion.inject(geth_poa_middleware, layer=0)
