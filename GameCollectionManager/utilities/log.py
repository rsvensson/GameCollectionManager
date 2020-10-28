import logging
import logging.handlers
import os
import sys

# Formatters
SIMPLE_FORMATTER = logging.Formatter("%(asctime)s: %(message)s")
ERROR_FORMATTER = logging.Formatter("[%(levelname)s:%(asctime)s:%(module)s]: %(message)s")
DEBUG_FORMATTER = logging.Formatter("%(levelname)-8s %(asctime)s [%(module)s.%(funcName)s:%(lineno)s]:%(message)s")

# Logfiles
ERROR_LOGFILE = "data/log/error.log"
DEBUG_LOGFILE = "data/log/debug.log"
if not os.path.exists("data/log"):
    os.makedirs("data/log")
if not os.path.exists(ERROR_LOGFILE):
    with open(ERROR_LOGFILE, "w"): pass
if not os.path.exists(DEBUG_LOGFILE):
    with open(DEBUG_LOGFILE, "w"): pass

# Set up logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# Console logs
loghandler = logging.StreamHandler()
loghandler.setLevel(logging.WARNING)
loghandler.setFormatter(SIMPLE_FORMATTER)
logger.addHandler(loghandler)

# Error logs
loghandler = logging.handlers.RotatingFileHandler(ERROR_LOGFILE, maxBytes=20971520, backupCount=3)
loghandler.setLevel(logging.ERROR)
loghandler.setFormatter(ERROR_FORMATTER)
logger.addHandler(loghandler)

# Debug logs
loghandler = logging.handlers.RotatingFileHandler(DEBUG_LOGFILE, maxBytes=20971520, backupCount=3)
loghandler.setLevel(logging.INFO)
loghandler.setFormatter(DEBUG_FORMATTER)
logger.addHandler(loghandler)