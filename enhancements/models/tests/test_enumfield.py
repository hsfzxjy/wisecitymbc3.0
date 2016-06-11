from django.test import TestCase

from .models import ABC, Model


class EnumFieldTestCase(TestCase):

    def test_basic(self):
        Model.objects.create(test=ABC.A)

        obj = Model.objects.get(test=ABC.A)

        self.assertEqual(obj.test, ABC.A)

        obj.test = ABC.B
        obj.save()

    def test_defined_choices(self):
        from .models import ChoicesModel

    def test_default(self):
        from .models import DefaultModel

        obj = DefaultModel.objects.create()

        self.assertEqual(ABC.C, obj.test)

    def test_declared_choices(self):
        from .models import DeclaredChoicesModel, ABC2

        self.assertEqual(
            DeclaredChoicesModel._meta.get_field('test').choices,
            [
                (ABC2.A, 'ei'),
                (ABC2.B, 'bee'),
                (ABC2.C, 'sii'),
            ]
        )
