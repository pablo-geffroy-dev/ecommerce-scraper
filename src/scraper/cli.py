import argparse
import sys
from scraper.logger import get_logger


VERSION = "0.1.0"


def create_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="ecommerce-scraper",
        description="Structured e-commerce scraping tool",
    )

    parser.add_argument(
        "--version",
        action="store_true",
        help="Show application version",
    )

    parser.add_argument(
        "--verbose",
        action="store_true",
        help="Enable debug logging",
    )

    return parser


def main():
    parser = create_parser()
    args = parser.parse_args()

    log_level = None

    if args.verbose:
        log_level = 10  # logging.DEBUG
    else:
        log_level = 20  # logging.INFO

    logger = get_logger("scraper.cli", level=log_level)

    if args.version:
        print(f"ecommerce-scraper v{VERSION}")
        sys.exit(0)

    logger.info("CLI initialized successfully")


if __name__ == "__main__":
    main()


from scraper.http.client import HttpClient

client = HttpClient()
html = client.get("https://example.com")
print(html[:200])