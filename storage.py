import json
import os
import tempfile
from pathlib import Path
from datetime import datetime

BASE_DIR = Path(__file__).resolve().parent

USERS = BASE_DIR / "users.json"
HALLS = BASE_DIR / "halls.json"
CLASSES = BASE_DIR / "classes.json"
SUBSCRIPTIONS = BASE_DIR / "subscriptions.json"
PAYMENTS = BASE_DIR / "payments.json"
ENROLLMENTS = BASE_DIR / "enrollments.json"
WORKOUTS = BASE_DIR / "workouts.json"
WALLETS = BASE_DIR / "wallets.json"
TRANSACTIONS = BASE_DIR / "transactions.txt"

class DataError(Exception):
    pass

def load_json(path, default):
    path = Path(path)
    try:
        with path.open("r", encoding="utf-8") as f:
            data = json.load(f)
    except FileNotFoundError:
        return default
    except json.JSONDecodeError as e:
        raise DataError(f"{path.name} is corrupted ({e}). Fix the file before continuing.") from e
    except OSError as e:
        raise DataError(f"Cannot read {path.name}: {e}") from e

    if isinstance(default, list) and not isinstance(data, list):
        raise DataError(f"{path.name} must contain a JSON list.")
    if isinstance(default, dict) and not isinstance(data, dict):
        raise DataError(f"{path.name} must contain a JSON object.")
    return data

def save_json(path, data):
    path = Path(path)
    temp_path = None
    try:
        path.parent.mkdir(parents=True, exist_ok=True)
        with tempfile.NamedTemporaryFile("w", encoding="utf-8", dir=path.parent,
                                         prefix=path.name + ".", suffix=".tmp", delete=False) as f:
            temp_path = Path(f.name)
            json.dump(data, f, indent=4, ensure_ascii=False)
            f.flush()
            os.fsync(f.fileno())
        os.replace(temp_path, path)
    except (OSError, TypeError, ValueError) as e:
        if temp_path is not None:
            try:
                temp_path.unlink(missing_ok=True)
            except OSError:
                pass
        raise DataError(f"Cannot write {path.name}: {e}") from e

def append_line(path, line):
    path = Path(path)
    try:
        with path.open("a", encoding="utf-8") as f:
            f.write(line + "\n")
    except OSError as e:
        raise DataError(f"Cannot write {path.name}: {e}") from e

def read_lines(path):
    path = Path(path)
    try:
        with path.open("r", encoding="utf-8") as f:
            return [line.rstrip("\n") for line in f if line.strip()]
    except FileNotFoundError:
        return []
    except OSError as e:
        raise DataError(f"Cannot read {path.name}: {e}") from e

def now_str():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")
