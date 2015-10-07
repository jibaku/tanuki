from django.test import TestCase
from django.core.exceptions import ValidationError

from survey.utils import validate_list
from survey.utils import get_choices


class UtilsTestCase(TestCase):

    def test_validate_list(self):
        self.assertEqual(validate_list("1,2"), None)
        self.assertEqual(validate_list("1,2,3"), None)
        with self.assertRaises(ValidationError):
            validate_list("1")

    def test_get_choices(self):
        self.assertEqual(
            get_choices("1,2"),
            (('1', '1'), ('2', '2'))
        )
        self.assertEqual(
            get_choices("a,b"),
            (('a', 'a'), ('b', 'b'))
        )
