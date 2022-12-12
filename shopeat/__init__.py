import logging


def create_stream_handler(level: int):
    handler = logging.StreamHandler()
    handler.setLevel(level)
    handler.setFormatter(
        logging.Formatter("%(asctime)s -- %(levelname)-5s -- %(message)s")
    )
    return handler


def configure_logging(level: int):
    logger = logging.getLogger(__name__)
    logger.setLevel(level)
    logger.addHandler(create_stream_handler(level))


configure_logging(logging.DEBUG)
