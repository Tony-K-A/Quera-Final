import re

USERNAME_RE = re.compile(r"[A-Za-z][A-Za-z0-9_]{2,19}")
NAME_RE = re.compile(r"[^\W\d_][\w ]{1,39}")
TIME_RE = re.compile(r"(?:[01]\d|2[0-3]):[0-5]\d")
POSITIVE_INT_RE = re.compile(r"[1-9]\d{0,8}")
NON_NEGATIVE_INT_RE = re.compile(r"\d{1,5}")
TOOLS_RE = re.compile(r"[\w ]+(?:\s*,\s*[\w ]+)*")
CARD_RE = re.compile(r"\d{16}")
EXPIRY_RE = re.compile(r"(?:0[1-9]|1[0-2])/\d{2}")
CVV2_RE = re.compile(r"\d{3,4}")

NAME_ERROR = "Use 2-40 characters: letters, digits and spaces."
USERNAME_ERROR = "Use 3-20 characters: letters, digits, underscore."
