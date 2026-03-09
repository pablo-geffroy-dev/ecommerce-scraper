from scraper.logger import get_logger
from scraper.exceptions import NetworkError, ParsingError


class ScraperService:

    def __init__(self, http_client, parser):
        self.http_client = http_client
        self.parser = parser
        self.logger = get_logger("scraper.services.scraper_service")

    def scrape(self, url: str):
        self.logger.info(f"Starting scrape for URL: {url}")

        # 1. Fetch HTML
        html = self.http_client.get(url)

        # 2. Parse product
        product = self.parser.parse(html, url)

        self.logger.info(f"Scraping successful for URL: {url}")

        return product