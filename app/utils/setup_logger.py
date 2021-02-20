import logging


def init_logger(log_file_path: str = None):
    logging.basicConfig(filename=log_file_path, level=logging.INFO,
                        format="[%(asctime)s] p%(process)s {%(filename)s:"
                               "%(lineno)d} %(message)s")
    logger = logging.getLogger(__name__)
    return logger
