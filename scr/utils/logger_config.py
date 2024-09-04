import logging

def logger_config() -> logging.Logger:
    """
    Configures and returns a logger with both console and file handlers.

    The logger is configured to log messages at the INFO level. Logs are formatted to include the timestamp, log level, and message.

    Returns
    -------
    logging.Logger
        Configured logger instance.
    """
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)

    console_handler = logging.StreamHandler()
    file_handler = logging.FileHandler("app.log", mode="w", encoding="utf-8")

    formatter = logging.Formatter(
        "{asctime} | {levelname} | {message}",
        style="{",
        datefmt="%Y-%m-%d %H:%M:%S"
    )

    console_handler.setFormatter(formatter)
    file_handler.setFormatter(formatter)

    logger.addHandler(console_handler)
    logger.addHandler(file_handler)

    return logger

logger = logger_config()
