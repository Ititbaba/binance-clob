import json
from decimal import Decimal
from typing import Optional, Tuple

from bintrees import RBTree
from schemas.market_data import PriceLevel, Snapshot, UpdateEvent


class OrderBook:
    def __init__(self, symbol: str):
        self.symbol = symbol
        self.bids = RBTree()
        self.asks = RBTree()
        self.last_update_id: int = 0

    def apply_snapshot(self, snapshot: Snapshot) -> None:
        self.bids.clear()
        self.asks.clear()
        for level in snapshot.bids:
            self._apply_level(self.bids, level)
        for level in snapshot.asks:
            self._apply_level(self.asks, level)
        self.last_update_id = snapshot.last_update_id

    def apply_diff_event(self, event: UpdateEvent) -> None:
        for level in event.bids:
            self._apply_level(self.bids, level)
        for level in event.asks:
            self._apply_level(self.asks, level)
        self.last_update_id = event.final_update_id

    @staticmethod
    def _apply_level(tree: RBTree, level: PriceLevel) -> None:
        if level.quantity == 0:
            try:
                tree.remove(level.price)
            except KeyError:
                pass
        else:
            tree.insert(level.price, level.quantity)

    def best_bid(self) -> Optional[Tuple[Decimal, Decimal]]:
        return self.bids.max_item() if self.bids else None

    def best_ask(self) -> Optional[Tuple[Decimal, Decimal]]:
        return self.asks.min_item() if self.asks else None

    def to_json(self, depth: int = 10) -> str:
        bids = list(reversed(list(self.bids.items())))[:depth]
        asks = list(self.asks.items())[:depth]

        return json.dumps(
            {
                "lastUpdateId": self.last_update_id,
                "bids": [[str(price), str(quantity)] for price, quantity in bids],
                "asks": [[str(price), str(quantity)] for price, quantity in asks],
            },
            indent=2,
        )
