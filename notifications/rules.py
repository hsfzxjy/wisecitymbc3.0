import rules


@rules.predicate
def is_my_notification(user, obj):
    return obj is None or obj.user.id == user.id

logined_and_is_mine = rules.is_authenticated & is_my_notification

rules.add_perm('notifications', rules.is_authenticated)

rules.add_perm('notifications.add_notification', rules.always_false)
rules.add_perm('notifications.change_notification', rules.always_false)
rules.add_perm('notifications.delete_notification', logined_and_is_mine)
rules.add_perm('notifications.view_notification', logined_and_is_mine)
