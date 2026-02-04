from fastapi import FastAPI

from presentation.api.v1.routes import auth, companies, users
from presentation.api.v1.middlewares.rate_limit import RateLimitMiddleware


def create_app() -> FastAPI:
    app = FastAPI(title="MachWork API", version="1.0.0")
    app.add_middleware(RateLimitMiddleware)
    app.include_router(auth.router, prefix="/api/v1")
    app.include_router(users.router, prefix="/api/v1")
    app.include_router(companies.router, prefix="/api/v1")
    return app


app = create_app()
