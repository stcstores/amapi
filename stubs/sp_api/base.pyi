from enum import Enum
from typing import Self

class Marketplaces(Enum):
    endpioint: str
    marketplace_id: str
    region: str
    def __init__(self, endpioint: str, marketplace_id: str, region: str): ...
    UK: Self
    US: Self

class SellingApiException(Exception): ...

class Client:
    def __init__(
        self,
        marketplace: Marketplaces,
        credentials: dict[str, str] | None,
    ): ...

class ApiResponse:
    payload: dict[str, object]
