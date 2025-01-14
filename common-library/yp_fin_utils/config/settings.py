import os
from dotenv import load_dotenv

load_dotenv()

def get_env_var(key, default=None):
    value = os.getenv(key, default)
    if value is None:
        raise RuntimeError(f"Missing required environment variable: {key}")
    return value

STOCKDB_ALIAS = get_env_var('STOCKDB_ALIAS')

