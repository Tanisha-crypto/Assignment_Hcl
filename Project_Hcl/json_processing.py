import json


def load_json(filename):
    """Load and return JSON data from a file."""
    with open(filename, "r", encoding="utf-8") as file:
        return json.load(file)


def process_json():
    users = load_json("users.json")
    books = load_json("books.json")

    print("\n--- JSON PROCESSING ---")
    print(f"Total users: {len(users)}")
    print(f"Total books: {len(books)}")

    print("\nBooks with rating greater than 4:")
    high_rated_books = [
        book for book in books
        if book["rating"] > 4
    ]

    if high_rated_books:
        for book in high_rated_books:
            print(f"- {book['title']} (Rating: {book['rating']})")
    else:
        print("No books found.")

    print("\nUsers whose company name contains 'Group':")
    group_users = [
        user for user in users
        if "group" in user["company"].lower()
    ]

    if group_users:
        for user in group_users:
            print(f"- {user['name']} | {user['company']}")
    else:
        print("No matching users found.")

    average_price = (
        sum(book["price"] for book in books) / len(books)
        if books else 0
    )

    report = {
        "total_users": len(users),
        "total_books": len(books),
        "average_price": round(average_price, 2)
    }

    with open("report.json", "w", encoding="utf-8") as file:
        json.dump(report, file, indent=4)

    print("\nCombined report:")
    print(json.dumps(report, indent=4))
    print("\nSaved report to report.json")


if __name__ == "__main__":
    try:
        process_json()
    except FileNotFoundError as error:
        print(f"Required JSON file not found: {error}")
    except json.JSONDecodeError as error:
        print(f"Invalid JSON: {error}")
