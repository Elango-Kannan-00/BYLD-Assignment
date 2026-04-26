# BYLD Portfolio API

FastAPI backend for a portfolio management system built for a wealth-tech style use case.

The project focuses on correctness in money handling, clean separation of concerns, and a reviewer-friendly API surface that can be understood in a few minutes.

Reviewer path: `docker compose up`, then open `http://localhost:8000/swagger-ui`.

Deviation from the Spring Boot review constraint: this repository is FastAPI-based, so Swagger is exposed at `/swagger-ui` through FastAPI's built-in OpenAPI UI rather than a Spring Boot Swagger configuration.

Why FastAPI here: the codebase was already Python-based, and FastAPI gives typed request and response validation, automatic OpenAPI docs, and low-boilerplate routing. The tradeoff versus Spring Boot is less framework convention, so I compensated with an explicit Docker path, stricter validation, and integration tests against a real PostgreSQL database.

## Project Overview

This API lets a client create a portfolio, fund it, place buy and sell transactions, record dividends, and inspect holdings and portfolio summaries.

Money is handled with `Decimal` end-to-end, primary keys use UUIDs, and PostgreSQL stores monetary values in `NUMERIC` columns.
All money columns use `NUMERIC(19,4)` so the precision matches the assignment requirement.

## Features

- Create a portfolio with client name and risk profile
- Add cash balance to a portfolio
- Buy and sell transactions
- Weighted-average cost basis for holdings
- Portfolio summary and holdings view
- Record dividends against a record date
- Dividend payout calculation from holdings on record date
- Cash balance credit on dividend record
- Dividends grouped by symbol
- Structured validation and consistent error responses

## Tech Stack

- FastAPI
- PostgreSQL
- SQLAlchemy 2.0
- Alembic
- Pydantic v2
- Python 3.11+

## Project Structure

```text
.
├─ main.py
├─ app/
│  ├─ api/v1/routers/
│  ├─ core/
│  ├─ exceptions/
│  ├─ models/
│  ├─ repositories/
│  ├─ schemas/
│  ├─ services/
│  └─ utils/
├─ alembic/
├─ tests/
├─ AI_LOG.md
└─ pyproject.toml
```

## Setup Instructions

### 1. Clone the repo

```bash
git clone <repo-url>
cd BYLD-Portfolio-API
```

### 2. Start with Docker

```bash
docker compose up --build
```

This starts PostgreSQL and the API, runs database migrations automatically, and serves the docs at `http://localhost:8000/swagger-ui`.

### 3. Local development without Docker

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -e .[dev]
```

### 4. Set up PostgreSQL

Create a database and update `.env`:

```env
DATABASE_URL=postgresql+psycopg://postgres:postgres@localhost:5432/byld_portfolio
APP_NAME=BYLD Portfolio API
APP_ENV=development
```

### 5. Run Alembic migrations

```bash
alembic upgrade head
```

### 6. Run the app

```bash
uvicorn app.main:app --reload
```

### 7. Run real-DB integration tests

Start PostgreSQL with Docker, then point the integration suite at it:

```powershell
docker compose up -d db
$env:INTEGRATION_DATABASE_URL="postgresql+psycopg://postgres:postgres@localhost:5432/byld_portfolio"
pytest tests/integration -m integration
```

## API Endpoints

- `POST /v1/portfolios` - Create a portfolio
- `POST /v1/portfolios/{portfolio_id}/balance` - Add cash to a portfolio
- `GET /v1/portfolios/{portfolio_id}` - Return portfolio summary with holdings
- `GET /v1/portfolios/{portfolio_id}/holdings` - List holdings only
- `POST /v1/portfolios/{portfolio_id}/transactions/buy` - Buy shares and update weighted average cost
- `POST /v1/portfolios/{portfolio_id}/transactions/sell` - Sell shares and reject if quantity exceeds holdings
- `POST /v1/portfolios/{portfolio_id}/dividends` - Record a dividend and credit cash balance
- `GET /v1/portfolios/{portfolio_id}/dividends` - List dividends grouped by symbol

Variant B note: dividend payouts are calculated from holdings as of the record date, not from the current holdings after later trades.

## Docker Files

- [`Dockerfile`](c:/Users/Elango%20Kannan/Downloads/BYLD-Portfolio%20API/Dockerfile)
- [`docker-compose.yml`](c:/Users/Elango%20Kannan/Downloads/BYLD-Portfolio%20API/docker-compose.yml)

## Example Requests and Responses

### Create portfolio

```bash
curl -X POST http://127.0.0.1:8000/v1/portfolios \
  -H "Content-Type: application/json" \
  -d '{"clientName":"Aarav Mehta","riskProfile":"balanced"}'
