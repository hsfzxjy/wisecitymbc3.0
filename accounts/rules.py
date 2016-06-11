import rules

from rules import is_authenticated

from . import consts


__all__ = ['is_government', 'is_bureau', 'is_company', 'is_self']


def user_type_predicate_factory(user_type):

    @rules.predicate
    def _predicate(user):
        return user.user_type == user_type

    return _predicate

is_government = user_type_predicate_factory(consts.UserType.government)
is_company = user_type_predicate_factory(consts.UserType.company)
is_bureau = user_type_predicate_factory(consts.UserType.bureau)


@rules.predicate
def is_self(user, obj):
    return obj is None or user.id == obj.id

logined_and_government = is_authenticated & is_government

government_or_self = logined_and_government | (is_authenticated & is_self)

rules.add_perm('accounts', is_government)
rules.add_perm('accounts.add_user', logined_and_government)
rules.add_perm('accounts.change_user', government_or_self)
rules.add_perm('accounts.delete_user', logined_and_government)

rules.add_perm('accounts.add_userdata', government_or_self)

rules.add_perm('accounts.view_user_data', government_or_self)
rules.add_perm('accounts.change_userdata', government_or_self)
rules.add_perm('accounts.delete_userdata', government_or_self)
