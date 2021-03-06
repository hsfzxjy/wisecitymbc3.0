import re
import html

from django.utils.encoding import force_text

from django.utils.translation import ugettext as _

re_expression = re.compile(r'{{(.*?)}}')


def extract_variables(template, **kwargs):
    expressions = re_expression.findall(template)
    return {
        exp: html.escape(str(eval(exp, {}, kwargs)))
        .replace('(', '&lpar;')
        .replace(')', '&rpar;')
        .replace('[', '&lsqb;')
        .replace(']', '&rsqb;')
        for exp in expressions
    }


def render(template, context):

    template = _(template)

    return re_expression.sub(
        lambda match_object:
            force_text(context.get(match_object.groups()[0])),
        template
    )
