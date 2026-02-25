class ScraperError(Exception):
    """Base exception for scraper domain."""


class NetworkError(ScraperError):
    """Raised when network request fails."""