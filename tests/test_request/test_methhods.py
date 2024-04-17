from unittest import mock

import pytest

from amapi import request


@pytest.fixture
def mock_session():
    return mock.Mock()


@mock.patch("amapi.request.GenerateReportRequest")
def test_request_generate_report(mock_request_class, mock_session):
    report_type = "report_type"
    value = request.request_generate_report(
        session=mock_session, report_type=report_type
    )
    mock_request_class.assert_called_once_with(mock_session)
    mock_request_class.return_value.call.assert_called_once_with(
        report_type=report_type
    )
    assert value == str(mock_request_class.return_value.call.return_value)


@mock.patch("amapi.request.GetDocumentIdRequest")
def test_request_document_id(mock_request_class, mock_session):
    report_id = "report_id"
    value = request.request_document_id(session=mock_session, report_id=report_id)
    mock_request_class.assert_called_once_with(mock_session)
    mock_request_class.return_value.call.assert_called_once_with(report_id=report_id)
    assert value == str(mock_request_class.return_value.call.return_value)


@mock.patch("amapi.request.GetDocumentUrlRequest")
def test_request_document_url(mock_request_class, mock_session):
    document_id = "document_id"
    value = request.request_document_url(session=mock_session, document_id=document_id)
    mock_request_class.assert_called_once_with(mock_session)
    mock_request_class.return_value.call.assert_called_once_with(
        document_id=document_id
    )
    assert value == str(mock_request_class.return_value.call.return_value)
