from web3 import Web3
from web3.middleware import geth_poa_middleware


def get_eth_provider(uri: str) -> Web3:
    web = Web3(Web3.HTTPProvider(uri))
    web.middleware_onion.inject(geth_poa_middleware, layer=0)
    return web
