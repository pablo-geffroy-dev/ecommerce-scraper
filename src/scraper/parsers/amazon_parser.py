import re
from bs4 import BeautifulSoup
from datetime import datetime, UTC
from scraper.models import Product
from scraper.exceptions import ParsingError
from scraper.logger import get_logger


class AmazonParser:
    def __init__(self):
        self.logger = get_logger("scraper.parsers.amazon_parser")

    def parse(self, html: str, url: str) -> Product:
        if not html:
            raise ParsingError("Empty HTML content")

        soup = BeautifulSoup(html, "html.parser")

        title = self._parse_title(soup)
        price, currency = self._parse_price(soup)
        availability = self._parse_availability(soup)

        return Product(
            title=title,
            price=price,
            currency=currency,
            availability=availability,
            scraped_at=datetime.now(UTC),
            url=url,
        )

    def _parse_title(self, soup: BeautifulSoup) -> str:
        element = soup.select_one(".product-title")
        if not element or not element.text.strip():
            self.logger.error("Product title not found")
            raise ParsingError("Product title not found")

        return element.text.strip()

    def _parse_price(self, soup: BeautifulSoup) -> tuple[float, str]:
        element = soup.select_one(".price")
        if not element or not element.text.strip():
            self.logger.error("Product price not found")
            raise ParsingError("Product price not found")

        raw_price = element.text.strip()

        # Extract currency symbol (€, $, £ etc.)
        currency_match = re.match(r"([^\d]+)", raw_price)
        if not currency_match:
            self.logger.error(f"Currency not found in price: {raw_price}")
            raise ParsingError("Currency not found in price")

        currency = currency_match.group(1)

        # Extract numeric part
        number_match = re.search(r"([\d.,]+)", raw_price)
        if not number_match:
            self.logger.error(f"Numeric value not found in price: {raw_price}")
            raise ParsingError("Numeric value not found in price")

        number_str = number_match.group(1)

        # Normalize price (handle comma or dot decimal)
        normalized = number_str.replace(",", ".")

        try:
            price = float(normalized)
        except ValueError:
            self.logger.error(f"Invalid price format: {raw_price}")
            raise ParsingError("Invalid price format")

        return price, currency

    def _parse_availability(self, soup: BeautifulSoup) -> str:
        element = soup.select_one(".availability")
        if not element or not element.text.strip():
            self.logger.error("Availability information not found")
            raise ParsingError("Availability information not found")

        return element.text.strip()