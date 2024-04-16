"""Exceptions for the amapi package."""

from typing import Any, Mapping


class LoginCredentialsNotSetError(ValueError):
    """Exception raised when creating an API session without credentials set."""

    def __init__(self, *args: list[Any], **kwargs: Mapping[str, Any]) -> None:
        """Exception raised when creating an API session without credentials set."""
        super().__init__("REFESH_TOKEN, LWA_APP_ID and LWA_CLIENT_SECRET must be set.")
