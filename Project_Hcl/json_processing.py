"""Validate datasets, filter records and produce a structured JSON report."""
from analysis import analyze_books, analyze_users
from storage import load_json, save_json, validate_books, validate_users


def process_json():
    users = validate_users(load_json('users.json'))
    books = validate_books(load_json('books.json'))
    report = {
        'total_users': len(users),
        'total_books': len(books),
        'average_price': analyze_books(books)['average_price'],
        'users_in_group_companies': [
            user for user in users if 'group' in user['company'].casefold()
        ],
        'books_above_4_stars': [book for book in books if book['rating'] > 4],
        'user_analysis': analyze_users(users),
        'book_analysis': analyze_books(books),
    }
    path = save_json('report.json', report)
    return report, path


def main():
    try:
        report, path = process_json()
        print(f"Report saved to {path}: {report['total_users']} users, "
              f"{report['total_books']} books, average price £{report['average_price']:.2f}")
    except (ValueError, OSError) as exc:
        print(f'JSON processing failed: {exc}')
        raise SystemExit(1) from exc


if __name__ == '__main__':
    main()
