import rules

from accounts import rules as account_rules

from .models import Reply, Topic


@rules.predicate
def is_my_topic(user, obj):
    if obj is None:
        return False

    if isinstance(obj, Topic):
        topic = obj
    elif isinstance(obj, Reply):
        topic = obj.topic
    else:
        return False

    return topic is not None and topic.asker.id == user.id

is_my_topic = account_rules.is_authenticated & is_my_topic


@rules.predicate
def is_my_reply(user, reply):
    return reply is not None and reply.author.id == user.id

is_my_topic_or_government = account_rules.is_authenticated & \
    (is_my_topic | account_rules.is_government)
is_government_or_company = account_rules.logined_and_government & \
    account_rules.logined_and_company


# registration
rules.add_perm('questions', account_rules.logined_and_government)

rules.add_perm('questions.add_topic', account_rules.logined_and_company)
rules.add_perm('questions.change_topic', is_my_topic_or_government)
rules.add_perm('questions.delete_topic', is_my_topic_or_government)
rules.add_perm('questions.view_topic', is_my_topic_or_government)

rules.add_perm('questions.add_reply', account_rules.is_my_topic_or_government)
rules.add_perm('questions.change_reply', rules.always_deny)
rules.add_perm('questions.delete_reply',
               account_rules.is_my_topic_or_government)
rules.add_perm('questions.view_reply', is_my_topic_or_government)
