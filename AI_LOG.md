## AI Used

* Codex (OpenAI)

## Prompt

Asked AI to:

* Build a FastAPI backend for a portfolio system
* Create project structure
* Implement REST API for all the necessary endpoints
* Set up PostgreSQL + Alembic
* Add tests and dependencies

## API Endpoint Log

The following endpoints were implemented and documented as part of the API surface:

* `POST /v1/portfolios` - Create a portfolio
* `POST /v1/portfolios/{portfolio_id}/balance` - Add cash balance to an existing portfolio
* `GET /v1/portfolios/{portfolio_id}` - Return a portfolio summary with holdings
* `GET /v1/portfolios/{portfolio_id}/holdings` - Return holdings only
* `POST /v1/portfolios/{portfolio_id}/transactions/buy` - Buy shares and update weighted average cost basis
* `POST /v1/portfolios/{portfolio_id}/transactions/sell` - Sell shares and reject oversells
* `POST /v1/portfolios/{portfolio_id}/dividends` - Record a dividend and credit the cash balance
* `GET /v1/portfolios/{portfolio_id}/dividends` - List dividends grouped by symbol

## What AI Produced

* Project folder structure
* Portfolio, transaction, dividend, and holding models
* Request and response schemas
* Repository and service layers
* API routers for all portfolio, transaction, and dividend endpoints
* Global error handling
* Alembic setup and migration support
* Basic tests
* Response messages for portfolio create, balance add, buy, sell, and dividend create endpoints

## What I Kept / Changed

**Kept:**

* Layered architecture
* UUID as primary key
* Decimal for money
* PostgreSQL setup

**Changed:**

* Avoided SQLite for testing
* Simplified project entrypoint
* Documented the full endpoint set instead of only the main write operations

## My Design Decision

* Avoided SQLite-based tests

## Time Split

* Coding: 20%
* Prompting: 30%
* Review: 20%
* Debugging: 20%
* Testing: 15%
* Docs: 5%
