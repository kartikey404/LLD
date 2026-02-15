from logger.record import LogRecord


class LogFormatter:
    def format(self, record: LogRecord) -> str:
        time_text = record.timestamp.strftime("%Y-%m-%d %H:%M:%S")
        return f"[{time_text}] [{record.level.name}] [{record.logger_name}] {record.message}"

