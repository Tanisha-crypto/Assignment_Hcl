# Data Collection and Processing Using JSON, APIs and Web Scraping

**Course:** Python for Data Engineering  
**Project Type:** Educational ETL Pipeline  
**Language:** Python 3  
**Data Formats:** JSON  
**Libraries:** Requests, BeautifulSoup, JSON, Unittest  

---

## 1. Project Overview

This project demonstrates a small **ETL (Extract, Transform, Load) pipeline** using Python.

The pipeline collects data from two different sources:

1. **REST API** – JSONPlaceholder Users API
2. **Website** – Books to Scrape

The collected data is validated, cleaned, transformed, deduplicated, stored as JSON, processed, and analyzed to generate a combined report.

The project demonstrates the following Data Engineering concepts:

- API integration
- JSON processing
- Web scraping
- Data validation
- Data cleaning
- Deduplication
- Data transformation
- JSON storage
- Data analysis
- Error handling
- Atomic file writing
- Unit testing
- Command-line execution
- ETL pipeline orchestration

---

# 2. Data Sources

## API Source

**JSONPlaceholder Users API**

https://jsonplaceholder.typicode.com/users

The API provides user information including:

- Name
- Username
- Email
- Company

---

## Web Scraping Source

**Books to Scrape**

https://books.toscrape.com/

The website provides book information including:

- Book title
- Price
- Rating

The scraper follows pagination when required and collects at least 20 valid books.

---

# 3. ETL Pipeline

The project follows the following ETL process:

```text
                         ┌───────────────────────┐
                         │      DATA SOURCES     │
                         └───────────┬───────────┘
                                     │
                    ┌────────────────┴────────────────┐
                    │                                 │
                    ▼                                 ▼
          ┌───────────────────┐             ┌───────────────────┐
          │ JSONPlaceholder   │             │ Books to Scrape   │
          │      REST API     │             │      Website      │
          └─────────┬─────────┘             └─────────┬─────────┘
                    │                                 │
                    ▼                                 ▼
          ┌───────────────────┐             ┌───────────────────┐
          │   API Extraction  │             │  Web Scraping     │
          │    api_data.py    │             │ web_scraping.py   │
          └─────────┬─────────┘             └─────────┬─────────┘
                    │                                 │
                    ▼                                 ▼
          ┌───────────────────┐             ┌───────────────────┐
          │ Validate Users    │             │ Validate Books    │
          │ Required Fields   │             │ Price & Rating    │
          └─────────┬─────────┘             └─────────┬─────────┘
                    │                                 │
                    └───────────────┬─────────────────┘
                                    │
                                    ▼
                         ┌──────────────────────┐
                         │   Data Cleaning      │
                         │  Strip / Parse / Map │
                         └──────────┬───────────┘
                                    │
                                    ▼
                         ┌──────────────────────┐
                         │    Deduplication     │
                         │   Invalid Records    │
                         │      Removed         │
                         └──────────┬───────────┘
                                    │
                                    ▼
                         ┌──────────────────────┐
                         │    JSON Storage      │
                         │      storage.py      │
                         └──────────┬───────────┘
                                    │
                         ┌──────────┴───────────┐
                         │                      │
                         ▼                      ▼
                ┌─────────────────┐    ┌─────────────────┐
                │   users.json    │    │   books.json    │
                └────────┬────────┘    └────────┬────────┘
                         │                      │
                         └──────────┬───────────┘
                                    │
                                    ▼
                         ┌──────────────────────┐
                         │  JSON Processing     │
                         │ json_processing.py   │
                         └──────────┬───────────┘
                                    │
                                    ▼
                         ┌──────────────────────┐
                         │      Analysis        │
                         │     analysis.py      │
                         └──────────┬───────────┘
                                    │
                                    ▼
                         ┌──────────────────────┐
                         │    report.json       │
                         │ Combined ETL Report  │
                         └──────────────────────┘
```

---

# 4. Project Architecture

The project is divided into independent modules so that each stage of the pipeline can be tested and executed separately.

```text
Project Root
│
├── api_data.py
│
├── web_scraping.py
│
├── storage.py
│
├── json_processing.py
│
├── analysis.py
│
├── main.py
│
├── requirements.txt
│
├── README.md
│
├── data/
│   ├── users.json
│   ├── books.json
│   └── report.json
│
└── tests/
    └── test_pipeline.py
```

