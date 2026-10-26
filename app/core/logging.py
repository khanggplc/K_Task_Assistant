import logging
import sys


def setup_logging(debug: bool = True) -> logging.Logger:
    level = logging.DEBUG if debug else logging.INFO
    log_format = "%(asctime)s | %(levelname)-8s | %(name)s:%(funcName)s:%(lineno)d - %(message)s"

    logging.basicConfig(
        level=level,
        format=log_format,
        handlers=[
            logging.StreamHandler(sys.stdout)
        ]
    )

    logger = logging.getLogger("ai_task_assistant")
    logger.setLevel(level)
    return logger


logger = setup_logging()
