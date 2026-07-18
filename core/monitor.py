import asyncio
import time
from dataclasses import dataclass
from typing import Optional

from core.event_queue import EventQueue
from utils.logger import get_logger

logger = get_logger(__name__)


@dataclass
class Metrics:
    events_received: int = 0
    events_applied: int = 0
    gaps_detected: int = 0
    resyncs_started: int = 0
    resyncs_succeeded: int = 0
    reader_errors: int = 0
    snapshot_fetch_errors: int = 0
    current_queue_size: int = 0
    last_event_received_at: Optional[float] = None
    last_successful_sync_at: Optional[float] = None


class Monitor:
    def __init__(self):
        self.metrics = Metrics()

    def record_event_received(self) -> None:
        self.metrics.events_received += 1
        self.metrics.last_event_received_at = time.time()

    def record_event_applied(self) -> None:
        self.metrics.events_applied += 1

    def record_gap_detected(self) -> None:
        self.metrics.gaps_detected += 1

    def record_resync_started(self) -> None:
        self.metrics.resyncs_started += 1

    def record_resync_succeeded(self) -> None:
        self.metrics.resyncs_succeeded += 1
        self.metrics.last_successful_sync_at = time.time()

    def record_reader_error(self) -> None:
        self.metrics.reader_errors += 1

    def record_snapshot_fetch_error(self) -> None:
        self.metrics.snapshot_fetch_errors += 1

    def _sample_queue_size(self, queue: EventQueue) -> None:
        size = queue.queue_size()
        self.metrics.current_queue_size = size

    async def run(self, queue: EventQueue, interval_seconds: float = 10.0) -> None:
        while True:
            await asyncio.sleep(interval_seconds)
            self._sample_queue_size(queue)
            logger.info(
                "events_received=%s events_applied=%s gaps_detected=%s "
                "resyncs_started=%s resyncs_succeeded=%s reader_errors=%s "
                "snapshot_fetch_errors=%s current_queue_size=%s "
                "last_event_received_at=%s last_successful_sync_at=%s",
                self.metrics.events_received,
                self.metrics.events_applied,
                self.metrics.gaps_detected,
                self.metrics.resyncs_started,
                self.metrics.resyncs_succeeded,
                self.metrics.reader_errors,
                self.metrics.snapshot_fetch_errors,
                self.metrics.current_queue_size,
                self.metrics.last_event_received_at,
                self.metrics.last_successful_sync_at,
            )
