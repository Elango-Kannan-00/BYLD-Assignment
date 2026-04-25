from collections.abc import Generator
from decimal import Decimal
from uuid import uuid4

import pytest
from fastapi.testclient import TestClient

from app.core.constants import RiskProfile
from app.main import app
from app.schemas.portfolio import PortfolioResponse


@pytest.fixture
def client() -> Generator[TestClient, None, None]:
    app.dependency_overrides.clear()
    with TestClient(app) as test_client:
        yield test_client
    app.dependency_overrides.clear()


@pytest.fixture
def portfolio_response() -> PortfolioResponse:
    return PortfolioResponse(
        id=uuid4(),
        clientName="Aarav Mehta",
        riskProfile=RiskProfile.balanced,
        cashBalance=Decimal("0.00"),
        message="Portfolio created",
    )