---

# 5. Project File Responsibilities

## `api_data.py`

Responsible for extracting user data from the REST API.

Main responsibilities:

- Send HTTP GET request
- Check HTTP response
- Parse JSON response
- Validate user records
- Clean text fields
- Save valid records to `users.json`
- Report errors clearly

---

## `web_scraping.py`

Responsible for extracting book information from Books to Scrape.

Main responsibilities:

- Request webpage HTML
- Parse HTML using BeautifulSoup
- Extract book title
- Extract book price
- Extract book rating
- Validate scraped records
- Remove duplicate books
- Follow pagination
- Stop after collecting requested number of books
- Save results to `books.json`

---

## `storage.py`

Provides shared JSON storage functionality.

Responsibilities:

- Load JSON files
- Validate records
- Save JSON data
- Perform atomic writes
- Prevent corrupted or partially written output
- Reject invalid/empty collection results where appropriate

---

## `json_processing.py`

Processes the collected datasets.

Responsibilities:

- Load `users.json`
- Load `books.json`
- Filter users belonging to companies containing `"Group"`
- Filter books rated above four stars
- Calculate total users
- Calculate total books
- Calculate average book price
- Generate combined report
- Save result to `report.json`

---

## `analysis.py`

Performs statistical analysis on the collected data.

Responsibilities:

- Calculate company frequencies
- Calculate book price statistics
- Calculate average price
- Calculate minimum price
- Calculate maximum price
- Generate rating distribution
- Analyze collected datasets

---

## `main.py`

Acts as the command-line entry point.

It provides a simple interface for executing individual pipeline stages or the complete pipeline.

Supported stages:

```text
api
scrape
report
analyze
all
```

It also provides failure reporting when a stage cannot be completed successfully.

---

## `tests/test_pipeline.py`

Contains unit tests for the pipeline.

Tests are designed to work without internet access by using mocked HTTP responses.

The tests verify:

- API extraction
- API validation
- Web scraping
- Book parsing
- Data cleaning
- Duplicate handling
- JSON storage
- Invalid input handling
- Pipeline processing

---

# 6. Data Flow

The complete data flow is:

```text
API
 │
 ▼
Extract Users
 │
 ▼
Validate
 │
 ▼
Clean
 │
 ▼
users.json
 │
 └──────────────────────┐
                        │
                        ▼
                    Processing
                        ▲
                        │
books.toscrape.com      │
 │                      │
 ▼                      │
Scrape Books            │
 │                      │
 ▼                      │
Validate                │
 │                      │
 ▼                      │
Clean                   │
 │                      │
 ▼                      │
Deduplicate             │
 │                      │
 ▼                      │
books.json ─────────────┘
                        │
                        ▼
                    Analysis
                        │
                        ▼
                  report.json
```

---

# 7. Data Schemas

## Users Schema

`users.json` contains an array of user objects.

Example structure:

```json
[
    {
        "name": "Example User",
        "username": "exampleuser",
        "email": "example@example.com",
        "company": "Example Group"
    }
]
```

Required fields:

| Field | Type | Requirement |
|---|---|---|
| name | string | Non-empty |
| username | string | Non-empty |
| email | string | Non-empty |
| company | string | Non-empty |

---

# 8. Books Schema

`books.json` contains an array of book objects.

Example structure:

```json
[
    {
        "title": "Example Book",
        "price": 25.99,
        "rating": 4
    }
]
```

Required fields:

| Field | Type | Requirement |
|---|---|---|
| title | string | Non-empty |
| price | number | >= 0 |
| rating | integer | 1–5 |

---

# 9. Report Schema

`report.json` contains the combined processing and analysis results.

The report includes:

- Total users
- Total books
- Average book price
- Users working in companies containing `"Group"`
- Books rated above four stars
- Company frequencies
- Book price statistics
- Rating distribution

A simplified structure is:

```json
{
    "total_users": 0,
    "total_books": 0,
    "average_price": 0,
    "group_users": [],
    "books_above_four_stars": [],
    "company_frequencies": {},
    "price_statistics": {},
    "rating_distribution": {}
}
```

The actual values are generated by running the pipeline and must not be manually fabricated.

---

# 10. Data Cleaning

The pipeline performs several data
