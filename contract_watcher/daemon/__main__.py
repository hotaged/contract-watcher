import asyncio
import tortoise

from contract_watcher.daemon.providers import get_eth_provider
from contract_watcher.daemon.logger import get_logger
from contract_watcher.daemon.events import poll_contract_event, event_callback

from contract_watcher.config import settings, TORTOISE_ORM
from contract_watcher.models import Webhook, History


async def main(poll_interval: float = 1.0):
    logger = get_logger(__name__)
    provider = get_eth_provider(settings.rpc_url)

    await tortoise.Tortoise.init(TORTOISE_ORM)

    background_tasks = set()

    logger.info("Daemon initialized.")

    while True:
        for webhook in await Webhook.all():
            try:
                logs = poll_contract_event(
                    provider,
                    webhook.address,
                    webhook.abi,
                    webhook.event
                )
            except Exception as err:
                logger.info(f"Unexpected error: {err}")
                continue

            for log in logs:
                transaction_hash = log['transactionHash'].hex()

                if not await History.filter(transaction_hash=transaction_hash).exists():
                    task = asyncio.create_task(event_callback(webhook, log))
                    task.add_done_callback(background_tasks.discard)
                    background_tasks.add(task)

        await asyncio.sleep(poll_interval)


def run():
    asyncio.run(main(settings.poll_interval))


if __name__ == '__main__':
    run()
