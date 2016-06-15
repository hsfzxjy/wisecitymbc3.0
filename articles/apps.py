from django.apps import AppConfig

from watson import search as watson


class ArticlesConfig(AppConfig):
    name = 'articles'

    def ready(self):
        watson.register(self.get_model('Article'))
