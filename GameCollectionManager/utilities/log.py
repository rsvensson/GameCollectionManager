import logging
import logging.handlers
import os
import sys

# Formatters
FILE_FORMATTER = logging.Formatter("[%(levelname)s:%(asctime)s:%(module)s]: %(message)s")

SIMPLE_FORMATTER = logging.Formatter("%(asctime)s: %(message)s")

DEBUG_FORMATTER = logging.Formatter("%(levelname)-8s %(asctime)s [%(module)s.%(funcName)s:%(lineno)s]:%(message)s")

# Log file
LOG_FILENAME = "data/log/gcm.log"
loghandler = logging.handlers.RotatingFileHandler(LOG_FILENAME, maxBytes=20971520, backupCount=3)
loghandler.setFormatter(FILE_FORMATTER)

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
logger.addHandler(loghandler)

# Set logging level to Warnings
console_handler = logging.StreamHandler(stream=sys.stdout)
console_handler.setFormatter(SIMPLE_FORMATTER)
logger.addHandler(console_handler)
logger.setLevel(logging.INFO)