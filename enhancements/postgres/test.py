from django_nose import NoseTestSuiteRunner
from enhancements.postgres import init_zhparser


class PostgresEnhancedTestRunner(NoseTestSuiteRunner):

    def setup_databases(self, **kwargs):
        ret = super(PostgresEnhancedTestRunner, self).setup_databases(**kwargs)
        init_zhparser()

        return ret
