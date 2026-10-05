"""Shared paths, JSON I/O and record validation."""
import json
import math
import os
from pathlib import Path
from tempfile import NamedTemporaryFile

DATA_DIR = Path(__file__).resolve().parent / 'data'


def save_json(filename, records):
    """Atomically save JSON without corrupting an existing file on failure."""
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    destination = DATA_DIR / filename
    temporary = None
    try:
        with NamedTemporaryFile('w', encoding='utf-8', dir=DATA_DIR,
                                prefix='.tmp_', suffix='.json', delete=False) as file:
            temporary = Path(file.name)
            json.dump(records, file, indent=4, ensure_ascii=False, allow_nan=False)
            file.write('\n')
        os.replace(temporary, destination)
    finally:
        if temporary is not None and temporary.exists():
            temporary.unlink()
    return destination


def load_json(filename):
    """Load JSON with a clear error if the file is absent or malformed."""
    path = DATA_DIR / filename
    try:
        with path.open(encoding='utf-8') as file:
            return json.load(file)
    except FileNotFoundError as exc:
        raise ValueError(f'{path} is missing; run data collection first') from exc
    except json.JSONDecodeError as exc:
        raise ValueError(f'{path} contains invalid JSON: {exc}') from exc


def validate_users(users):
    if not isinstance(users, list) or not users:
        raise ValueError('users must be a non-empty list')
    for index, user in enumerate(users):
        if not isinstance(user, dict) or not all(
            isinstance(user.get(key), str) and user[key].strip()
            for key in ('name', 'username', 'email', 'company')
        ) or '@' not in user['email']:
            raise ValueError(f'Invalid user at index {index}')
    return users


def validate_books(books):
    if not isinstance(books, list) or not books:
        raise ValueError('books must be a non-empty list')
    for index, book in enumerate(books):
        if (not isinstance(book, dict)
            or not isinstance(book.get('title'), str) or not book['title'].strip()
            or type(book.get('price')) not in (int, float)
            or not math.isfinite(book['price']) or book['price'] < 0
            or type(book.get('rating')) is not int
            or not 1 <= book['rating'] <= 5):
            raise ValueError(f'Invalid book at index {index}')
    return books
