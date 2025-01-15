import os
import logging
import datetime
from logging.handlers import RotatingFileHandler


def configure_logging(log_filename):
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)

    log_dir = os.path.dirname(log_filename)
    if not os.path.exists(log_dir):
        os.makedirs(log_dir, exist_ok=True)

    file_handler = RotatingFileHandler(log_filename, maxBytes=1024 * 1024, backupCount=3)
    file_handler.setLevel(logging.INFO)

    formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    console_handler.setFormatter(formatter)
    file_handler.setFormatter(formatter)

    logging.basicConfig(level=logging.INFO, handlers=[console_handler, file_handler])

    utc_offset = datetime.timedelta(hours=9)
    local_tz = datetime.timezone(utc_offset, name='Asia/Seoul')
    logging.Formatter.converter = lambda *args: datetime.datetime.now(local_tz).timetuple()
