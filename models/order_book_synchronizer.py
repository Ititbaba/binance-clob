from enum import Enum, auto

from logger import get_logger
from models.binance_client import BinanceClient
from models.event_queue import EventQueue
from models.monitor import Monitor
from models.order_book import OrderBook
from schemas.market_data import Snapshot, UpdateEvent

logger = get_logger(__name__)

class SyncState(Enum):
    BUFFERING = auto()
    SYNCING = auto()
    SYNCED = auto()


class OrderBookSynchronizer:
    def __init__(
        self,
        symbol: str,
        binance_client: BinanceClient,
        order_book: OrderBook,
        queue: EventQueue,
        monitor: Monitor,
    ):
        self.symbol = symbol
        self.binance_client = binance_client
        self.order_book = order_book
        self.monitor = monitor
        self.state = SyncState.BUFFERING
        self._queue = queue

    async def run(self) -> None:
        while True:
            await self._resync()
            while self.state == SyncState.SYNCED:
                event = await self._queue.get()
                if self._is_gap(event):
                    self.monitor.record_gap_detected()
                    self.state = SyncState.BUFFERING
                else:
                    self.order_book.apply_diff_event(event)
                    self.monitor.record_event_applied()

    async def _resync(self) -> None:
        self.monitor.record_resync_started()
        self.state = SyncState.SYNCING

        snapshot = await self._fetch_snapshot()
        event = await self._queue.get()

        while True:
            if event.final_update_id <= snapshot.last_update_id:
                event = await self._queue.get()
                continue
            if event.first_update_id <= snapshot.last_update_id + 1:
                break
            snapshot = await self._fetch_snapshot()  # event.first_update_id > snapshot.last_update_id + 1

        self.order_book.apply_snapshot(snapshot)
        self.order_book.apply_diff_event(event)
        self.monitor.record_event_applied()

        self.state = SyncState.SYNCED
        self.monitor.record_resync_succeeded()

    async def _fetch_snapshot(self) -> Snapshot:
        while True:
            try:
                return await self.binance_client.fetch_snapshot()
            except Exception as error:
                logger.warning("Failed to fetch snapshot: %s", error)
                self.monitor.record_snapshot_fetch_error()

    def _is_gap(self, event: UpdateEvent) -> bool:
        return event.first_update_id != self.order_book.last_update_id + 1
