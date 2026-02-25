import pytest
from unittest.mock import Mock, patch

from scraper.http.client import HttpClient
from requests.exceptions import ConnectionError
from scraper.exceptions import NetworkError


@patch("scraper.http.client.time.sleep", return_value=None)
def test_get_success_returns_text(mock_sleep):
    client = HttpClient()

    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.text = "OK"

    with patch.object(client.session, "get", return_value=mock_response):
        result = client.get("https://fake-url.com")

    assert result == "OK"


@patch("scraper.http.client.time.sleep", return_value=None)
def test_retry_on_500_then_success(mock_sleep):
    client = HttpClient(retries=3)

    response_500 = Mock()
    response_500.status_code = 500

    response_200 = Mock()
    response_200.status_code = 200
    response_200.text = "Recovered"

    with patch.object(
        client.session,
        "get",
        side_effect=[response_500, response_200],
    ):
        result = client.get("https://fake-url.com")

    assert result == "Recovered"


@patch("scraper.http.client.time.sleep", return_value=None)
def test_network_exception_raises_network_error(mock_sleep):
    client = HttpClient(retries=1)

    with patch.object(
        client.session,
        "get",
        side_effect=ConnectionError("Connection failed"),
    ):
        with pytest.raises(NetworkError):
            client.get("https://fake-url.com")