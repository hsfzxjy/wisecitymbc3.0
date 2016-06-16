import rules
from rules import always_true, always_false

rules.add_perm('files', always_true)
rules.add_perm('files.add_file', always_true)
rules.add_perm('files.change_file', always_false)
rules.add_perm('files.delete_file', always_true)
