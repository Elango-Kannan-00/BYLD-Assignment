from collections.abc import Sequence


class AppException(Exception):
    def __init__(
        self,
        code: str,
        message: str,
        details: Sequence[dict] | None = None,
        status_code: int = 400,
    ) -> None:
        self.code = code
        self.message = message
        self.details = list(details or [])
        self.status_code = status_code
        super().__init__(message)
