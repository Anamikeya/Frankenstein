#Blom Version 0.001

import logging
import sys

class timer:
    """
    Returns min elapsed since created.

    Print using str(timer)
    """
    from time import time

    def __init__(self):
        self.start = self.time()
        pass

    def __str__(self):
        self.end = self.time()

        self.duration = round((self.end - self.start) / 60, 2)

        return str(self.duration)


def init_logger(name, lvlstream=logging.INFO, lvlfile=logging.DEBUG):
    filename = name + ".log"

    logger = logging.getLogger(name)

    # Add two handlers, one for screen, one for file
    handler_stream = logging.StreamHandler(sys.stdout)
    handler_file = logging.FileHandler(filename)

    # Set format
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    handler_stream.setFormatter(formatter)
    handler_file.setFormatter(formatter)

    # Setting level of logging
    logger.setLevel(logging.DEBUG)
    handler_stream.setLevel(lvlstream)
    handler_file.setLevel(lvlfile)

    # Adding handlers to logger
    logger.addHandler(handler_stream)
    logger.addHandler(handler_file)

    return logger


def get_logger(name):
    logger = logging.getLogger(name)
    return logger
