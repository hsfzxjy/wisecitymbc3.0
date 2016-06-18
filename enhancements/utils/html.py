from bs4 import BeautifulSoup
import html2text, re

from enhancements.models.mixins import AutoCleanMixin

INVALID_TAGS = ['script', 'iframe']


def standardize(html):

    soup = BeautifulSoup(html, "html.parser")

    for element in soup.findAll(True):
        if element.name in INVALID_TAGS:
            element.extract()

    return str(soup)


def filter_html_mixin(field_names):

    class FilterHtmlMixin(AutoCleanMixin):

        def _clean_html(self):
            for field_name in field_names:
                setattr(self, field_name, standardize(
                    getattr(self, field_name)))

        def clean(self):
            self._clean_html()

            return super(FilterHtmlMixin, self).clean()

    return FilterHtmlMixin


def summarize(html):
    parser = html2text.HTML2Text()

    text = re.sub(r'\n{2,}', '\n', parser.handle(html))

    lines = text.split('\n')

    return '\n'.join(lines[:20])
