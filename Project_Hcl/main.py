import api_data
import web_scraping
import json_processing
import analysis


def fetch_api_data():
    print("\nFetching API data...")
    users = api_data.fetch_users()
    api_data.save_users(users)
    print(f"Successfully saved {len(users)} users to users.json")


def scrape_book_data():
    print("\nScraping book data...")
    books = web_scraping.scrape_books(20)
    web_scraping.save_books(books)
    print(f"Successfully saved {len(books)} books to books.json")
    web_scraping.analyze_books(books)


def generate_json_files():
    print("\nGenerating JSON report...")
    json_processing.process_json()


def analyze_data():
    print("\nRunning analysis...")
    users = analysis.load_json("users.json")
    books = analysis.load_json("books.json")

    analysis.analyze_users(users)
    analysis.analyze_books(books)


def main():
    while True:
        print("\n======================================")
        print(" DATA COLLECTION & PROCESSING PIPELINE")
        print("======================================")
        print("1. Fetch API Data")
        print("2. Scrape Book Data")
        print("3. Generate JSON Files")
        print("4. Analyze Data")
        print("5. Run Complete Pipeline")
        print("6. Exit")

        choice = input("\nEnter your choice: ").strip()

        try:
            if choice == "1":
                fetch_api_data()

            elif choice == "2":
                scrape_book_data()

            elif choice == "3":
                generate_json_files()

            elif choice == "4":
                analyze_data()

            elif choice == "5":
                fetch_api_data()
                scrape_book_data()
                generate_json_files()
                analyze_data()
                print("\nComplete pipeline finished successfully.")

            elif choice == "6":
                print("Exiting program...")
                break

            else:
                print("Invalid choice. Please select 1-6.")

        except Exception as error:
            print(f"\nError: {error}")


if __name__ == "__main__":
    main()
