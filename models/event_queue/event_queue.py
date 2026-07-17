from abc import ABC, abstractmethod

from schemas.market_data import UpdateEvent



class EventQueue(ABC):
    @abstractmethod
    async def put(self, event: UpdateEvent) -> None: ...

    @abstractmethod
    async def get(self) -> UpdateEvent: ...

    @abstractmethod
    def qsize(self) -> int: ...
