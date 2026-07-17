import asyncio

from config import settings
from models.binance_client import BinanceClient
from models.order_book import OrderBook
from models.order_book_synchronizer import OrderBookSynchronizer
from models.event_reader import EventReader


async def main() -> None:
    binance_client = BinanceClient(symbol=settings.symbol)
    order_book = OrderBook(symbol=settings.symbol)
    reader = EventReader(binance_client)
    order_book_synchronizer = OrderBookSynchronizer(
        symbol=settings.symbol, binance_client=binance_client, order_book=order_book, queue=reader.queue
    )

    await asyncio.gather(reader.run(), order_book_synchronizer.run())


if __name__ == "__main__":
    asyncio.run(main())
