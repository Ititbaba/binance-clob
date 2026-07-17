import asyncio
from enum import Enum, auto

from models.binance_client import BinanceClient
from models.monitoring import Monitor
from models.order_book import OrderBook
from schemas.market_data import UpdateEvent


class SyncState(Enum):
    BUFFERING = auto()
    SYNCING = auto()
    SYNCED = auto()


class OrderBookSynchronizer:
    def __init__(self, symbol: str, binance_client: BinanceClient, order_book: OrderBook, monitor: Monitor):
        self.symbol = symbol
        self.binance_client = binance_client
        self.order_book = order_book
        self.monitor = monitor
        self.state = SyncState.BUFFERING
        self._queue: "asyncio.Queue[UpdateEvent]" = asyncio.Queue()

    async def run(self) -> None:
        reader_task = asyncio.create_task(self._reader())
        try:
            while True:
                await self._resync()
                while self.state == SyncState.SYNCED:
                    event = await self._queue.get()
                    if self._is_gap(event):
                        self.monitor.record_gap()
                        self.state = SyncState.BUFFERING
                    else:
                        self.order_book.apply_diff_event(event)
                        self.monitor.record_event(event)
        finally:
            reader_task.cancel()

    async def _reader(self) -> None:
        while True:
            try:
                async for event in self.binance_client.stream_diff_events():
                    await self._queue.put(event)
            except Exception:
                pass
            self.state = SyncState.BUFFERING

    async def _resync(self) -> None:
        self.monitor.record_resync()
        self.state = SyncState.SYNCING

        snapshot = await self.binance_client.fetch_snapshot()
        event = await self._queue.get()

        while True:
            if event.final_update_id <= snapshot.last_update_id:
                event = await self._queue.get()
                continue
            if event.first_update_id <= snapshot.last_update_id + 1:
                break
            snapshot = await self.binance_client.fetch_snapshot() # event.first_update_id > snapshot.last_update_id + 1

        self.order_book.apply_snapshot(snapshot)
        self.order_book.apply_diff_event(event)
        self.monitor.record_event(event)

        self.state = SyncState.SYNCED

    def _is_gap(self, event: UpdateEvent) -> bool:
        return event.first_update_id != self.order_book.last_update_id + 1
