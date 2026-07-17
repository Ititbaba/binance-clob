import asyncio
from enum import Enum, auto

from models.binance_client import BinanceClient
from models.order_book import OrderBook
from schemas.market_data import UpdateEvent


class SyncState(Enum):
    BUFFERING = auto()
    SYNCING = auto()
    SYNCED = auto()


class OrderBookSynchronizer:
    """Owns snapshot sync, bridging, gap detection, and update application.
    No knowledge of WebSocket connections - just consumes UpdateEvents from
    a queue supplied by the caller."""

    def __init__(
        self,
        symbol: str,
        binance_client: BinanceClient,
        order_book: OrderBook,
        queue: "asyncio.Queue[UpdateEvent]",
    ):
        self.symbol = symbol
        self.binance_client = binance_client
        self.order_book = order_book
        self.state = SyncState.BUFFERING
        self._queue = queue

    async def run(self) -> None:
        while True:
            await self._resync()
            while self.state == SyncState.SYNCED:
                event = await self._queue.get()
                if self._is_gap(event):
                    self.state = SyncState.BUFFERING
                else:
                    self.order_book.apply_diff_event(event)

    async def _resync(self) -> None:
        self.state = SyncState.SYNCING

        snapshot = await self.binance_client.fetch_snapshot()
        event = await self._queue.get()

        while True:
            if event.final_update_id <= snapshot.last_update_id:
                event = await self._queue.get()
                continue
            if event.first_update_id <= snapshot.last_update_id + 1:
                break
            snapshot = await self.binance_client.fetch_snapshot()  # event.first_update_id > snapshot.last_update_id + 1

        self.order_book.apply_snapshot(snapshot)
        self.order_book.apply_diff_event(event)

        self.state = SyncState.SYNCED

    def _is_gap(self, event: UpdateEvent) -> bool:
        return event.first_update_id != self.order_book.last_update_id + 1
