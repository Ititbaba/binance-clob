import asyncio

from config import settings
from models.binance_client import BinanceClient
from models.monitoring import Monitor
from models.order_book import OrderBook
from models.sync_manager import SyncManager


async def main() -> None:
    binance_client = BinanceClient(symbol=settings.symbol)
    order_book = OrderBook(symbol=settings.symbol)
    monitor = Monitor()
    sync_manager = SyncManager(
        symbol=settings.symbol, binance_client=binance_client, order_book=order_book, monitor=monitor
    )

    await sync_manager.run()


if __name__ == "__main__":
    asyncio.run(main())
