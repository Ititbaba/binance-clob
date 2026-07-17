import asyncio
from models.event_queue import EventQueue
from schemas.market_data import UpdateEvent


class AsyncioEventQueue(EventQueue):
    def __init__(self):
        self._queue: "asyncio.Queue[UpdateEvent]" = asyncio.Queue()

    async def put(self, event: UpdateEvent) -> None:
        await self._queue.put(event)

    async def get(self) -> UpdateEvent:
        return await self._queue.get()

    def queue_size(self) -> int:
        return self._queue.qsize()
