import logging

# Lambda logging config
logger = logging.getLogger()

# Comment out the below section for lambda deployment

#--- Start section
logger = logging.getLogger('email-sender')
hdlr = logging.FileHandler('emailsender.log')
formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
hdlr.setFormatter(formatter)
logger.addHandler(hdlr)
#--- End Section

logger.setLevel(logging.DEBUG)


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
