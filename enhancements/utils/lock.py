from collections import defaultdict
from functools import wraps


class pass_if_locked(object):
    """
    Decorator for signal receivers.
    """

    def __init__(self, lock_name, unlock=True):
        self.__lock_name = lock_name
        self.__unlock = unlock

    def __call__(self, func):

        @wraps(func)
        def inner(sender, instance, *args, **kwargs):
            lock = instance.locks[self.__lock_name]
            if lock.is_locked:
                lock.unlock()
                return

            return func(sender, instance, *args, **kwargs)

        return inner


class Lock(object):

    def __init__(self):
        self.__locked = False

    def lock(self):
        self.__locked = True

    def unlock(self):
        self.__locked = False

    @property
    def is_locked(self):
        return self.__locked


class LockMixin(object):

    def __init__(self, *args, **kwargs):
        self.locks = defaultdict(Lock)

        return super(LockMixin, self).__init__(*args, **kwargs)
