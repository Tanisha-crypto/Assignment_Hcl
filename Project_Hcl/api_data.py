import json
import requests

API_URL = "https://jsonplaceholder.typicode.com/users"


def fetch_users():
    """Fetch users from the JSONPlaceholder API and return processed records."""
    response = requests.get(API_URL, timeout=10)
    response.raise_for_status()

    users = response.json()

    processed_users = []
    for user in users:
        processed_users.append({
            "name": user.get("name", ""),
            "email": user.get("email", ""),
            "company": user.get("company", {}).get("name", "")
        })

    return processed_users


def save_users(users, filename="users.json"):
    """Save processed users to a JSON file."""
    with open(filename, "w", encoding="utf-8") as file:
        json.dump(users, file, indent=4, ensure_ascii=False)


def main():
    try:
        users = fetch_users()

        print("\n--- API DATA ---")
        for user in users:
            print(
                f"Name: {user['name']} | "
                f"Username: {user.get('username', 'N/A')} | "
                f"Email: {user['email']} | "
                f"Company: {user['company']}"
            )

        print(f"\nTotal users: {len(users)}")

        companies = sorted({user["company"] for user in users})
        print("\nCompany names:")
        for company in companies:
            print(company)

        save_users(users)
        print("\nSaved processed data to users.json")

    except requests.RequestException as error:
        print(f"API request failed: {error}")
    except OSError as error:
        print(f"File error: {error}")


if __name__ == "__main__":
    main()
