from pprint import pprint


def print_sql():
    from django.db import connection
    pprint(connection.queries)
