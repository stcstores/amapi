"""amapi."""

import time
from pathlib import Path
from typing import Type

import requests

from amapi.request import (
    GET_FBA_ESTIMATE_FEES_REPORT,
    request_document_id,
    request_document_url,
    request_generate_report,
)
from amapi.session import AmapiSession, AmapiSessionUK, AmapiSessionUS

report_type = "GET_FBA_ESTIMATED_FBA_FEES_TXT_DATA"


UK_FILENAME = Path.home() / "Desktop" / f"{report_type}.csv"
US_FILENAME = Path.home() / "Desktop" / f"{report_type}_US.csv"


def get_report(session: Type[AmapiSession], filepath: Path) -> None:
    """Generate and download a report."""
    with session() as s:
        report_id = request_generate_report(
            session=s, report_type=GET_FBA_ESTIMATE_FEES_REPORT
        )
        time.sleep(60)
        document_id = request_document_id(s, report_id=report_id)
        document_url = request_document_url(s, document_id=document_id)
    document = requests.get(document_url).text

    with open(Path.cwd() / filepath, "w") as f:
        f.write(document)


def main() -> None:
    """Generate and download reports."""
    get_report(AmapiSessionUK, UK_FILENAME)
    get_report(AmapiSessionUS, US_FILENAME)


if __name__ == "__main__":
    main()
