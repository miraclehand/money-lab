from pymodm import connect
from yp_fin_utils.config.settings import get_env_var


def setup_mongodb_connection(mongo_base_uri=None, connection_alias=None):
    mongo_base_uri = mongo_base_uri or get_env_var('MONGO_BASE_URI')
    connection_alias = connection_alias or get_env_var('STOCKDB_ALIAS')
    mongo_uri = f"{mongo_base_uri}/{connection_alias}"

    connect(mongo_uri, alias=connection_alias, connect=False)

