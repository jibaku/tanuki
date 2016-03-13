"""Utils for taniku app."""

from django.core.exceptions import ValidationError


def validate_list(value, separator=','):
    """Take a text value and verifies that there is at least one comma."""
    values = value.split(separator)
    if len(values) < 2:
        msg = "The selected field requires an associated list of choices. "
        msg += "Choices must contain more than one item."
        raise ValidationError(msg)


def get_choices(value, separator=','):
    """
    Parse the choices and return a tuple.

    The tuple is formatted appropriately for the 'choices' argument
    of a form widget.
    """
    choices = value.split(separator)
    choices_list = []
    for c in choices:
        c = c.strip()
        choices_list.append((c, c))
    choices_tuple = tuple(choices_list)
    return choices_tuple
