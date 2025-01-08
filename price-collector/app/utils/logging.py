import logging
import datetime
from logging.handlers import RotatingFileHandler


def configure_logging():
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)

    file_handler = RotatingFileHandler("data/logs/app.log", maxBytes=1024 * 1024, backupCount=3)
    file_handler.setLevel(logging.INFO)

    formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    console_handler.setFormatter(formatter)
    file_handler.setFormatter(formatter)

    logging.basicConfig(level=logging.INFO, handlers=[console_handler, file_handler])

    utc_offset = datetime.timedelta(hours=9)
    local_tz = datetime.timezone(utc_offset, name='Asia/Seoul')
    logging.Formatter.converter = lambda *args: datetime.datetime.now(local_tz).timetuple()
