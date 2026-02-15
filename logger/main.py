from __future__ import annotations

import os
import sys

if __package__ is None or __package__ == "":
    current_dir = os.path.dirname(os.path.abspath(__file__))
    parent_dir = os.path.dirname(current_dir)
    if parent_dir not in sys.path:
        sys.path.insert(0, parent_dir)

from logger.appenders import ConsoleAppender, FileAppender
from logger.dispatchers import LevelRouterDispatcher
from logger.levels import LogLevel
from logger.logger import Logger


def main() -> None:
    base_dir = os.path.dirname(__file__)
    file_nmae = os.path.join(base_dir, 'app.log')

    console = ConsoleAppender(min_level=LogLevel.TRACE)
    info_appender = FileAppender(file_path=file_nmae, min_level=LogLevel.INFO)
    debug_appender = FileAppender(file_path=file_nmae, min_level=LogLevel.DEBUG)
    error_appender = FileAppender(file_path=file_nmae, min_level=LogLevel.ERROR)

    router = LevelRouterDispatcher(
        routes={
            LogLevel.TRACE: [console],
            LogLevel.DEBUG: [console, debug_appender],
            LogLevel.INFO: [console, info_appender],
            LogLevel.WARN: [console, info_appender],
            LogLevel.ERROR: [console, error_appender],
        },
        fallback_appenders=[console],
    )

    app_logger = Logger(name="PaymentService", dispatcher=router, min_level=LogLevel.TRACE)

    app_logger.trace("trace: request entered service")
    app_logger.debug("debug: validating payload")
    app_logger.info("info: payment accepted")
    app_logger.warn("warn: retrying downstream API")
    app_logger.error("error: downstream timeout")

    print(f"Info/Warn logs: {file_nmae}")
    print(f"Debug logs: {file_nmae}")
    print(f"Error logs: {file_nmae}")


if __name__ == "__main__":
    main()
