"""Exceptions for the amapi package."""

from typing import Any, Mapping


class LoginCredentialsNotSetError(ValueError):
    """Exception raised when creating an API session without credentials set."""

    def __init__(self, *args: list[Any], **kwargs: Mapping[str, Any]) -> None:
        """Exception raised when creating an API session without credentials set."""
        super().__init__(
            "REFRESH_TOKEN_KEY, APP_ID_KEY and CLIENT_SECRET_KEY must be set."
        )
