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

The pipeline performs several data-cleaning operations.

### Text Cleaning

Text fields are stripped of unnecessary whitespace.

```python
text.strip()
```

### Price Cleaning

Book prices are converted from scraped text into numeric GBP values.

Example:

```text
£51.77
```

becomes:

```text
51.77
```

### Rating Conversion

Website rating labels are converted into integers.

Example:

```text
One → 1
Two → 2
Three → 3
Four → 4
Five → 5
```

### Invalid Records

Malformed records are skipped and warnings are generated.

### Duplicate Records

Duplicate scraped books are ignored.

---

# 11. Validation

The pipeline validates data before storing it.

## User Validation

A valid user must contain:

```text
name
username
email
company
```

All fields must contain non-empty strings.

## Book Validation

A valid book must contain:

```text
title
price
rating
```

The following conditions must be satisfied:

```text
title != empty
price >= 0
1 <= rating <= 5
```

---

# 12. Error Handling

The project includes explicit error handling for:

- Network failures
- HTTP errors
- Request timeouts
- Invalid JSON
- Missing files
- Invalid records
- Empty extraction results
- Invalid command-line arguments
- File-writing failures

The pipeline does **not** silently replace failed extraction with fake data.

If collection fails, the relevant stage reports the failure.

---

# 13. Atomic JSON Storage

JSON output is written atomically.

Instead of directly overwriting the destination file, the pipeline first writes the new content to a temporary file and then replaces the original file.

Conceptually:

```text
New Data
   │
   ▼
Temporary JSON File
   │
   ▼
Successful Write
   │
   ▼
Replace Existing File
```

This reduces the risk of leaving a partially written JSON file if an error occurs during writing.

---

# 14. Web Scraping Pagination

The scraper supports pagination.

The process is:

```text
Page 1
  │
  ▼
Extract Books
  │
  ▼
Enough Books?
 ┌┴──────────────┐
 │ Yes           │ No
 ▼               ▼
Stop         Next Page
                 │
                 ▼
             Extract Books
                 │
                 └──────► Repeat
```

The scraper continues until the requested number of valid books has been collected or there are no additional pages.

Example:

```bash
python main.py --step scrape --books 20
```

---

# 15. Requirements

The project uses Python packages listed in `requirements.txt`.

Example:

```text
requests
beautifulsoup4
```

Python standard-library modules such as:

```text
json
os
tempfile
unittest
argparse
collections
```

do not require separate installation.

---

# 16. Installation

Open PowerShell inside the project directory.

Create a virtual environment:

```powershell
py -m venv .venv
```

Activate it:

```powershell
.\.venv\Scripts\Activate.ps1
```

Install dependencies:

```powershell
python -m pip install -r requirements.txt
```

If PowerShell blocks virtual-environment activation, use:

```powershell
.venv\Scripts\python.exe -m pip install -r requirements.txt
```

and use:

```powershell
.venv\Scripts\python.exe
```

instead of `python`.

---

# 17. Running the Complete Pipeline

Run the complete pipeline using:

```powershell
python main.py --step all --books 20
```

The pipeline performs:

```text
API Extraction
      ↓
Web Scraping
      ↓
JSON Storage
      ↓
JSON Processing
      ↓
Data Analysis
      ↓
Final Report
```

Expected output files:

```text
data/
├── users.json
├── books.json
└── report.json
```

---

# 18. Running Individual Stages

## API Extraction

```powershell
python main.py --step api
```

This generates:

```text
data/users.json
```

---

## Web Scraping

```powershell
python main.py --step scrape --books 20
```

This generates:

```text
data/books.json
```

---

## JSON Processing

Run after API and scraping stages:

```powershell
python main.py --step report
```

---

## Analysis

```powershell
python main.py --step analyze
```

---

# 19. Running Individual Python Files

Each major stage can also be executed independently.

```powershell
python api_data.py
```

```powershell
python web_scraping.py
```

```powershell
python json_processing.py
```

```powershell
python analysis.py
```

---

# 20. Testing

Unit tests are included in:

```text
tests/test_pipeline.py
```

Run all tests with:

```powershell
python -m unittest discover -s tests -v
```

The tests use mocked network responses, so they do not require an active internet connection.

Expected output will contain successful test results similar to:

```text
test_api_extraction ... ok
test_book_parsing ... ok
test_validation ... ok
test_storage ... ok

----------------------------------------------------------------------
Ran X tests in X.XXXs

OK
```

The exact number and timing depend on the implementation.

---

# 21. Testing Architecture

```text
                 ┌─────────────────────┐
                 │   Unit Test Suite   │
                 │ test_pipeline.py    │
                 └──────────┬──────────┘
                            │
              ┌─────────────┼─────────────┐
              │             │             │
              ▼             ▼             ▼
        API Tests      Scraping Tests   Storage Tests
              │             │             │
              └─────────────┼─────────────┘
                            │
                            ▼
                    Validation Tests
                            │
                            ▼
                     Processing Tests
```

---

# 22. Reliability Features

The pipeline includes the following reliability features:

### Request Timeout

