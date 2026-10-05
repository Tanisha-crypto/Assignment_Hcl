"""Scrape a requested number of validated books from Books to Scrape."""
import logging
from decimal import Decimal, InvalidOperation
from urllib.parse import urljoin
import requests
from bs4 import BeautifulSoup
from storage import save_json, validate_books

BASE_URL = 'https://books.toscrape.com/'
RATING_MAP = {'One': 1, 'Two': 2, 'Three': 3, 'Four': 4, 'Five': 5}
LOGGER = logging.getLogger(__name__)
HEADERS = {'User-Agent': 'UniversityDataEngineeringAssignment/1.0 (educational scraping)'}


def parse_book(article):
    title_node = article.select_one('h3 a')
    price_node = article.select_one('.price_color')
    rating_node = article.select_one('.star-rating')
    if not all((title_node, price_node, rating_node)):
        return None
    title = (title_node.get('title') or title_node.get_text(' ', strip=True)).strip()
    price_text = price_node.get_text(strip=True).replace('£', '').replace(',', '')
    rating = next((RATING_MAP[word] for word in rating_node.get('class', [])
                   if word in RATING_MAP), None)
    try:
        price = float(Decimal(price_text))
    except (InvalidOperation, ValueError):
        return None
    book = {'title': title, 'price': price, 'rating': rating}
    try:
        validate_books([book])
    except ValueError:
        return None
    return book


def scrape_books(number_of_books=20, session=None):
    if type(number_of_books) is not int or number_of_books < 1:
        raise ValueError('number_of_books must be a positive integer')
    client = session if session is not None else requests
    books, seen, visited = [], set(), set()
    page_url = BASE_URL
    while page_url and len(books) < number_of_books:
        if page_url in visited:
            raise ValueError('Pagination loop detected')
        visited.add(page_url)
        response = client.get(page_url, timeout=15, headers=HEADERS)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        articles = soup.select('article.product_pod')
        if not articles:
            raise ValueError(f'No book records found at {page_url}; HTML may have changed')
        for article in articles:
            book = parse_book(article)
            if book is None:
                LOGGER.warning('Skipping a malformed book record on %s', page_url)
                continue
            key = (book['title'], book['price'], book['rating'])
            if key not in seen:
                seen.add(key)
                books.append(book)
            if len(books) >= number_of_books:
                break
        next_node = soup.select_one('li.next a')
        page_url = urljoin(page_url, next_node['href']) if next_node and next_node.get('href') else None
    if len(books) < number_of_books:
        raise ValueError(f'Only {len(books)} valid books found; expected {number_of_books}')
    return validate_books(books)


def save_books(books):
    return save_json('books.json', validate_books(books))


def main():
    logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')
    try:
        books = scrape_books(20)
        path = save_books(books)
        print(f'Saved {len(books)} validated books to {path}')
        for book in books:
            print(f"{book['title']} | £{book['price']:.2f} | {book['rating']} stars")
    except (requests.RequestException, ValueError, OSError) as exc:
        LOGGER.error('Scraping failed: %s', exc)
        raise SystemExit(1) from exc


if __name__ == '__main__':
    main()
