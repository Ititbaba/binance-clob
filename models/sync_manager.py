from enum import Enum, auto

from models.binance_client import BinanceClient
from models.monitoring import Monitor
from models.order_book import OrderBook
from schemas.market_data import UpdateEvent


class SyncState(Enum):
    BUFFERING = auto()
    SYNCING = auto()
    SYNCED = auto()


class SyncManager:
    def __init__(self, symbol: str, binance_client: BinanceClient, order_book: OrderBook, monitor: Monitor):
        self.symbol = symbol
        self.binance_client = binance_client
        self.order_book = order_book
        self.monitor = monitor
        self.state = SyncState.BUFFERING
        self._buffer: list[UpdateEvent] = []

    async def run(self) -> None:
        self.binance_client.stream_diffs

    async def _resync(self) -> None:
        pass

    def _is_gap(self, event: UpdateEvent) -> bool:
        pass
