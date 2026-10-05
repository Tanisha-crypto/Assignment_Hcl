"""Collect and validate JSONPlaceholder users."""
import logging
import requests
from storage import save_json, validate_users

API_URL = 'https://jsonplaceholder.typicode.com/users'
LOGGER = logging.getLogger(__name__)


def fetch_users(session=None):
    client = session if session is not None else requests
    response = client.get(API_URL, timeout=15)
    response.raise_for_status()
    try:
        raw_users = response.json()
    except ValueError as exc:
        raise ValueError('API returned invalid JSON') from exc
    if not isinstance(raw_users, list):
        raise ValueError('API response must be a list of users')
    processed = []
    for index, user in enumerate(raw_users):
        if not isinstance(user, dict) or not isinstance(user.get('company'), dict):
            LOGGER.warning('Skipping malformed API record %s', index)
            continue
        record = {
            'name': str(user.get('name') or '').strip(),
            'username': str(user.get('username') or '').strip(),
            'email': str(user.get('email') or '').strip(),
            'company': str(user['company'].get('name') or '').strip(),
        }
        try:
            validate_users([record])
        except ValueError:
            LOGGER.warning('Skipping incomplete API record %s', index)
            continue
        processed.append(record)
    return validate_users(processed)


def save_users(users):
    return save_json('users.json', validate_users(users))


def main():
    logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')
    try:
        users = fetch_users()
        path = save_users(users)
        print(f'Saved {len(users)} validated users to {path}')
        for user in users:
            print(f"{user['name']} | {user['username']} | {user['email']} | {user['company']}")
    except (requests.RequestException, ValueError, OSError) as exc:
        LOGGER.error('API collection failed: %s', exc)
        raise SystemExit(1) from exc


if __name__ == '__main__':
    main()
