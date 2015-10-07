from django.core.exceptions import ValidationError


def validate_list(value):
    """
    takes a text value and verifies that there is at least one comma
    """
    values = value.split(',')
    if len(values) < 2:
        raise ValidationError("The selected field requires an associated list of choices. Choices must contain more than one item.")


def get_choices(value):
    """
    Parse the choices and return a tuple formatted appropriately for the
    'choices' argument of a form widget.
    """
    choices = value.split(',')
    choices_list = []
    for c in choices:
        c = c.strip()
        choices_list.append((c,c))
    choices_tuple = tuple(choices_list)
    return choices_tuple
