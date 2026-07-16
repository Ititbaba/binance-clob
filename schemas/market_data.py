from dataclasses import dataclass
from decimal import Decimal
from typing import List


@dataclass(frozen=True)
class PriceLevel:
    price: Decimal
    quantity: Decimal


@dataclass(frozen=True)
class Snapshot:
    last_update_id: int
    bids: List[PriceLevel]
    asks: List[PriceLevel]


@dataclass(frozen=True)
class UpdateEvent:
    symbol: str
    event_time: int
    first_update_id: int
    final_update_id: int
    bids: List[PriceLevel]
    asks: List[PriceLevel]
