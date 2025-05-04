import logging
from enum import StrEnum

LOG_FORMAT_DEBUG = "%(asctime)s:%(levelname)s:%(message)s:%(pathname)s:%(funcName)s:%(lineno)d"

class LogLevels(StrEnum):
    DEBUG = "DEBUG"
    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"
    CRITICAL = "CRITICAL"
    
def configure_logging(log_level: str = LogLevels.INFO):
    log_level = str(log_level).upper()
    log_levels = [level.value for level in LogLevels] 
    if log_level not in log_levels:
        logging.basicConfig(level=LogLevels.ERROR)
        return
    if log_level == LogLevels.DEBUG:
        logging.basicConfig(level=LogLevels.DEBUG, format=LOG_FORMAT_DEBUG)
        return
    logging.basicConfig(level=log_level)