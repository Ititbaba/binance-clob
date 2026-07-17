from models.binance_client import BinanceClient
from models.event_queue import AsyncioEventQueue
from models.monitor import Monitor


class EventReader:
    def __init__(self, binance_client: BinanceClient, monitor: Monitor):
        self.binance_client = binance_client
        self.monitor = monitor
        self.queue: AsyncioEventQueue = AsyncioEventQueue()

    async def run(self) -> None:
        while True:
            try:
                async for event in self.binance_client.stream_diff_events():
                    self.monitor.record_event_received()
                    await self.queue.put(event)
            except Exception:
                self.monitor.record_reader_error()
