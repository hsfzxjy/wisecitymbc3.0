from django.core.urlresolvers import NoReverseMatch

from rest_framework.reverse import reverse

import warnings


def safe_reverse(viewname, default='', *args, **extra):
    """
    When not matched, this function will return the
    URL indicating by `default` and print out a warning
    instead of raising an error.
    """

    try:
        return reverse(viewname, *args, **extra)
    except NoReverseMatch:
        warnings.warn('Reverse %r not matched.' %
                      viewname, RuntimeWarning)

        return default
