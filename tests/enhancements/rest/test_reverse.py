from django.test import SimpleTestCase


class ReverseTestCase(SimpleTestCase):

    def test_reverse(self):
        from enhancements.rest.reverse import safe_reverse

        self.assertEqual(safe_reverse('not-exists', default='/404/'), '/404/')
