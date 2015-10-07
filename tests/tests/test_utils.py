from django.test import TestCase
from django.core.exceptions import ValidationError

from survey.utils import validate_list


class UtilsTestCase(TestCase):

    def test_validate_list(self):
        self.assertEqual(validate_list("1,2"), None)
        self.assertEqual(validate_list("1,2,3"), None)
        with self.assertRaises(ValidationError):
            validate_list("1")
