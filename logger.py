# logger.py - Logging Setup
# ------------------------
# This module provides a standard logging setup for the modular app.
# Logs are written to both a rotating file and the console.
# Logging is initialized at app startup.

import logging
from logging.handlers import RotatingFileHandler
import os

def setup_logging(log_dir='logs', log_file='app.log'):
    """
    Set up logging for the app.
    Logs go to both a rotating file and the console.
    Args:
        log_dir (str): Directory for log files
        log_file (str): Log file name
    """
    os.makedirs(log_dir, exist_ok=True)
    log_path = os.path.join(log_dir, log_file)
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)

    # File handler (rotating): keeps up to 5 files, 2MB each
    file_handler = RotatingFileHandler(log_path, maxBytes=2*1024*1024, backupCount=5)
    file_formatter = logging.Formatter('[%(asctime)s] %(levelname)s %(name)s: %(message)s')
    file_handler.setFormatter(file_formatter)
    logger.addHandler(file_handler)

    # Console handler: outputs to terminal/Streamlit logs
    console_handler = logging.StreamHandler()
    console_formatter = logging.Formatter('%(levelname)s: %(message)s')
    console_handler.setFormatter(console_formatter)
    logger.addHandler(console_handler)

    logger.info('Logging is set up. Logs will be written to %s', log_path) 