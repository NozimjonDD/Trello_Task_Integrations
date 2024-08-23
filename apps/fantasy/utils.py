import secrets
import string


def generate_league_invite_code(length=6):
    chars = string.ascii_uppercase + string.digits

    code = "".join(secrets.choice(chars) for _ in range(length))
    return code
