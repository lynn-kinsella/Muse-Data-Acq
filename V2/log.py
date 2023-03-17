import logging

def configure_logger(logger, filename=None):
    file_handler = logging.FileHandler(filename, mode='w')
    stream_handler = logging.StreamHandler()
    formatter = logging.Formatter('%(levelname)s: %(message)s')

    file_handler.setFormatter(formatter)
    stream_handler.setFormatter(formatter)

    logger.setLevel(logging.DEBUG)
    logger.addHandler(file_handler)
    logger.addHandler(stream_handler)
