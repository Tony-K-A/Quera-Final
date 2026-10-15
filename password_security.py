import hashlib
import hmac
import secrets

_PREFIX = "pbkdf2_sha256"
_ITERATIONS = 310_000

def hash_password(password):
    salt = secrets.token_hex(16)
    digest = hashlib.pbkdf2_hmac("sha256", password.encode("utf-8"), salt.encode("ascii"), _ITERATIONS)
    return f"{_PREFIX}${_ITERATIONS}${salt}${digest.hex()}"

def verify_password(password, stored):
    if not isinstance(stored, str):
        return False
    parts = stored.split("$")
    if len(parts) != 4 or parts[0] != _PREFIX:
        return False
    try:
        iterations = int(parts[1])
        expected = bytes.fromhex(parts[3])
    except (ValueError, TypeError):
        return False
    actual = hashlib.pbkdf2_hmac("sha256", password.encode("utf-8"), parts[2].encode("ascii"), iterations)
    return hmac.compare_digest(actual, expected)

def is_password_hash(value):
    return isinstance(value, str) and value.startswith(_PREFIX + "$")
