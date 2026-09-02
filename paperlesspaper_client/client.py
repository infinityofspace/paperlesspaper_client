import time
from urllib.parse import urljoin

import requests


class ClientError(Exception):
    """Base exception for client-side API errors."""


class RateLimitExceededError(ClientError):
    """Raised when retry attempts are exhausted after HTTP 429 responses."""


class RequestFailedError(ClientError):
    """Raised when the API responds with a non-success status code."""


class Client:
    API_BASE_URL = "https://api.paperlesspaper.de/v1/"

    def __init__(self, api_key: str, base_url: str = API_BASE_URL):
        """
        Initialize the API client and expose grouped API endpoint helpers.

        :param api_key: API key used for authenticating all requests.
        :param base_url: Base URL of the Paperlesspaper API.
        """
        # Lazy imports keep module import side effects low (helps autodoc import order).
        from paperlesspaper_client.api.accounts import Accounts
        from paperlesspaper_client.api.devices import Devices
        from paperlesspaper_client.api.organizations import Organizations
        from paperlesspaper_client.api.papers import Papers
        from paperlesspaper_client.api.users import Users

        self.base_url = base_url
        self.api_key = api_key

        self.accounts = Accounts(self)
        self.devices = Devices(self)
        self.organizations = Organizations(self)
        self.papers = Papers(self)
        self.users = Users(self)

    def _request(
        self,
        method: str,
        endpoint: str,
        headers: dict | None = None,
        params: dict | None = None,
        json: dict | None = None,
        retries: int = 3,
        timeout: int = 10,
        retry_delay: int = 10,
        **kwargs,
    ):
        """
        Make an HTTP request to the Paperlesspaper API with retry logic for rate limiting.

        :param method: HTTP method to use for the request.
        :param endpoint: API endpoint to send the request to.
        :param headers: Optional headers to include in the request.
        :param params: Optional query parameters to include in the request.
        :param json: Optional data to include in the request body.
        :param retries: Number of retries to attempt in case of rate limiting.
        :param timeout: Timeout in seconds for the request.
        :param retry_delay: Delay in seconds between retries.
        :param kwargs: Additional keyword arguments to pass to the request.
        :return: Response object from the API.
        """

        url = urljoin(self.base_url, endpoint)

        headers = headers or {}
        headers.update({"x-api-key": self.api_key, "Content-Type": "application/json"})

        for attempt in range(retries):
            response = requests.request(
                method,
                url,
                headers=headers,
                params=params,
                json=json,
                timeout=timeout,
                **kwargs,
            )

            if response.status_code == 429:
                if attempt < retries - 1:
                    print(f"Rate limit exceeded. Retrying in {retry_delay} seconds...")
                    time.sleep(retry_delay)
                    continue
                else:
                    raise RateLimitExceededError(
                        "Rate limit exceeded. Maximum retry attempts reached."
                    )
            elif not response.ok:
                raise RequestFailedError(
                    f"Request failed with status code {response.status_code}: {response.text}"
                )

            response.raise_for_status()

            return response

        return None

    def get(
        self,
        endpoint: str,
        headers: dict | None = None,
        params: dict | None = None,
        **kwargs,
    ):
        """
        Send a GET request to the given API endpoint.

        :param endpoint: Relative API endpoint path.
        :param headers: Optional additional request headers.
        :param params: Optional query parameters.
        :param kwargs: Additional keyword arguments forwarded to `requests.request`.
        :return: Response object from the API.
        """

        return self._request("GET", endpoint, headers=headers, params=params, **kwargs)

    def post(
        self,
        endpoint: str,
        headers: dict | None = None,
        params: dict | None = None,
        json: dict | None = None,
        **kwargs,
    ):
        """
        Send a POST request to the given API endpoint with an optional JSON payload.

        :param endpoint: Relative API endpoint path.
        :param headers: Optional additional request headers.
        :param params: Optional query parameters.
        :param json: Optional JSON request body.
        :param kwargs: Additional keyword arguments forwarded to `requests.request`.
        :return: Response object from the API.
        """

        return self._request(
            "POST", endpoint, headers=headers, params=params, json=json, **kwargs
        )

    def put(
        self,
        endpoint: str,
        headers: dict | None = None,
        params: dict | None = None,
        json: dict | None = None,
        **kwargs,
    ):
        """
        Send a PUT request to the given API endpoint with an optional JSON payload.

        :param endpoint: Relative API endpoint path.
        :param headers: Optional additional request headers.
        :param params: Optional query parameters.
        :param json: Optional JSON request body.
        :param kwargs: Additional keyword arguments forwarded to `requests.request`.
        :return: Response object from the API.
        """

        return self._request(
            "PUT", endpoint, headers=headers, params=params, json=json, **kwargs
        )

    def delete(
        self,
        endpoint: str,
        headers: dict | None = None,
        params: dict | None = None,
        **kwargs,
    ):
        """
        Send a DELETE request to the given API endpoint.

        :param endpoint: Relative API endpoint path.
        :param headers: Optional additional request headers.
        :param params: Optional query parameters.
        :param kwargs: Additional keyword arguments forwarded to `requests.request`.
        :return: Response object from the API.
        """

        return self._request(
            "DELETE", endpoint, headers=headers, params=params, **kwargs
        )

    def patch(
        self,
        endpoint: str,
        headers: dict | None = None,
        params: dict | None = None,
        json: dict | None = None,
        **kwargs,
    ):
        """
        Send a PATCH request to the given API endpoint with an optional JSON payload.

        :param endpoint: Relative API endpoint path.
        :param headers: Optional additional request headers.
        :param params: Optional query parameters.
        :param json: Optional JSON request body.
        :param kwargs: Additional keyword arguments forwarded to `requests.request`.
        :return: Response object from the API.
        """

        return self._request(
            "PATCH", endpoint, headers=headers, params=params, json=json, **kwargs
        )
