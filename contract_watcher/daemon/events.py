import json
import aiohttp.client

from hexbytes import HexBytes
from functools import partial

from web3 import Web3
from web3.datastructures import AttributeDict
from web3.types import LogReceipt, Address, ABI

from contract_watcher.daemon.logger import get_logger
from contract_watcher.models import Webhook


logger = get_logger(__name__)


class HexJsonEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, HexBytes):
            return obj.hex()
        if isinstance(obj, AttributeDict):
            return dict(obj)
        return super().default(obj)


serializer = partial(json.dumps, cls=HexJsonEncoder)


def poll_contract_event(p: Web3, addr: Address, abi: ABI, event: str) -> list[LogReceipt]:
    from_block = p.eth.get_block_number() - 4000
    contract = p.eth.contract(address=addr, abi=abi)

    return contract.events[event].create_filter(fromBlock=from_block).get_all_entries()


async def event_callback(wh: Webhook, log: LogReceipt):
    logger.info(f"New event {log['transactionHash']}.")

    history = await wh.create_log_history(json.loads(serializer(log)), False)

    try:
        async with aiohttp.client.ClientSession(
                json_serialize=serializer
        ) as session:
            async with session.post(wh.url, json=dict(log)) as response:
                logger.info(f"Request sent. Response: {response}")
                history.sent = True

    except aiohttp.client.ClientError as conn_error:
        logger.warning(f"Cannot send event log. Exception: {conn_error}")
        history.sent = False

    await history.save()
