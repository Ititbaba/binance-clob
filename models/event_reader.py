import asyncio

from models.binance_client import BinanceClient
from schemas.market_data import UpdateEvent


class EventReader:
    def __init__(self, binance_client: BinanceClient):
        self.binance_client = binance_client
        self.queue: "asyncio.Queue[UpdateEvent]" = asyncio.Queue()

    async def run(self) -> None:
        while True:
            try:
                async for event in self.binance_client.stream_diff_events():
                    await self.queue.put(event)
            except Exception:
                pass
