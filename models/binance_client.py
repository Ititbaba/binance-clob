from typing import AsyncIterator

from schemas.market_data import Snapshot, UpdateEvent


class BinanceClient:
    def __init__(self, symbol: str):
        self.symbol = symbol

    def fetch_snapshot(self) -> Snapshot:
        pass

    async def stream_diffs(self) -> AsyncIterator[UpdateEvent]:
        pass
