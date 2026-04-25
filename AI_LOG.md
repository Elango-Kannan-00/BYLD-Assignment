
## AI Used

* Codex (OpenAI)

## Prompt

Asked AI to:

* Build a FastAPI backend for a portfolio system
* Create project structure
* Implement REST API for all the necessary endpoints
* Set up PostgreSQL + Alembic
* Add tests and dependencies

## What AI Produced

* Project folder structure
* Portfolio model, schema, repository, service, router
* Global error handling
* Alembic setup and migration
* Basic tests
* POST /v1/portfolios/{portfolio_id}/balance
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

## My Design Decision

* Avoided SQLite-based tests

## Time Split

* Coding: 20%
* Prompting: 30%
* Review: 20%
* Debugging: 20%
* Testing: 15%
* Docs: 5%