```

```json
{
  "id": "0c0ef6f8-0d0b-4e1b-9eab-9f2d3f1f2f10",
  "clientName": "Aarav Mehta",
  "riskProfile": "balanced",
  "cashBalance": "0.0000",
  "message": "Portfolio created"
}
```

### Buy transaction

```bash
curl -X POST http://127.0.0.1:8000/v1/portfolios/0c0ef6f8-0d0b-4e1b-9eab-9f2d3f1f2f10/transactions/buy \
  -H "Content-Type: application/json" \
  -d '{"symbol":"aapl","quantity":5,"price":"120.0000"}'
```

```json
{
  "id": "6a5efb5c-233d-4f4f-b84f-6ccfb4b3f68c",
  "portfolioId": "0c0ef6f8-0d0b-4e1b-9eab-9f2d3f1f2f10",
  "symbol": "AAPL",
  "transactionType": "buy",
  "quantity": 5,
  "price": "120.0000",
  "totalAmount": "600.0000",
  "message": "Purchased the stock"
}
```

### Record dividend

```bash
curl -X POST http://127.0.0.1:8000/v1/portfolios/0c0ef6f8-0d0b-4e1b-9eab-9f2d3f1f2f10/dividends \
  -H "Content-Type: application/json" \
  -d '{"symbol":"AAPL","perShareAmount":"1.5000","recordDate":"2026-04-25"}'
```

```json
{
  "id": "3d7d4d41-5c51-4e45-8a64-26cc62d1d2f7",
  "portfolioId": "0c0ef6f8-0d0b-4e1b-9eab-9f2d3f1f2f10",
  "symbol": "AAPL",
  "quantityHeld": 12,
  "perShareAmount": "1.5000",
  "payout": "18.0000",
  "recordDate": "2026-04-25",
  "message": "Dividend recorded"
}
```

### Portfolio summary

```json
{
  "id": "0c0ef6f8-0d0b-4e1b-9eab-9f2d3f1f2f10",
  "clientName": "Aarav Mehta",
  "riskProfile": "balanced",
  "cashBalance": "118.0000",
  "holdings": [
    {
      "symbol": "AAPL",
      "quantity": 12,
      "weightedAverageCostBasis": "106.6667"
    }
  ]
}
```

## Design Decisions

- `Decimal` instead of float: money needs exact arithmetic. Float rounding errors are not acceptable for balances, payouts, or cost basis calculations.
- `NUMERIC(19,4)` for money: four decimal places preserve precision while keeping the representation predictable for financial calculations.
- Layered architecture: routers, services, repositories, models, and schemas keep transport, business logic, and persistence separate. That makes the code easier to test and safer to change.
- Weighted-average cost: it is recalculated only on `BUY`. `SELL` reduces quantity only, and rejects if the requested quantity exceeds current holdings with a `409` error.
- PostgreSQL `NUMERIC`: database storage matches the application-level Decimal model, so precision is preserved across reads and writes.

## Scaling Notes

- If traffic grows, the API can be split into authenticated ownership checks, read replicas for reporting, and background jobs for dividend processing.
- The current model keeps the domain simple and readable, which is a good fit for a reviewer exercise, but it would need pagination, caching, and ownership checks in production.
- Request IDs are echoed through the API as `X-Request-Id`, which makes tracing individual requests easier when logs get noisy.

## Two More Days

- Add authentication and portfolio ownership checks
- Add pagination, filtering, and sort options for holdings and dividends
- Add CI with linting, formatting, and coverage reporting
- Add richer portfolio analytics such as realized gain/loss and allocation breakdowns
- Add an authenticated request log dashboard or structured log sink

## Trade-offs

- No authentication or authorization layer
- No pagination or filtering on list endpoints
- No external market-data integration
- No async job queue for dividend processing
- No explicit transaction-history endpoint beyond the buy/sell operations

## AI Usage

AI was used during development. The prompt history and AI contribution notes are documented in [`AI_LOG.md`](c:/Users/Elango Kannan/Downloads/BYLD-Portfolio API/AI_LOG.md).

## Run Tests

```bash
pytest
```

If you want quieter output:

```bash
pytest -q
```
