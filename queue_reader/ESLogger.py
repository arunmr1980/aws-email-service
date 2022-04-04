import logging

# Lambda logging config
logger = logging.getLogger()

logger.setLevel(logging.INFO)


def info(msg):
    logger.info(msg)

def debug(msg):
    logger.debug(msg)

def warn(msg):
    logger.warn(msg)

def error(msg):
    logger.error(msg)

def exception(ex):
    logger.exception(ex)
