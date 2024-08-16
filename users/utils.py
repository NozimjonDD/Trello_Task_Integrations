import secrets
from django.core.validators import RegexValidator
from django.utils.translation import gettext_lazy as _


def generate_otp(digits=4) -> str:
    num = secrets.randbelow(10 ** digits)
    return f"{num:0{digits}d}"


def generate_secret(length=40) -> str:
    return secrets.token_hex(length // 2)


phone_number_validator = RegexValidator(
    regex=r"^\+998\d{9}$",
    message=_("Phone number must be entered in the format: '+99890 123 45 67'. Up to 13 digits allowed.")
)
