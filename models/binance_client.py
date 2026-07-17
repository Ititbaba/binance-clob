import json
from typing import AsyncIterator

import httpx
import websockets

from config import settings
from models.parser import MessageParseError, Parser
from schemas.market_data import Snapshot, UpdateEvent


class BinanceClient:
    def __init__(self, symbol: str):
        self.symbol = symbol

    async def fetch_snapshot(self) -> Snapshot:
        async with httpx.AsyncClient() as client:
            response = await client.get(
                settings.binance_rest_url,
                params={"symbol": self.symbol.upper(), "limit": settings.binance_depth_limit},
                timeout=10,
            )
        response.raise_for_status()
        return Parser.parse_snapshot(response.json())

    async def stream_diff_events(self) -> AsyncIterator[UpdateEvent]:
        url = f"{settings.binance_ws_base_url}/{self.symbol.lower()}@depth"
        async with websockets.connect(url) as ws:
            async for raw_event in ws:
                try:
                    event = Parser.parse_diff_event(json.loads(raw_event))
                except (json.JSONDecodeError, MessageParseError):
                    continue
                yield event
