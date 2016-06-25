from pprint import pprint


def print_urls():
    from django.core.urlresolvers import get_resolver
    pprint(list(get_resolver(None).reverse_dict.items()))
