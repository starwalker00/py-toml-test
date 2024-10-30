import logging

logger = logging.getLogger(__name__)

def database(server, port, username):
    logger.info(f"Connecting to database at {server} on port {port}")
    logger.info(f"Username: {username}")

def aaa(param1):
    logger.info(f"Function 'aaa' called with param1: {param1}")

def bbb(param1, param3):
    logger.info(f"Function 'bbb' called with param1: {param1}, param3: {param3}")
    logger.debug(f"Function 'bbb' called with param1: {param1}, param3: {param3}")
