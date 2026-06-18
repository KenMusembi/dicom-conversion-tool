import logging
import os
from datetime import datetime


def setup_logger(
    log_dir: str = "logs",
    log_name: str = "media_dicom_converter.log",
    level=logging.INFO
):
    """
    Configures application-wide logging with both console and file output.
    """

    os.makedirs(log_dir, exist_ok=True)
    log_path = os.path.join(log_dir, log_name)

    logger = logging.getLogger()
    logger.setLevel(level)

    # Prevent duplicate handlers (important in CLI runs)
    if logger.handlers:
        return logger

    # -------------------------
    # FORMATTER
    # -------------------------
    formatter = logging.Formatter(
        fmt="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    # -------------------------
    # CONSOLE HANDLER
    # -------------------------
    console_handler = logging.StreamHandler()
    console_handler.setLevel(level)
    console_handler.setFormatter(formatter)

    # -------------------------
    # FILE HANDLER
    # -------------------------
    file_handler = logging.FileHandler(log_path)
    file_handler.setLevel(level)
    file_handler.setFormatter(formatter)

    # -------------------------
    # ATTACH HANDLERS
    # -------------------------
    logger.addHandler(console_handler)
    logger.addHandler(file_handler)

    logger.info("Logger initialized")
    logger.info(f"Log file: {log_path}")

    return logger


# -----------------------------
# OPTIONAL: CONTEXTUAL LOGGER
# -----------------------------
def get_logger(name: str):
    """
    Returns a module-specific logger.
    """
    return logging.getLogger(name)