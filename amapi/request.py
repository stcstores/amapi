"""Amapi requests."""

import datetime as dt
from typing import Any

from sp_api.api import Reports
from sp_api.base import ApiResponse, Client

from .session import AmapiSession

GET_FBA_ESTIMATE_FEES_REPORT = "GET_FBA_ESTIMATED_FBA_FEES_TXT_DATA"


class BaseRequest:
    """Base class for amapi requests."""

    REQUEST_CLASS = Client
    REQUEST_METHOD = ""

    def __init__(self, session: AmapiSession) -> None:
        """Set session."""
        self.session = session

    def get_request(self) -> Client:
        """Return an instance of the request class."""
        return self.REQUEST_CLASS(
            credentials=self.session.get_credentials(),
            marketplace=self.session.marketplace,
        )

    def _request_args(self) -> dict[str, object]:
        return {"marketplaceIds": [self.session.marketplace.marketplace_id]}

    def request_args(self, *args: Any, **kwargs: Any) -> dict[str, object]:
        """Return request arguments."""
        return kwargs

    def call(self, *args: Any, **kwargs: Any) -> Any:
        """Make the request."""
        request = self.get_request()
        response = getattr(request, self.REQUEST_METHOD)(**self.request_args(**kwargs))
        return self.handle_response(response)

    def handle_response(self, response: ApiResponse) -> Any:
        """Return parsed response."""
        return response.payload


class GenerateReportRequest(BaseRequest):
    """Request class for generating reports."""

    REQUEST_CLASS = Reports
    REQUEST_METHOD = "create_report"

    def request_args(
        self, report_type: str, date: dt.datetime | None = None
    ) -> dict[str, Any]:
        """Return request arguments."""
        args = super()._request_args()
        date = date or dt.datetime.now(dt.timezone.utc) - dt.timedelta(hours=72)
        args["reportType"] = report_type
        args["dataStartTime"] = date.isoformat()
        return args

    def handle_response(self, response: ApiResponse) -> Any:
        """Return the generated report's report ID."""
        payload = super().handle_response(response)
        return payload["reportId"]


class GetDocumentIdRequest(BaseRequest):
    """Request class for retriveing the ID of a generated report document."""

    REQUEST_CLASS = Reports
    REQUEST_METHOD = "get_report"

    def request_args(self, report_id: str) -> dict[str, Any]:
        """Return request arguments."""
        args = super()._request_args()
        args["reportId"] = report_id
        return args

    def handle_response(self, response: ApiResponse) -> Any:
        """Return the ID of the document."""
        payload = super().handle_response(response)
        return payload["reportDocumentId"]


class GetDocumentUrlRequest(BaseRequest):
    """Request class for retrieving document URLs."""

    REQUEST_CLASS = Reports
    REQUEST_METHOD = "get_report_document"

    def request_args(self, document_id: str) -> dict[str, object]:
        """Return arguments for the request."""
        args = super()._request_args()
        args["reportDocumentId"] = document_id
        return args

    def handle_response(self, response: ApiResponse) -> Any:
        """Return the document's URL."""
        payload = super().handle_response(response)
        return payload["url"]


def request_generate_report(session: AmapiSession, report_type: str) -> str:
    """Request the generation of a report.

    Args:
        session (amapi.session.AmapiSession): A session instance.
        report_type (str): The type of report to genererate.
    """
    report_id = GenerateReportRequest(session).call(report_type=report_type)
    return str(report_id)


def request_document_id(session: AmapiSession, report_id: str) -> str:
    """
    Request the ID of a generated report document.

    Args:
        session (amapi.session.AmapiSession): A session instance.
        report_id (str): The ID of the report request.
    """
    docutment_id = GetDocumentIdRequest(session).call(report_id=report_id)
    return str(docutment_id)


def request_document_url(session: AmapiSession, document_id: str) -> str:
    """Request the URL of a generated document.

    args:
        session (amapi.session.AmapiSession): A session instance.
        document_id (str): The ID of the generated document.
    """
    url = GetDocumentUrlRequest(session).call(document_id=document_id)
    return str(url)
