# core/logger.py

import logging
import os

LOG_DIR = "logs"
os.makedirs(LOG_DIR, exist_ok=True)

def log_event(message, level="INFO"):
    from datetime import datetime
    with open("system_log.txt", "a") as f:
        f.write(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} [{level}] {message}\n")

def get_logger(name):
    logger = logging.getLogger(name)
    if logger.hasHandlers():
        return logger

    logger.setLevel(logging.DEBUG)

    # File handler
    fh = logging.FileHandler(f"{LOG_DIR}/{name}.log")
    fh.setLevel(logging.DEBUG)

    # Console handler
    ch = logging.StreamHandler()
    ch.setLevel(logging.INFO)

    # Formatter
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    fh.setFormatter(formatter)
    ch.setFormatter(formatter)

    # Add handlers
    logger.addHandler(fh)
    logger.addHandler(ch)

    return logger