import logging
from logging.handlers import RotatingFileHandler


def configure_logging(logger, level, file_name, formatter, max_bytes, backup_count):
    logger.setLevel(level)
    log_file = f"{file_name}.log"
    file_handler = RotatingFileHandler(
        log_file,
        mode="w",
        maxBytes=max_bytes,
        backupCount=backup_count,
        encoding="utf-8",
    )
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)


ai_logger_formatter = logging.Formatter(
    "%(asctime)s - %(levelname)s - %(funcName)s - [AI Model: %(ai_model)s] - [Component: %(component)s] - %(message)s"
)
logger_ai = logging.getLogger("AI")
configure_logging(logger_ai, logging.INFO, "log_ai", ai_logger_formatter, 1024, 0)


database_logger_formatter = logging.Formatter(
    "%(asctime)s - %(levelname)s - %(funcName)s - [ProjectId: %(project_id)s] - [Field: %(field)s] - %(message)s"
)
logger_db = logging.getLogger("DB")
configure_logging(logger_db, logging.INFO, "log_db", database_logger_formatter, 1024, 0)


classic_logger_formatter = logging.Formatter(
    "%(asctime)s - %(levelname)s - %(funcName)s - %(message)s"
)
logger = logging.getLogger("LOGGER")
configure_logging(logger, logging.INFO, "log", classic_logger_formatter, 2048, 0)
