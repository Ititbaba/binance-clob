from decimal import Decimal, InvalidOperation
from typing import List

from schemas.market_data import PriceLevel, Snapshot, UpdateEvent


class MessageParseError(Exception):
    pass


class Parser:
    @staticmethod
    def _parse_levels(raw_levels: list) -> List[PriceLevel]:
        levels = []
        for raw_level in raw_levels:
            try:
                price_str, qty_str = raw_level
                levels.append(PriceLevel(price=Decimal(price_str), quantity=Decimal(qty_str)))
            except (ValueError, InvalidOperation, TypeError) as error:
                raise MessageParseError(f"invalid price level: {raw_level}")
        return levels

    @staticmethod
    def parse_snapshot(raw_snapshot: dict) -> Snapshot:
        try:
            return Snapshot(
                last_update_id=raw_snapshot["lastUpdateId"],
                bids=Parser._parse_levels(raw_snapshot["bids"]),
                asks=Parser._parse_levels(raw_snapshot["asks"]),
            )
        except KeyError as error:
            raise MessageParseError(f"missing field in snapshot: {error}")

    @staticmethod
    def parse_diff_event(raw_event: dict) -> UpdateEvent:
        if raw_event.get("e") != "depthUpdate":
            raise MessageParseError(f"unexpected event type: {raw_event.get('e')!r}")
        try:
            return UpdateEvent(
                symbol=raw_event["s"],
                event_time=raw_event["E"],
                first_update_id=raw_event["U"],
                final_update_id=raw_event["u"],
                bids=Parser._parse_levels(raw_event["b"]),
                asks=Parser._parse_levels(raw_event["a"]),
            )
        except KeyError as error:
            raise MessageParseError(f"missing field in diff event: {error}")
