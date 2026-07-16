from decimal import Decimal
from typing import Optional, Tuple

from bintrees import RBTree
from schemas.market_data import Snapshot, UpdateEvent


class OrderBook:
    def __init__(self, symbol: str):
        self.symbol = symbol
        self.bids = RBTree()
        self.asks = RBTree()
        self.last_update_id: int = 0

    def apply_snapshot(self, snapshot: Snapshot) -> None:
        raise NotImplementedError

    def apply_diff(self, event: UpdateEvent) -> None:
        raise NotImplementedError

    def best_bid(self) -> Optional[Tuple[Decimal, Decimal]]:
        raise NotImplementedError

    def best_ask(self) -> Optional[Tuple[Decimal, Decimal]]:
        raise NotImplementedError
