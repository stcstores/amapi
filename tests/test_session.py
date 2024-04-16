from pathlib import Path
from unittest import mock

import pytest
import toml
from sp_api.base import Marketplaces

from amapi import exceptions
from amapi.session import AmapiSession, AmapiSessionUK, AmapiSessionUS


@pytest.fixture(autouse=True)
def temp_cwd(tmpdir):
    with tmpdir.as_cwd():
        yield tmpdir


@pytest.fixture
def refresh_token():
    return "REFRESH_TOKEN"


@pytest.fixture
def app_id():
    return "APP_ID"


@pytest.fixture
def client_secret():
    return "CLIENT_SECRET"


@pytest.fixture
def config_filename():
    return "config_file.toml"


@pytest.fixture
def config_file(refresh_token, config_filename, app_id, client_secret):
    data = {
        AmapiSessionUK.REFRESH_TOKEN_KEY: refresh_token,
        AmapiSessionUK.APP_ID_KEY: app_id,
        AmapiSessionUK.CLIENT_SECRET_KEY: client_secret,
    }
    path = Path.cwd() / config_filename
    with open(path, "w") as f:
        toml.dump(data, f)
    return path


@pytest.fixture
def mock_credentials_are_set_method():
    with mock.patch("amapi.session.AmapiSession.credentials_are_set") as m:
        m.return_value = True
        yield m


@pytest.fixture
def mock_load_from_config_file_method():
    with mock.patch("amapi.session.AmapiSession.load_from_config_file") as m:
        yield m


@pytest.fixture
def mock_find_config_filepath_method():
    with mock.patch("amapi.session.AmapiSession.find_config_filepath") as m:
        yield m


@pytest.fixture
def reset_session():
    AmapiSession.CONFIG_FILENAME = None
    AmapiSession.refresh_token = None
    AmapiSession.app_id = None
    AmapiSession.client_secret = None
    AmapiSessionUK.CONFIG_FILENAME = None
    AmapiSessionUK.refresh_token = None
    AmapiSessionUK.app_id = None
    AmapiSessionUK.client_secret = None
    AmapiSessionUS.CONFIG_FILENAME = None
    AmapiSessionUS.refresh_token = None
    AmapiSessionUS.app_id = None
    AmapiSessionUS.client_secret = None


def test_enter_method_with_credentials_set(
    reset_session,
    mock_credentials_are_set_method,
    mock_load_from_config_file_method,
    mock_find_config_filepath_method,
):
    with AmapiSessionUK() as session:
        mock_credentials_are_set_method.call_count == 1
        mock_find_config_filepath_method.assert_not_called()
        mock_load_from_config_file_method.assert_not_called()
        assert isinstance(session, AmapiSession)


def test_enter_method_with_load_credentials_from_file(
    reset_session,
    mock_credentials_are_set_method,
    mock_load_from_config_file_method,
    mock_find_config_filepath_method,
):
    mock_credentials_are_set_method.side_effect = [False, True]
    with AmapiSessionUK() as session:
        mock_credentials_are_set_method.call_count == 2
        mock_find_config_filepath_method.assert_called_once_with()
        mock_load_from_config_file_method.assert_called_once_with(
            config_file_path=mock_find_config_filepath_method.return_value
        )
        assert isinstance(session, AmapiSession)


def test_enter_method_without_config_or_path(
    reset_session,
    mock_credentials_are_set_method,
    mock_load_from_config_file_method,
    mock_find_config_filepath_method,
):
    mock_credentials_are_set_method.side_effect = [False, False]
    mock_find_config_filepath_method.return_value = None
    with pytest.raises(exceptions.LoginCredentialsNotSetError):
        with AmapiSessionUK() as session:
            mock_credentials_are_set_method.call_count == 2
            mock_find_config_filepath_method.assert_called_once_with()
            assert isinstance(session, AmapiSession)


def test_set_login_method(reset_session, refresh_token, app_id, client_secret):
    AmapiSession.set_login(
        refresh_token=refresh_token, app_id=app_id, client_secret=client_secret
    )
    assert AmapiSession.refresh_token == refresh_token
    assert AmapiSession.app_id == app_id
    assert AmapiSession.client_secret == client_secret


@pytest.mark.parametrize(
    "refresh_token,app_id,client_secret,expected",
    (
        ("REFRESH_TOKEN", "APP_ID", "CLIENT_SECRET", True),
        (None, "APP_ID", "CLIENT_SECRET", False),
        ("REFRESH_TOKEN", None, "CLIENT_SECRET", False),
        ("REFRESH_TOKEN", "APP_ID", None, False),
        (None, None, "CLIENT_SECRET", False),
        (None, None, None, False),
    ),
)
def test_credentials_are_set_method(
    refresh_token, app_id, client_secret, expected, reset_session
):
    AmapiSession.refresh_token = refresh_token
    AmapiSession.app_id = app_id
    AmapiSession.client_secret = client_secret
    assert AmapiSession.credentials_are_set() is expected


def test_find_config_filepath_returns_config_file_in_cwd(
    temp_cwd, config_filename, config_file
):
    AmapiSession.CONFIG_FILENAME = config_filename
    path = AmapiSession.find_config_filepath()
    assert path == temp_cwd / AmapiSession.CONFIG_FILENAME


def test_find_config_filepath_returns_None_without_config_file_path_set(reset_session):
    path = AmapiSession.find_config_filepath()
    assert path is None


def test_find_config_filepath_returns_None_without_config_file_in_cwd(
    reset_session, config_filename
):
    AmapiSession.CONFIG_FILENAME = config_filename
    path = AmapiSession.find_config_filepath()
    assert path is None


def test_load_from_config_file_sets_credendials(
    reset_session, config_file, refresh_token, app_id, client_secret
):
    AmapiSessionUK.load_from_config_file(config_file)
    assert AmapiSessionUK.refresh_token == refresh_token
    assert AmapiSessionUK.app_id == app_id
    assert AmapiSessionUK.client_secret == client_secret


def test_amapi_session_uk(reset_session):
    assert AmapiSessionUK.REFRESH_TOKEN_KEY == "REFRESH_TOKEN_UK"
    assert AmapiSessionUK.APP_ID_KEY == "LWA_APP_ID_UK"
    assert AmapiSessionUK.CLIENT_SECRET_KEY == "LWA_CLIENT_SECRET_UK"
    assert AmapiSessionUK.marketplace == Marketplaces.UK


def test_amapi_session_us(reset_session):
    assert AmapiSessionUS.REFRESH_TOKEN_KEY == "REFRESH_TOKEN_US"
    assert AmapiSessionUS.APP_ID_KEY == "LWA_APP_ID_US"
    assert AmapiSessionUS.CLIENT_SECRET_KEY == "LWA_CLIENT_SECRET_US"
    assert AmapiSessionUS.marketplace == Marketplaces.US
