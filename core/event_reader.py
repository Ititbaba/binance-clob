from utils.logger import get_logger
from core.binance_client import BinanceClient
from core.event_queue import AsyncioEventQueue
from core.monitor import Monitor

logger = get_logger(__name__)


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
            except Exception as error:
                logger.warning("WebSocket connection failed, reconnecting: %s", error)
                self.monitor.record_reader_error()
