from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware  
from webapi.config import settings
from webapi.controllers.v1.router import api_router
from webapi.middlewares.error_handler import register_exception_handlers


def create_app() -> FastAPI:
    app = FastAPI(
        title=settings.PROJECT_NAME,
        debug=settings.DEBUG,
    )

    app.add_middleware(
        CORSMiddleware,
        allow_origins=[
            "http://localhost:3000",  
            "http://localhost:5173",  
            "http://127.0.0.1:3000",
            "http://127.0.0.1:5173",
        ],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    register_exception_handlers(app)

    app.include_router(api_router, prefix=settings.API_V1_PREFIX)

    return app


app = create_app()


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)