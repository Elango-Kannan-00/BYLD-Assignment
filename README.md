# BYLD Portfolio API

## POST /v1/portfolios

### Request
```json
{
  "clientName": "Aarav Mehta",
  "riskProfile": "balanced"
}
```

### Response
```json
{
  "id": "8d5a6d8d-7f0e-4f56-9f63-8b9d9e4a9d11",
  "clientName": "Aarav Mehta",
  "riskProfile": "balanced",
  "cashBalance": "0.00"
}
```

### Flow
Router -> Service -> Repository -> PostgreSQL via SQLAlchemy 2.0, with DTOs handled by Pydantic and money stored as `Decimal` / `NUMERIC`.

## Run

```powershell
python -m alembic upgrade head
uvicorn main:app --reload
```
