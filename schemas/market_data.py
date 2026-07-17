import json
from dataclasses import dataclass
from decimal import Decimal
from typing import List


@dataclass(frozen=True)
class PriceLevel:
    price: Decimal
    quantity: Decimal

    def to_list(self) -> list:
        return [str(self.price), str(self.quantity)]

    def to_json(self) -> str:
        return json.dumps(self.to_list())


@dataclass(frozen=True)
class Snapshot:
    last_update_id: int
    bids: List[PriceLevel]
    asks: List[PriceLevel]

    def to_json(self) -> str:
        return json.dumps(
            {
                "lastUpdateId": self.last_update_id,
                "bids": [level.to_list() for level in self.bids],
                "asks": [level.to_list() for level in self.asks],
            },
            indent=2,
        )


@dataclass(frozen=True)
class UpdateEvent:
    symbol: str
    event_time: int
    first_update_id: int
    final_update_id: int
    bids: List[PriceLevel]
    asks: List[PriceLevel]

    def to_json(self) -> str:
        return json.dumps(
            {
                "e": "depthUpdate",
                "E": self.event_time,
                "s": self.symbol,
                "U": self.first_update_id,
                "u": self.final_update_id,
                "b": [level.to_list() for level in self.bids],
                "a": [level.to_list() for level in self.asks],
            },
            indent=2,
        )
