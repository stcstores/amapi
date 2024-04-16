"""Session manager for ampi."""

from pathlib import Path
from typing import Any, Callable, Self

import toml
from sp_api.base import Marketplaces

from . import exceptions


class AmapiSession:
    """Session manager for Amapi."""

    CONFIG_FILENAME = ".amapi.toml"
    refresh_token = None
    app_id = None
    client_secret = None
    marketplace: Marketplaces

    REFRESH_TOKEN_KEY: str
    APP_ID_KEY: str
    CLIENT_SECRET_KEY: str

    def __enter__(self) -> Self:
        if not self.__class__.credentials_are_set():
            config_path = self.__class__.find_config_filepath()
            if config_path is not None:
                self.__class__.load_from_config_file(config_file_path=config_path)
        if not self.__class__.credentials_are_set():
            raise exceptions.LoginCredentialsNotSetError()
        return self

    def __exit__(self, exc_type: None, exc_value: None, exc_tb: None) -> None:
        self.__class__.get_credentials()

    @classmethod
    def set_login(
        cls,
        refresh_token: str | None = None,
        app_id: str | None = None,
        client_secret: str | None = None,
    ) -> None:
        """Set login credentials (refresh_token, app_id, client_secret)."""
        cls.refresh_token = refresh_token
        cls.app_id = app_id
        cls.client_secret = client_secret

    @classmethod
    def credentials_are_set(cls) -> bool:
        """Return True if all auth credentials are set, otherwise False."""
        if None in (cls.refresh_token, cls.app_id, cls.client_secret):
            return False
        else:
            return True

    @classmethod
    def find_config_filepath(cls) -> Path | None:
        """
        Return the path to a shopify config file or None.

        Recursivly scan backwards from the current working directory and return the
        path to a file matching cls.CONFIG_FILENAME if one exists, otherwise returns
        None.
        """
        path = Path.cwd()
        while path.parent != path:
            config_file = path / cls.CONFIG_FILENAME
            if config_file.exists():
                return config_file
            path = path.parent
        return None

    @classmethod
    def load_from_config_file(cls, config_file_path: Path | str) -> None:
        """Set login credentials as specified in a toml file located at config_file_path."""
        with open(config_file_path) as f:
            config = toml.load(f)
        cls.set_login(
            refresh_token=config.get(cls.REFRESH_TOKEN_KEY),
            app_id=config.get(cls.APP_ID_KEY),
            client_secret=config.get(cls.CLIENT_SECRET_KEY),
        )

    @classmethod
    def get_credentials(cls) -> dict[str, str]:
        """Return session credentials as a dict."""
        return dict(
            refresh_token=str(cls.refresh_token),
            lwa_app_id=str(cls.app_id),
            lwa_client_secret=str(cls.client_secret),
        )


class AmapiSessionUK(AmapiSession):
    """Amapi session for Amazon UK."""

    REFRESH_TOKEN_KEY = "REFRESH_TOKEN_UK"
    APP_ID_KEY = "LWA_APP_ID_UK"
    CLIENT_SECRET_KEY = "LWA_CLIENT_SECRET_UK"
    marketplace = Marketplaces.UK


class AmapiSessionUS(AmapiSession):
    """Amapi session for Amazon US."""

    REFRESH_TOKEN_KEY = "REFRESH_TOKEN_US"
    APP_ID_KEY = "LWA_APP_ID_US"
    CLIENT_SECRET_KEY = "LWA_CLIENT_SECRET_US"
    marketplace = Marketplaces.US


def amazon_uk_session(func: Callable) -> Callable:
    """Use an amapi session as a method decorator."""

    def wrapper_amapi_session(*args: Any, **kwargs: Any) -> Any:
        with AmapiSessionUK() as session:
            kwargs["session"] = session
            return func(*args, **kwargs)

    return wrapper_amapi_session


def amazon_us_session(func: Callable) -> Callable:
    """Use an amapi session as a method decorator."""

    def wrapper_amapi_session(*args: Any, **kwargs: Any) -> Any:
        with AmapiSessionUS() as session:
            kwargs["session"] = session
            return func(*args, **kwargs)

    return wrapper_amapi_session
