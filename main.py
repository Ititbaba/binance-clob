import asyncio

from config import settings
from core.binance_client import BinanceClient
from core.event_reader import EventReader
from core.monitor import Monitor
from core.order_book import OrderBook
from core.order_book_synchronizer import OrderBookSynchronizer


async def main() -> None:
    binance_client = BinanceClient(symbol=settings.symbol)
    order_book = OrderBook(symbol=settings.symbol)
    monitor = Monitor()
    reader = EventReader(binance_client, monitor)
    order_book_synchronizer = OrderBookSynchronizer(
        symbol=settings.symbol,
        binance_client=binance_client,
        order_book=order_book,
        queue=reader.queue,
        monitor=monitor,
    )

    await asyncio.gather(
        reader.run(),
        order_book_synchronizer.run(),
        monitor.run(queue=reader.queue, interval_seconds=10.0),
    )


if __name__ == "__main__":
    asyncio.run(main())
