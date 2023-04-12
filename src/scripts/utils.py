import secrets


RANDOM_STRING_CHARS = "QWERTYUIOPASDFGHJKLZXCVBNM123456789"


def get_random_string(length=5, allowed_chars=RANDOM_STRING_CHARS):
    return "".join(secrets.choice(allowed_chars) for i in range(length))
