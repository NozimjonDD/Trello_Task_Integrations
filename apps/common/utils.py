from django.core.validators import RegexValidator
from django.utils.translation import gettext_lazy as _

phone_number_validator = RegexValidator(
    regex=r"^\+998\d{9}$",
    message=_("Phone number must be entered in the format: '+99890 123 45 67'. Up to 13 digits allowed.")
)
formation_validator = RegexValidator(
    regex=r"^\d(-\d){1,4}$",
    message=_("Formation must be entered in the format: '4-4-2' or '5-2-2-1'. Up to 5 digits allowed.")
)


def pretty_price(price):
    if price >= 1_000_000:
        pretty_value = f'{price / 1_000_000:.1f}mln'
    elif price >= 1_000:
        pretty_value = f'{price / 1_000:.1f}k'
    else:
        pretty_value = str(price)

    return pretty_value.rstrip('0').rstrip('.') if '.' in pretty_value else pretty_value