Network requests use timeouts so that the program does not wait indefinitely.

### HTTP Error Checking

HTTP errors are explicitly checked.

### Input Validation

Records are validated before being stored.

### Duplicate Prevention

Duplicate books are removed during scraping.

### Empty Result Protection

The pipeline fails instead of replacing existing data with an empty result caused by a collection failure.

### Atomic Writes

JSON files are safely written using temporary files before replacement.

### Explicit Error Reporting

Errors are reported to the user instead of being silently ignored.

---

# 23. Complete Pipeline Architecture

```text
                         DATA SOURCES
                              │
              ┌───────────────┴───────────────┐
              │                               │
              ▼                               ▼
        REST API                         Web Site
    JSONPlaceholder                 Books to Scrape
              │                               │
              ▼                               ▼
        api_data.py                    web_scraping.py
              │                               │
              ▼                               ▼
       User Validation               Book Validation
              │                               │
              ▼                               ▼
        Data Cleaning                  Data Cleaning
              │                               │
              ▼                               ▼
        users.json                     books.json
              │                               │
              └───────────────┬───────────────┘
                              │
                              ▼
                         storage.py
                              │
                              ▼
                    json_processing.py
                              │
                              ▼
                          analysis.py
                              │
                              ▼
                         report.json
                              │
                              ▼
                     Final Data Report
```

---

# 24. Command-Line Architecture

The `main.py` file provides a command-line interface.

```text
                  main.py
                     │
        ┌────────────┼────────────┐
        │            │            │
        ▼            ▼            ▼
       api         scrape       report
        │            │            │
        ▼            ▼            ▼
   api_data.py   web_scraping  json_processing
                                   │
                                   ▼
                              report.json
                                   │
                                   ▼
                                analyze
                                   │
                                   ▼
                              analysis.py
```

---

# 25. Expected Final Project Structure

After successfully running the pipeline, the project should look like:

```text
data-engineering-assignment/
│
├── api_data.py
├── web_scraping.py
├── storage.py
├── json_processing.py
├── analysis.py
├── main.py
├── requirements.txt
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

The JSON files inside `data/` must contain real records generated from the API and website.

---

# 26. Execution Evidence

For submission, the following evidence should be captured.

## Pipeline Execution

Run:

```powershell
python main.py --step all --books 20
```

Take a screenshot showing successful execution.

---

## Test Execution

Run:

```powershell
python -m unittest discover -s tests -v
```

Take a screenshot showing:

```text
OK
```

---

## Generated Data

Open:

```text
data/users.json
data/books.json
data/report.json
```

and verify that they contain real, non-empty data.

---

# 27. Submission Checklist

Before submitting the project, verify all of the following:

- [ ] Python virtual environment created
- [ ] Dependencies installed
- [ ] API extraction completed successfully
- [ ] Web scraping completed successfully
- [ ] At least 20 books collected
- [ ] `users.json` contains real API records
- [ ] `books.json` contains real scraped records
- [ ] `report.json` contains nonzero totals
- [ ] JSON validation works
- [ ] Duplicate books are handled
- [ ] Data cleaning is implemented
- [ ] Pagination is implemented
- [ ] Error handling is implemented
- [ ] Atomic JSON storage is implemented
- [ ] Unit tests pass
- [ ] Pipeline execution screenshot captured
- [ ] Test execution screenshot captured
- [ ] README included
- [ ] requirements.txt included
- [ ] tests included
- [ ] Generated JSON files included
- [ ] Entire project zipped

---

# 28. Important Data Integrity Rule

The following files:

```text
data/users.json
data/books.json
data/report.json
```

are **generated outputs**.

They must not be manually fabricated or filled with placeholder data.

The correct workflow is:

```text
Run Pipeline
     ↓
Collect Real Data
     ↓
Validate Data
     ↓
Clean Data
     ↓
Store JSON
     ↓
Process Data
     ↓
Generate Report
```

---

# 29. Limitations

This project is designed as a small educational Data Engineering pipeline and is not intended to be a production-grade scheduling or distributed processing system.

Known limitations include:

- Web scraping depends on the current HTML structure of the target website.
- Network access is required for live extraction.
- API availability may change.
- Website structure may change in the future.
- The project does not implement a production scheduler.
- The project does not use distributed processing frameworks such as Spark.
- The pipeline does not claim successful live extraction until it has actually been executed.

---

# 30. Conclusion

This project demonstrates a complete Python-based ETL workflow:

```text
EXTRACT
   ↓
API + Web Scraping
   ↓
TRANSFORM
   ↓
Validation + Cleaning + Deduplication
   ↓
LOAD
   ↓
JSON Storage
   ↓
PROCESS
   ↓
Filtering + Aggregation
   ↓
ANALYZE
   ↓
Statistics + Distributions
   ↓
REPORT
   ↓
report.json
```

The project provides a practical demonstration of how raw data from APIs and websites can be collected, validated, cleaned, stored, processed, and analyzed using Python.

It also demonstrates important Data Engineering practices such as modular project structure, error handling, reliable storage, testing, and command-line orchestration.
