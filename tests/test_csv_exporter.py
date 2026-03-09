from scraper.exporters.csv_exporter import CSVExporter
from scraper.models import Product
from datetime import datetime, UTC


def test_csv_export(tmp_path):

    file_path = tmp_path / "products.csv"

    exporter = CSVExporter()

    product = Product(
        title="Mouse",
        price=25.0,
        currency="€",
        availability="In stock",
        scraped_at=datetime.now(UTC),
        url="https://example.com"
    )

    exporter.export([product], file_path)

    content = file_path.read_text()

    assert "Mouse" in content
    assert "25.0" in content