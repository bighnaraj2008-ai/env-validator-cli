"""Isolated memory-buffered logging subsystem for test runs."""

from __future__ import annotations

import io
import logging
from typing import List


class TestLogCaptureHandler(logging.Handler):
    """Captures log records into an in-memory string buffer for assertions."""

    def __init__(self) -> None:
        super().__init__()
        self.records: List[logging.LogRecord] = []
        self.stream = io.StringIO()

    def emit(self, record: logging.LogRecord) -> None:
        self.records.append(record)
        msg = self.format(record)
        self.stream.write(msg + "\n")

    def get_logs(self) -> List[str]:
        return [self.format(r) for r in self.records]

    def clear(self) -> None:
        self.records.clear()
        self.stream = io.StringIO()
