from app.exceptions.base import AppException


class DividendNotAllowedError(AppException):
    def __init__(self) -> None:
        super().__init__(code="dividend_not_allowed", message="Dividend cannot be recorded", status_code=400)
