from enhancements.entries import BaseListEntries, BaseDictEntries
from django.test import TestCase


class ListEntries(BaseListEntries):

    pass


class ListEntriesTestCase(TestCase):

    def test_register_and_unregister(self):
        (list_entries, list_register,
            list_unregister, list_exists) = ListEntries.expose()
        list_register('item')
        self.assertTrue(list_exists('item'))

        try:
            list_register('item')
        except KeyError:
            pass
        else:
            self.fail('It should raise error when registering'
                      'duplicated entries.')

        list_unregister('item')
        self.assertFalse(list_exists('item'))


class DictEntries(BaseDictEntries):

    pass


class DictEntriesTestCase(TestCase):

    def test_register_and_unregister(self):
        (dict_entries, dict_register,
            dict_unregister, dict_exists,
            dict_get_value) = DictEntries.expose()
        dict_register('key', 'value')
        self.assertTrue(dict_exists('key'))
        self.assertEqual(dict_get_value('key'), 'value')

        try:
            dict_register('key', 'value')
        except KeyError:
            pass
        else:
            self.fail('It should raise error when registering'
                      'duplicated entries.')

        dict_unregister('key')
        self.assertFalse(dict_exists('key'))
