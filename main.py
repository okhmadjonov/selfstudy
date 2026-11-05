from fastapi import FastAPI
from webapi.config import settings
from webapi.controllers.v1.router import api_router
from webapi.middlewares.error_handler import register_exception_handlers  # <-- 1. Import


def create_app() -> FastAPI:
    app = FastAPI(
        title=settings.PROJECT_NAME,
        debug=settings.DEBUG,
    )

    # 2. Global Exception Handler'ni ulash
    register_exception_handlers(app)

    # Controller'larni ro'yxatdan o'tkazish
    app.include_router(api_router, prefix=settings.API_V1_PREFIX)

    return app


app = create_app()


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)