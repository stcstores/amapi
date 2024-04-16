import pytest

from amapi import exceptions


def test_login_credentials_not_set_error():
    with pytest.raises(
        exceptions.LoginCredentialsNotSetError,
        match="REFRESH_TOKEN_KEY, APP_ID_KEY and CLIENT_SECRET_KEY must be set.",
    ):
        raise exceptions.LoginCredentialsNotSetError
