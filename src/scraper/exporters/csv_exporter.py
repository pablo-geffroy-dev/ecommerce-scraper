import csv
from pathlib import Path
from scraper.models import Product
from scraper.exceptions import ScraperError
from scraper.logger import get_logger


class CSVExporter:

    def __init__(self):
        self.logger = get_logger("scraper.exporters.csv_exporter")

    def export(self, products: list[Product], path: str) -> None:
        file_exists = Path(path).exists()

        try:
            with open(path, "a", newline="", encoding="utf-8") as f:
                writer = csv.writer(f)

                if not file_exists:
                    writer.writerow([
                        "title",
                        "price",
                        "currency",
                        "availability",
                        "scraped_at",
                        "url",
                    ])

                for product in products:
                    writer.writerow([
                        product.title,
                        product.price,
                        product.currency,
                        product.availability,
                        product.scraped_at.isoformat(),
                        product.url,
                    ])

        except OSError as e:
            self.logger.error(f"CSV export failed: {e}")
            raise ScraperError("Failed to export CSV") from e