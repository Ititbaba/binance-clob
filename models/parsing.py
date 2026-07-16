from typing import List

from schemas.market_data import PriceLevel, Snapshot, UpdateEvent


class MessageParseError(Exception):
    pass


class Parser:
    @staticmethod
    def _parse_levels(raw_levels: list) -> List[PriceLevel]:
        pass

    @staticmethod
    def parse_snapshot(raw_snapshot: dict) -> Snapshot:
        pass

    @staticmethod
    def parse_diff_event(raw_event: dict) -> UpdateEvent:
        pass
