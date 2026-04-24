from fastapi import FastAPI, HTTPException, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from app.api.v1.routers.portfolios import router as portfolios_router
from app.core.config import get_settings
from app.exceptions.base import AppException
from app.schemas.common import ErrorDetail, ErrorResponse

settings = get_settings()

app = FastAPI(title=settings.app_name)
app.include_router(portfolios_router)


@app.exception_handler(RequestValidationError)
def validation_exception_handler(_: Request, exc: RequestValidationError) -> JSONResponse:
    details = [
        ErrorDetail(
            field=".".join(str(part) for part in item["loc"] if part != "body"),
            message=item["msg"],
        )
        for item in exc.errors()
    ]
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content=ErrorResponse(error="validation_error", details=details).model_dump(mode="json"),
    )


@app.exception_handler(HTTPException)
def http_exception_handler(_: Request, exc: HTTPException) -> JSONResponse:
    return JSONResponse(
        status_code=exc.status_code,
        content=ErrorResponse(error="http_error", details=[ErrorDetail(message=str(exc.detail))]).model_dump(mode="json", exclude_none=True),
    )


@app.exception_handler(AppException)
def app_exception_handler(_: Request, exc: AppException) -> JSONResponse:
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content=ErrorResponse(
            error=exc.code,
            details=[ErrorDetail(field=item.get("field"), message=item.get("message", "")) for item in exc.details] or None,
        ).model_dump(mode="json", exclude_none=True),
    )


@app.exception_handler(Exception)
def generic_exception_handler(_: Request, __: Exception) -> JSONResponse:
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content=ErrorResponse(error="internal_server_error", details=[ErrorDetail(message="An unexpected error occurred")]).model_dump(mode="json", exclude_none=True),
    )
