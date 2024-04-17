from unittest import mock

import pytest
from sp_api.api import Reports

from amapi.request import GetDocumentIdRequest


@pytest.fixture
def mock_session():
    session = mock.Mock()
    return session


@pytest.fixture
def request_instance(mock_session):
    request = GetDocumentIdRequest(session=mock_session)
    request.REQUEST_CLASS = mock.Mock()
    return request


def test_request_class_attribue():
    assert GetDocumentIdRequest.REQUEST_CLASS == Reports


def test_request_method_attribue():
    assert GetDocumentIdRequest.REQUEST_METHOD == "get_report"


def test_GetDocumentIdRequest_instance(mock_session, request_instance):
    assert request_instance.session == mock_session


def test_get_request_method(mock_session, request_instance):
    value = request_instance.get_request()
    mock_session.get_credentials.assert_called_once_with()
    request_instance.REQUEST_CLASS.assert_called_once_with(
        credentials=mock_session.get_credentials.return_value,
        marketplace=mock_session.marketplace,
    )
    assert value == request_instance.REQUEST_CLASS.return_value


def test__request_args_method(mock_session, request_instance):
    assert request_instance._request_args() == {
        "marketplaceIds": [mock_session.marketplace.marketplace_id]
    }


def test_request_args_method(mock_session, request_instance):
    report_id = "report_id"
    value = request_instance.request_args(report_id=report_id)
    assert value == {
        "marketplaceIds": [mock_session.marketplace.marketplace_id],
        "reportId": report_id,
    }


def test_call_method(request_instance, mock_session):
    kwargs = {"a": "b"}
    request_instance.get_request = mock.MagicMock()
    request_instance.request_args = mock.MagicMock()
    request_instance.handle_response = mock.MagicMock()
    value = request_instance.call(**kwargs)
    request_instance.get_request.assert_called_once_with()
    request = request_instance.get_request.return_value
    request_instance.request_args.assert_called_once_with(**kwargs)
    request.get_report.assert_called_once_with()
    request_instance.handle_response.assert_called_once_with(
        request.get_report.return_value
    )
    assert value == request_instance.handle_response.return_value


def test_handle_response_method(request_instance):
    response = mock.MagicMock()
    value = request_instance.handle_response(response)
    assert value == response.payload["reportDocumentId"]
