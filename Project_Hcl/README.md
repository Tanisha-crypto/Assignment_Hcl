# Python Data Engineering Assignment

## Data Collection and Processing Using JSON, APIs and Web Scraping

This project implements a small ETL-style data pipeline using Python.

## Objectives

The project demonstrates:

- REST API integration
- JSON processing
- Web scraping
- Data cleaning
- Data storage
- Data analysis
- Modular Python programming

## Data Sources

### API

JSONPlaceholder:

https://jsonplaceholder.typicode.com/users

### Website

Books to Scrape:

https://books.toscrape.com

## Project Structure

```text
Assignment/
│
├── api_data.py
├── web_scraping.py
├── json_processing.py
├── analysis.py
├── main.py
│
├── users.json
├── books.json
├── report.json
│
└── README.md
```

## Requirements

Python 3.9 or later is recommended.

Install the required libraries:

```bash
pip install requests beautifulsoup4
```

## Run the Individual Programs

### 1. API Data Collection

```bash
python api_data.py
```

This fetches users and creates:

```text
users.json
```

### 2. Web Scraping

```bash
python web_scraping.py
```

This scrapes at least 20 books and creates:

```text
books.json
```

### 3. JSON Processing

After `users.json` and `books.json` have been generated:

```bash
python json_processing.py
```

This creates:

```text
report.json
```

### 4. Data Analysis

```bash
python analysis.py
```

This displays user and book analysis.

## Run the Complete Pipeline

For the bonus challenge:

```bash
python main.py
```

Select:

```text
1. Fetch API Data
2. Scrape Book Data
3. Generate JSON Files
4. Analyze Data
5. Run Complete Pipeline
6. Exit
```

Option 5 executes the entire workflow automatically.

## Output Files

### users.json

Contains processed API user records:

```json
[
    {
        "name": "Leanne Graham",
        "email": "Sincere@april.biz",
        "company": "Romaguera-Crona"
    }
]
```

### books.json

Contains scraped book information:

```json
[
    {
        "title": "A Light in the Attic",
        "price": 51.77,
        "rating": 3
    }
]
```

### report.json

Contains combined summary information:

```json
{
    "total_users": 10,
    "total_books": 20,
    "average_price": 35.42
}
```

The exact book statistics can change if the website data changes.

## Error Handling

The programs include:

- HTTP error handling
- Request timeout
- File handling
- Invalid JSON handling
- Missing-file handling
- Basic validation for scraped ratings

## Data Pipeline

```text
JSONPlaceholder API
        |
        v
   api_data.py
        |
        v
    users.json
        |
        |
Books to Scrape
        |
        v
 web_scraping.py
        |
        v
    books.json
        |
        v
json_processing.py
        |
        v
   report.json
        |
        v
   analysis.py
```

## Learning Outcomes

After completing this project, the student can:

- Consume REST APIs using Python
- Parse JSON data
- Extract information from web pages
- Store structured data
- Build simple ETL pipelines
- Perform exploratory data analysis
- Create reusable data engineering workflows
