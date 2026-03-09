import argparse
from scraper.http.client import HttpClient
from scraper.parsers.amazon_parser import AmazonParser
from scraper.services.scraper_service import ScraperService
from scraper.exporters.csv_exporter import CSVExporter
from scraper.logger import get_logger
from scraper.exceptions import NetworkError, ParsingError


def main():
    parser = argparse.ArgumentParser()

    parser.add_argument("url", help="Product page URL")
    parser.add_argument("--output", default="products.csv")

    args = parser.parse_args()

    logger = get_logger("scraper.cli")

    http_client = HttpClient()
    parser_obj = AmazonParser()
    service = ScraperService(http_client, parser_obj)
    exporter = CSVExporter()

    try:
        product = service.scrape(args.url)
        exporter.export([product], args.output)
        
        logger.info(f"Product exported to {args.output}")

    except NetworkError as e:

        logger.error(f"Network error while scraping: {e}")

    except ParsingError as e:

        logger.error(f"Parsing error: {e}")

    except Exception as e:

        logger.error(f"Unexpected error: {e}")


if __name__ == "__main__":
    main()