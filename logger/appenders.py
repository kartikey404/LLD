from __future__ import annotations

from abc import ABC, abstractmethod
import threading

from logger.formatter import LogFormatter
from logger.levels import LogLevel
from logger.record import LogRecord


class LogAppender(ABC):
    def __init__(self, min_level: LogLevel = LogLevel.TRACE, formatter: LogFormatter | None = None) -> None:
        self.min_level = min_level
        self.formatter = formatter or LogFormatter()
        self._lock = threading.Lock()

    def append(self, record: LogRecord) -> None:
        if record.level < self.min_level:
            return
        output = self.formatter.format(record)
        with self._lock:
            self._write(output)

    @abstractmethod
    def _write(self, output: str) -> None:
        raise NotImplementedError


class ConsoleAppender(LogAppender):
    def _write(self, output: str) -> None:
        print(output)


class FileAppender(LogAppender):
    def __init__(
        self,
        file_path: str,
        min_level: LogLevel = LogLevel.TRACE,
        formatter: LogFormatter | None = None,
    ) -> None:
        super().__init__(min_level=min_level, formatter=formatter)
        self.file_path = file_path

    def _write(self, output: str) -> None:
        with open(self.file_path, "a", encoding="utf-8") as file:
            file.write(output + "\n")
