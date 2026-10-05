import json
import requests
from bs4 import BeautifulSoup

BASE_URL = "https://books.toscrape.com"
RATING_MAP = {
    "One": 1,
    "Two": 2,
    "Three": 3,
    "Four": 4,
    "Five": 5
}


def scrape_books(number_of_books=20):
    """Scrape at least the requested number of books."""
    books = []
    page_url = BASE_URL

    while len(books) < number_of_books and page_url:
        response = requests.get(page_url, timeout=10)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, "html.parser")

        for book in soup.select("article.product_pod"):
            title_element = book.select_one("h3 a")
            price_element = book.select_one(".price_color")
            rating_element = book.select_one(".star-rating")

            title = title_element.get("title", "").strip()
            price_text = price_element.get_text(strip=True)
            rating_word = next(
                (word for word in rating_element.get("class", [])
                 if word in RATING_MAP),
                None
            )

            if not rating_word:
                continue

            price = float(
                price_text.replace("£", "").replace(",", "").strip()
            )

            books.append({
                "title": title,
                "price": price,
                "rating": RATING_MAP[rating_word]
            })

            if len(books) >= number_of_books:
                break

        next_button = soup.select_one("li.next a")
        if next_button and len(books) < number_of_books:
            next_href = next_button.get("href")
            current_path = page_url.rsplit("/", 1)[0]
            page_url = f"{current_path}/{next_href}"
        else:
            page_url = None

    return books[:number_of_books]


def save_books(books, filename="books.json"):
    """Save scraped books to JSON."""
    with open(filename, "w", encoding="utf-8") as file:
        json.dump(books, file, indent=4, ensure_ascii=False)


def analyze_books(books):
    """Print basic price and rating analysis."""
    if not books:
        print("No books found.")
        return

    most_expensive = max(books, key=lambda book: book["price"])
    least_expensive = min(books, key=lambda book: book["price"])
    average_price = sum(book["price"] for book in books) / len(books)

    print("\n--- BOOK ANALYSIS ---")
    print(f"Most expensive: {most_expensive['title']} (£{most_expensive['price']:.2f})")
    print(f"Least expensive: {least_expensive['title']} (£{least_expensive['price']:.2f})")
    print(f"Average price: £{average_price:.2f}")


def main():
    try:
        books = scrape_books(20)

        print("\n--- SCRAPED BOOKS ---")
        for book in books:
            print(
                f"Title: {book['title']} | "
                f"Price: £{book['price']:.2f} | "
                f"Rating: {book['rating']}"
            )

        print(f"\nTotal books scraped: {len(books)}")
        analyze_books(books)

        save_books(books)
        print("\nSaved scraped data to books.json")

    except requests.RequestException as error:
        print(f"Website request failed: {error}")
    except OSError as error:
        print(f"File error: {error}")


if __name__ == "__main__":
    main()
