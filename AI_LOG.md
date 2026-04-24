
## AI Used

* Codex (OpenAI)

## Prompt

Asked AI to:

* Build a FastAPI backend for a portfolio system
* Create project structure
* Implement POST /v1/portfolios
* Set up PostgreSQL + Alembic
* Add tests and dependencies

## What AI Produced

* Project folder structure
* Portfolio model, schema, repository, service, router
* Global error handling
* Alembic setup and migration
* Basic tests

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

* Coding: 30%
* Prompting: 10%
* Review: 20%
* Debugging: 20%
* Testing: 15%
* Docs: 5%
