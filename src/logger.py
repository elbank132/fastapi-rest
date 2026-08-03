import logging
import sys
import os
from logging.handlers import TimedRotatingFileHandler

logger = logging.getLogger("fastapi_app")
logger.setLevel(logging.DEBUG)

formatter = logging.Formatter(
    "%(asctime)s - %(levelname)s - [%(module)s] - %(message)s"
)

console_handler = logging.StreamHandler(sys.stdout)
console_handler.setFormatter(formatter)

# 4. Configure the Timed Rotating File Handler
file_handler = TimedRotatingFileHandler(
    filename="app.log",     # The active file for today
    when="midnight",        # Rotate exactly at midnight
    interval=1,             # Every 1 day
    backupCount=30,         # Keep exactly 30 days of history, delete older
    encoding="utf-8"
)


def log_namer(default_name):
    dir_name, file_name = os.path.split(default_name)
    
    if ".log." in file_name:
        base, date_suffix = file_name.split(".log.")
        new_name = f"{base}({date_suffix}).log"
        return os.path.join(dir_name, new_name)
    return default_name

file_handler.namer = log_namer
file_handler.setFormatter(formatter)

if not logger.handlers:
    logger.addHandler(console_handler)
    logger.addHandler(file_handler)