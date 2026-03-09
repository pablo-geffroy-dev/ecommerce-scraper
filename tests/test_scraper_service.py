from unittest.mock import Mock
from scraper.services.scraper_service import ScraperService
from scraper.models import Product
from datetime import datetime, UTC
import pytest
from scraper.exceptions import NetworkError, ParsingError


def test_scrape_success():
    mock_http = Mock()
    mock_parser = Mock()

    mock_http.get.return_value = "<html>...</html>"

    expected_product = Product(
        title="Test",
        price=10.0,
        currency="€",
        availability="In stock",
        scraped_at=datetime.now(UTC),
        url="https://fake-url.com",
    )

    mock_parser.parse.return_value = expected_product

    service = ScraperService(mock_http, mock_parser)

    result = service.scrape("https://fake-url.com")

    assert result == expected_product
    mock_http.get.assert_called_once()
    mock_parser.parse.assert_called_once()

def test_scrape_propagates_network_error():
    mock_http = Mock()
    mock_parser = Mock()

    mock_http.get.side_effect = NetworkError("fail")

    service = ScraperService(mock_http, mock_parser)

    with pytest.raises(NetworkError):
        service.scrape("https://fake-url.com")