import logging

def logger_setup(name):
    """Sets up a logger to log fatal errors

    Returns:
        logging.Logger: The Logger object
    """
    logger = logging.getLogger(name)
    logger.setLevel(logging.ERROR)

    formatter = logging.Formatter(
        '\n%(name)s -> %(asctime)s : %(levelname)s : Thread = %(threadName)s : %(message)s')

    handler = logging.FileHandler('errors.log')
    handler.setFormatter(formatter)

    logger.addHandler(handler)

    return logger