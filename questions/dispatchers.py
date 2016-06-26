from notifications import registry
from notifications.dispatch import Sender


registry.register('questions')

notifier = Sender({
    'create_topic': "{{target.asker.nickname}} asks a question "
    "[{{target.title}}]({{url}}). ",
    'update_topic': "{{target.asker.nickname}} updates the question "
    "[{{target.title}}]({{url}}). ",
    "open_topic": "{{target.asker.nickname}} opens the question "
    "[{{target.title}}]({{url}}). ",
    "close_topic": "{{target.asker.nickname}} closes the question "
    "[{{target.title}}]({{url}}). ",
    'create_reply': "{{target.author.nickname}} posts a"
    " reply on [{{target.topic.title}}]({{url}}).",
}, module='questions')
