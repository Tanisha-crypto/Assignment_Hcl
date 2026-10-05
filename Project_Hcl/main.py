"""CLI for running individual collection steps or the complete pipeline."""
import argparse
import logging
import requests
from api_data import fetch_users, save_users
from web_scraping import scrape_books, save_books
from json_processing import process_json
from analysis import analyze_users, analyze_books
from storage import load_json

LOGGER = logging.getLogger(__name__)


def run_api():
    users = fetch_users()
    print(f'API: saved {len(users)} users to {save_users(users)}')
    return users


def run_scraping(count):
    books = scrape_books(count)
    print(f'Scraping: saved {len(books)} books to {save_books(books)}')
    return books


def run_report():
    report, path = process_json()
    print(f"Report: saved to {path} ({report['total_users']} users, {report['total_books']} books)")
    return report


def run_analysis():
    import json
    result = {
        'users': analyze_users(load_json('users.json')),
        'books': analyze_books(load_json('books.json')),
    }
    print(json.dumps(result, indent=4))
    return result


def main(argv=None):
    parser = argparse.ArgumentParser(description='JSON, API and scraping data pipeline')
    parser.add_argument('--step', choices=['all', 'api', 'scrape', 'report', 'analyze'], default='all')
    parser.add_argument('--books', type=int, default=20, help='Number of books to scrape (default: 20)')
    args = parser.parse_args(argv)
    logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')
    try:
        if args.step in ('all', 'api'):
            run_api()
        if args.step in ('all', 'scrape'):
            run_scraping(args.books)
        if args.step in ('all', 'report'):
            run_report()
        if args.step in ('all', 'analyze'):
            run_analysis()
    except (requests.RequestException, ValueError, OSError) as exc:
        LOGGER.error('Pipeline stopped: %s', exc)
        return 1
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
