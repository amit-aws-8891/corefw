from datetime import datetime

from corefw.loggerfw import logger

LOGGER = logger.get_logger(__name__)


def log(func):
    """
    Decorator to log entry, exit and exception of an API
    :param func:
    :return:
    """

    def wrapper(*args, **kwargs):
        start_time = datetime.utcnow().timestamp()
        try:
            LOGGER.info("Entered function : %s", func.__name__)
            return func(*args, **kwargs)
        except Exception as exception:
            LOGGER.exception(exception)
            raise
        finally:
            time_taken = datetime.utcnow().timestamp() - start_time
            LOGGER.info(
                "Exit function : %s, Time taken(s) : %d", func.__name__, time_taken
            )

    return wrapper
