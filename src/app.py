from routes import chatbot
from settings import get_settings

from fastapi import FastAPI, Response  # noqa: E402
from fastapi.middleware.cors import CORSMiddleware  # noqa: E402
from fastapi.middleware.gzip import GZipMiddleware  # noqa: E402
from fastapi.staticfiles import StaticFiles  # noqa: E402

settings = get_settings()

app = FastAPI(
    title=f"FastAPI - {settings.APP_ENV}",
    docs_url="/docs" if settings.DOCS else None,
    description="FastAPI Documentation",
    version=settings.APP_VERSION,
    swagger_ui_parameters={
        "persistAuthorization": True,
        "tryItOutEnabled": True,
    },
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["Content-Disposition", "X-Internal-User-Email"],
)
app.add_middleware(GZipMiddleware, minimum_size=500)
# include router
app.include_router(chatbot.router)