from watson.backends import PostgresSearchBackend
from django.conf import settings


class PostgresChineseSearchBackend(PostgresSearchBackend):

    search_config = getattr(settings, 'TS_CONFIG_NAME', 'chinesecfg')
