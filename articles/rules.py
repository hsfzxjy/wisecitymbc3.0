import rules
from rules import is_authenticated

from . import consts
from accounts.rules import logined_and_government


@rules.predicate
def is_my_article(user, article):
    return article is None or user.id == article.author.id


@rules.predicate
def can_add_article(user):
    return is_authenticated(user) and \
        consts.ArticleType.from_user(user) is not None

logined_and_my_article = is_authenticated & is_my_article

rules.add_perm('articles', logined_and_government)
rules.add_perm('articles.view_article', rules.always_true)
rules.add_perm('articles.add_article', can_add_article)
rules.add_perm('articles.change_article',
               logined_and_government | logined_and_my_article)
rules.add_perm('articles.delete_article',
               logined_and_government | logined_and_my_article)

for action in ['view', 'add', 'change', 'delete']:
    rules.add_perm('articles.%s_tag' % action, rules.always_true)
