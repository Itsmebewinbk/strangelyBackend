import logging
import os


def get_logger(appname: str) -> logging.Logger:
    log_dir = os.path.abspath("./log")
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)

    logger = logging.getLogger(f"{appname}_log")
    if not logger.hasHandlers():  # Unique logger name
        logger.setLevel(logging.DEBUG)

        log_file = os.path.join(log_dir, f"{appname}.log")
        file_handler = logging.FileHandler(log_file)
        file_handler.setLevel(logging.DEBUG)
        file_formatter = logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        )
        file_handler.setFormatter(file_formatter)

        logger.addHandler(file_handler)

    return logger
