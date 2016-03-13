"""Test for survey.utils module."""
from django.test import TestCase
from django.core.exceptions import ValidationError

from survey.utils import validate_list
from survey.utils import get_choices


class UtilsTestCase(TestCase):
    """Test for survey.utils functions."""

    def test_validate_list(self):
        """Test validate_list function."""
        self.assertEqual(validate_list("1,2"), None)
        self.assertEqual(validate_list("1,2,3"), None)
        self.assertEqual(validate_list("1;2;3", separator=';'), None)
        with self.assertRaises(ValidationError):
            validate_list("1")
        with self.assertRaises(ValidationError):
            validate_list("1", separator=';')

    def test_get_choices(self):
        """Test get_choices function."""
        self.assertEqual(
            get_choices("1,2"),
            (('1', '1'), ('2', '2'))
        )
        self.assertEqual(
            get_choices("a,b"),
            (('a', 'a'), ('b', 'b'))
        )
        self.assertEqual(
            get_choices("1;2", separator=";"),
            (('1', '1'), ('2', '2'))
        )
