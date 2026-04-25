from app.exceptions.base import AppException


class PortfolioNotFoundError(AppException):
    def __init__(self) -> None:
        super().__init__(code="portfolio_not_found", message="Portfolio not found", status_code=404)
