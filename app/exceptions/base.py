from collections.abc import Sequence


class AppException(Exception):
    def __init__(self, code: str, message: str, details: Sequence[dict] | None = None) -> None:
        self.code = code
        self.message = message
        self.details = list(details or [])
        super().__init__(message)
