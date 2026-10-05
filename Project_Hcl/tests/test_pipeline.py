"""Offline tests: no live API or website is needed."""
import unittest
from unittest.mock import Mock
from bs4 import BeautifulSoup
from api_data import fetch_users
from web_scraping import parse_book, scrape_books
from analysis import analyze_books, analyze_users
from storage import validate_books, validate_users

USER = {'name': 'Alice', 'username': 'alice', 'email': 'alice@example.com', 'company': 'Example Group'}
BOOK = {'title': 'Example Book', 'price': 12.50, 'rating': 5}
HTML = '''<article class="product_pod"><h3><a title="Example Book">Book</a></h3>
<p class="star-rating Five"></p><p class="price_color">£12.50</p></article>'''


class PipelineTests(unittest.TestCase):
    def test_user_validation(self):
        self.assertEqual(validate_users([USER]), [USER])
        with self.assertRaises(ValueError):
            validate_users([{'name': 'Incomplete'}])

    def test_book_validation(self):
        self.assertEqual(validate_books([BOOK]), [BOOK])
        with self.assertRaises(ValueError):
            validate_books([{'title': 'Bad', 'price': -2, 'rating': 9}])

    def test_api_extraction(self):
        response = Mock()
        response.json.return_value = [{**USER, 'company': {'name': 'Example Group'}}]
        session = Mock()
        session.get.return_value = response
        self.assertEqual(fetch_users(session), [USER])
        session.get.assert_called_once()

    def test_api_bad_schema(self):
        response = Mock()
        response.json.return_value = {'not': 'a list'}
        session = Mock()
        session.get.return_value = response
        with self.assertRaises(ValueError):
            fetch_users(session)

    def test_scraping_parser(self):
        article = BeautifulSoup(HTML, 'html.parser').select_one('article')
        self.assertEqual(parse_book(article), BOOK)

    def test_scraping_request(self):
        response = Mock()
        response.text = HTML
        session = Mock()
        session.get.return_value = response
        self.assertEqual(scrape_books(1, session), [BOOK])

    def test_analysis(self):
        self.assertEqual(analyze_users([USER])['unique_companies'], 1)
        self.assertEqual(analyze_books([BOOK])['average_price'], 12.5)
        self.assertEqual(analyze_books([BOOK])['rating_distribution']['5'], 1)

    def test_empty_data_rejected(self):
        with self.assertRaises(ValueError):
            analyze_books([])


if __name__ == '__main__':
    unittest.main()
