import time
import requests
from requests import Response
from requests.exceptions import RequestException
from scraper.config import DEFAULT_TIMEOUT,DEFAULT_RETRIES,BACKOFF_FACTOR,USER_AGENT
from scraper.exceptions import NetworkError
from scraper.logger import get_logger
import certifi

class HttpClient:
    def __init__(
        self,
        timeout: int = DEFAULT_TIMEOUT,
        retries: int = DEFAULT_RETRIES,
        backoff_factor: float = BACKOFF_FACTOR,
    ):
        self.timeout = timeout
        self.retries = retries
        self.backoff_factor = backoff_factor

        self.session = requests.Session()
        self.session.headers.update(self._build_headers())
        self.session.verify = certifi.where()
        self.logger = get_logger("scraper.http.client")
        

    def _build_headers(self) -> dict:
        return {
            "User-Agent": USER_AGENT,
            "Accept": "text/html,application/xhtml+xml",
        }

    def _should_retry(self, response: Response | None, exception: Exception | None) -> bool:
        if exception is not None:
            return True

        if response is None:
            return False

        if response.status_code == 429:
            return True

        if response.status_code >= 500:
            return True

        return False

    def get(self, url: str) -> str:
        last_exception = None

        for attempt in range(self.retries):
            try:
                self.logger.info(f"Sending request to {url} (attempt {attempt + 1})")

                response = self.session.get(url, timeout=self.timeout)

                if not self._should_retry(response, None):
                    if 200 <= response.status_code < 300:
                        return response.text
                    else:
                        raise NetworkError(
                            f"Request failed with status code {response.status_code}"
                        )

                self.logger.warning(
                    f"Retryable response received (status={response.status_code})"
                )

            except RequestException as exc:
                last_exception = exc
                self.logger.warning(
                    f"Request exception occurred: {exc} (attempt {attempt + 1})"
                )

                if not self._should_retry(None, exc):
                    raise NetworkError(str(exc)) from exc

            # Backoff before next attempt
            sleep_time = self.backoff_factor * (2 ** attempt)
            self.logger.info(f"Sleeping {sleep_time:.2f}s before retry")
            time.sleep(sleep_time)

        self.logger.error("Request failed after maximum retries")

        if last_exception:
            raise NetworkError(str(last_exception)) from last_exception

        raise NetworkError("Request failed after maximum retries")