from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse
from application.exceptions import NotFoundException, ValidationException, ApplicationException


def register_exception_handlers(app: FastAPI) -> None:
    """
    .NET'dagi `app.UseExceptionHandler()` ekvivalenti.
    Barcha xatoliklarni bitta joyda tutib, standart formatda qaytaradi.
    """

    # 1. 404 Not Found xatolarini tutish
    @app.exception_handler(NotFoundException)
    async def not_found_handler(request: Request, exc: NotFoundException) -> JSONResponse:
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={
                "type": "https://tools.ietf.org/html/rfc7231#section-6.5.4",
                "title": "Not Found",
                "status": 404,
                "detail": exc.message,
                "instance": str(request.url.path),
            },
        )

    # 2. 400 Validation xatolarini tutish
    @app.exception_handler(ValidationException)
    async def validation_handler(request: Request, exc: ValidationException) -> JSONResponse:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={
                "type": "https://tools.ietf.org/html/rfc7231#section-6.5.1",
                "title": "Bad Request",
                "status": 400,
                "detail": exc.message,
                "instance": str(request.url.path),
            },
        )

    # 3. Kutilmagan boshqa barcha server xatolarini (500) tutish
    @app.exception_handler(Exception)
    async def global_exception_handler(request: Request, exc: Exception) -> JSONResponse:
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={
                "type": "https://tools.ietf.org/html/rfc7231#section-6.6.1",
                "title": "Internal Server Error",
                "status": 500,
                "detail": "Kutilmagan server xatoligi yuz berdi.",
                "error": str(exc),
                "instance": str(request.url.path),
            },
        )