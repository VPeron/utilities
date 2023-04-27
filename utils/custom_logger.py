import logging

def get_custom_logger(name):
    """
    Returns a custom logger with a specific name and log level.
    """
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)
    # create a stream handler to print logs to console
    handler = logging.StreamHandler()
    handler.setLevel(logging.INFO)
    # create a logging format
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)
    # add the file handler to the logger
    logger.addHandler(handler)
    return logger
