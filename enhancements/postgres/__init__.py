from django.db import connection
from django.db.utils import ProgrammingError, IntegrityError

from django.conf import settings

default_app_config = 'enhancements.postgres.apps.PgAppConfig'

COMMANDS = """
CREATE EXTENSION zhparser;
CREATE TEXT SEARCH CONFIGURATION {0} (PARSER = zhparser);
ALTER TEXT SEARCH CONFIGURATION {0} ADD MAPPING FOR n,v,a,i,e,l WITH simple;
""".format(getattr(settings, 'TS_CONFIG_NAME', 'chinesecfg')).split('\n')


def init_zhparser():
    cursor = connection.cursor()
    for command in COMMANDS:
        try:
            cursor.execute(command)
        except (ProgrammingError, IntegrityError):
            pass
