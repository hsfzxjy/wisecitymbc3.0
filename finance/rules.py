import rules

from accounts.rules import logined_and_government

from .basenames import basenames

perms_map = {
    'view': rules.always_true,
    'add': logined_and_government,
    'change': logined_and_government,
    'delete': logined_and_government
}

log_perms_map = {
    'view': rules.always_true,
    'add': logined_and_government,
    'chnage': logined_and_government,
    'delete': logined_and_government,
}

rules.add_perm('finance', logined_and_government)

for name in basenames:
    for action, perm in perms_map.items():
        rules.add_perm('finance.%s_%s' % (action, name.lower()), perm)

    for action, perm in log_perms_map.items():
        rules.add_perm('finance.%s_%slog' % (action, name.lower()), perm)
