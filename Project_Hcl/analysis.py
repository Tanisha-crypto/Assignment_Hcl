import json
from collections import Counter


def load_json(filename):
    with open(filename, "r", encoding="utf-8") as file:
        return json.load(file)


def analyze_users(users):
    print("\n========== USER ANALYSIS ==========")

    print(f"Total Users: {len(users)}")

    companies = [user["company"] for user in users]
    unique_companies = sorted(set(companies))

    print(f"Unique Companies: {len(unique_companies)}")

    print("\nTop 5 Companies (Alphabetically):")
    for company in unique_companies[:5]:
        print(f"- {company}")


def analyze_books(books):
    print("\n========== BOOK ANALYSIS ==========")

    if not books:
        print("No books available.")
        return

    average_price = sum(book["price"] for book in books) / len(books)

    print(f"Average Price: £{average_price:.2f}")

    highest_rating = max(book["rating"] for book in books)

    print(f"\nHighest Rating: {highest_rating}")
    print("Highest Rated Books:")
    for book in books:
        if book["rating"] == highest_rating:
            print(f"- {book['title']}")

    rating_counts = Counter(book["rating"] for book in books)

    print("\nNumber of Books in Each Rating Category:")
    for rating in range(1, 6):
        print(f"{rating} Star: {rating_counts.get(rating, 0)}")


def main():
    try:
        users = load_json("users.json")
        books = load_json("books.json")

        analyze_users(users)
        analyze_books(books)

    except FileNotFoundError as error:
        print(f"Required file not found: {error}")
    except json.JSONDecodeError as error:
        print(f"Invalid JSON file: {error}")


if __name__ == "__main__":
    main()
