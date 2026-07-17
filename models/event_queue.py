import asyncio
from abc import ABC, abstractmethod

from schemas.market_data import UpdateEvent


class EventQueue(ABC):
    @abstractmethod
    async def put(self, event: UpdateEvent) -> None: ...

    @abstractmethod
    async def get(self) -> UpdateEvent: ...


class AsyncioEventQueue:
    def __init__(self):
        self._queue: "asyncio.Queue[UpdateEvent]" = asyncio.Queue()

    async def put(self, event: UpdateEvent) -> None:
        await self._queue.put(event)

    async def get(self) -> UpdateEvent:
        return await self._queue.get()
