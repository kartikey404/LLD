from datetime import datetime

from logger.dispatchers import FanOutDispatcher, LogDispatcher
from logger.levels import LogLevel
from logger.record import LogRecord


class Logger:
    def __init__(
        self,
        name: str,
        dispatcher: LogDispatcher | None = None,
        min_level: LogLevel = LogLevel.TRACE,
    ) -> None:
        self.name = name
        self.dispatcher = dispatcher or FanOutDispatcher([])
        self.min_level = min_level

    def log(self, level: LogLevel, message: str) -> None:
        if level < self.min_level:
            return
        record = LogRecord(
            timestamp=datetime.now(),
            level=level,
            logger_name=self.name,
            message=message,
        )
        self.dispatcher.dispatch(record)

    def trace(self, message: str) -> None:
        self.log(LogLevel.TRACE, message)

    def debug(self, message: str) -> None:
        self.log(LogLevel.DEBUG, message)

    def info(self, message: str) -> None:
        self.log(LogLevel.INFO, message)

    def warn(self, message: str) -> None:
        self.log(LogLevel.WARN, message)

    def error(self, message: str) -> None:
        self.log(LogLevel.ERROR, message)
