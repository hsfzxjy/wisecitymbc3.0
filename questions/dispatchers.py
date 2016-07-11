from notifications import registry
from notifications.dispatch import Sender

from django.utils.translation import ugettext_noop as _


registry.register('questions')

notifier = Sender({
    'create_topic': _("{{target.asker.nickname}} asks a question "
                      "[{{target.title}}]({{url}}). "),
    'update_topic': _("{{target.asker.nickname}} updates the question "
                      "[{{target.title}}]({{url}}). "),
    "open_topic": _("{{target.asker.nickname}} opens the question "
                    "[{{target.title}}]({{url}}). "),
    "close_topic": _("{{target.asker.nickname}} closes the question "
                     "[{{target.title}}]({{url}}). "),
    'create_reply': _("{{target.author.nickname}} posts a"
                      " reply on [{{target.topic.title}}]({{url}})."),
}, module='questions')
