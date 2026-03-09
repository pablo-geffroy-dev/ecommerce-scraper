# E-commerce Scraper

A structured Python scraping tool designed to extract product information from e-commerce pages and export the data to CSV.

This project demonstrates a clean architecture approach with modular components, robust error handling, logging, and unit testing.

---

# Features

* HTTP client with retry and exponential backoff
* HTML parsing using BeautifulSoup
* Structured data model (`Product`)
* CSV export
* CLI interface
* Structured logging (console + file)
* Unit tests with pytest
* Clean modular architecture

---

# Project Structure

```
src/
  scraper/
    http/          # HTTP client
    parsers/       # HTML parsers
    services/      # orchestration logic
    exporters/     # CSV export
    models.py      # data models
    exceptions.py  # custom exceptions
    logger.py      # logging configuration
    cli.py         # command line interface

tests/             # unit tests
```

---

# Installation

Clone the repository:

```
git clone https://github.com/YOUR_USERNAME/ecommerce-scraper.git
cd ecommerce-scraper
```

Create a virtual environment:

```
python -m venv .venv
```

Activate it:

Windows

```
.venv\Scripts\activate
```

Linux / Mac

```
source .venv/bin/activate
```

Install dependencies:

```
pip install -r requirements.txt
pip install -e .
```

---

# Usage

Run the scraper from the CLI:

```
python -m scraper.cli https://example.com --output products.csv
```

Output example:

```
title,price,currency,availability,scraped_at,url
Gaming Mouse X200,49.99,€,In stock,2026-03-09T16:00:00,https://example.com
```

Logs will be written to:

```
logs/scraper.log
```

---

# Running Tests

Run the test suite with:

```
pytest -v
```

Example output:

```
7 passed
```

---

# Architecture

The project follows a layered architecture:

```
CLI
 ↓
ScraperService
 ↓
HttpClient → Parser
 ↓
Product model
 ↓
CSVExporter
```

Each component is isolated and testable.

---

# Example Product Model

```
Product(
    title="Gaming Mouse X200",
    price=49.99,
    currency="€",
    availability="In stock",
    scraped_at=datetime,
    url="https://example.com"
)
```

---

# Future Improvements

Possible extensions:

* price history tracking
* multiple marketplace parsers
* async scraping
* database storage
* Docker support

---

# License

MIT License
