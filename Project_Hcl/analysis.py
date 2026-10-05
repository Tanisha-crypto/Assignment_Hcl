"""Compute meaningful descriptive statistics from validated records."""
from collections import Counter
from statistics import mean, median
from storage import load_json, validate_books, validate_users


def analyze_users(users):
    validate_users(users)
    counts = Counter(user['company'] for user in users)
    return {
        'total_users': len(users),
        'unique_companies': len(counts),
        'top_5_companies_by_user_count': [
            {'company': name, 'users': count}
            for name, count in sorted(counts.items(), key=lambda item: (-item[1], item[0]))[:5]
        ],
        'company_frequencies': dict(sorted(counts.items())),
    }


def analyze_books(books):
    validate_books(books)
    prices = [book['price'] for book in books]
    highest_rating = max(book['rating'] for book in books)
    most_expensive = max(books, key=lambda book: book['price'])
    least_expensive = min(books, key=lambda book: book['price'])
    rating_counts = Counter(book['rating'] for book in books)
    return {
        'total_books': len(books),
        'average_price': round(mean(prices), 2),
        'median_price': round(median(prices), 2),
        'minimum_price': min(prices),
        'maximum_price': max(prices),
        'most_expensive_book': most_expensive,
        'least_expensive_book': least_expensive,
        'average_rating': round(mean(book['rating'] for book in books), 2),
        'highest_rating': highest_rating,
        'highest_rated_books': [book['title'] for book in books if book['rating'] == highest_rating],
        'rating_distribution': {str(rating): rating_counts.get(rating, 0) for rating in range(1, 6)},
        'books_above_4_stars': [book for book in books if book['rating'] > 4],
    }


def main():
    import json
    try:
        users = load_json('users.json')
        books = load_json('books.json')
        print(json.dumps({'users': analyze_users(users), 'books': analyze_books(books)}, indent=4))
    except (ValueError, OSError) as exc:
        print(f'Analysis failed: {exc}')
        raise SystemExit(1) from exc


if __name__ == '__main__':
    main()
