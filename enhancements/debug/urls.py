def print_urls():
    from django.core.urlresolvers import get_resolver
    print(list(get_resolver(None).reverse_dict.items()))
