from dataclasses import dataclass
from datetime import datetime

from logger.levels import LogLevel


@dataclass(frozen=True)
class LogRecord:
    timestamp: datetime
    level: LogLevel
    logger_name: str
    message: str

