from __future__ import annotations

from abc import ABC, abstractmethod

from logger.appenders import LogAppender
from logger.levels import LogLevel
from logger.record import LogRecord


class LogDispatcher(ABC):
    @abstractmethod
    def dispatch(self, record: LogRecord) -> None:
        raise NotImplementedError


class FanOutDispatcher(LogDispatcher):
    def __init__(self, appenders: list[LogAppender]) -> None:
        self.appenders = appenders

    def dispatch(self, record: LogRecord) -> None:
        for appender in self.appenders:
            appender.append(record)


class LevelRouterDispatcher(LogDispatcher):
    def __init__(
        self,
        routes: dict[LogLevel, list[LogAppender]],
        fallback_appenders: list[LogAppender] | None = None,
    ) -> None:
        self.routes = routes
        self.fallback_appenders = fallback_appenders or []

    def dispatch(self, record: LogRecord) -> None:
        appenders = self.routes.get(record.level, self.fallback_appenders)
        for appender in appenders:
            appender.append(record)

