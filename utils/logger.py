import logging
import sys


def configure_logging():
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)

    # formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')

    ch = logging.StreamHandler(sys.stdout)
    ch.setLevel(logging.INFO)
    # ch.setFormatter(formatter)

    logger.addHandler(ch)


configure_logging()
logger = logging.getLogger(__name__)