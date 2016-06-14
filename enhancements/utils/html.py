from bs4 import BeautifulSoup

INVALID_TAGS = ['script', 'iframe']


def standardize(html):

    soup = BeautifulSoup(html, "html.parser")

    for element in soup.findAll(True):
        if element.name in INVALID_TAGS:
            element.extract()

    return str(soup)
