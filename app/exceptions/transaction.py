from app.exceptions.base import AppException


class InsufficientHoldingError(AppException):
    def __init__(self) -> None:
        super().__init__(
            code="insufficient_holding",
            message="Insufficient holding quantity for sell transaction",
            status_code=409,
        )
