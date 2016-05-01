import re

from django.utils.encoding import force_text

re_expression = re.compile(r'{{(.*?)}}')


def extract_variables(template, **kwargs):
    expressions = re_expression.findall(template)
    return {
        exp: eval(exp, {}, kwargs)
        for exp in expressions
    }


def render(template, context):

    return re_expression.sub(
        lambda match_object:
            force_text(context.get(match_object.groups()[0])),
        template
    )
