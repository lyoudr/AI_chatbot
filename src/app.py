from routes import chatbot, authenticate, tasks
from settings import get_settings
from cassandra_database import get_cassandra_session

from fastapi import FastAPI, Request  # noqa: E402
from fastapi.middleware.cors import CORSMiddleware  # noqa: E402
from fastapi.middleware.gzip import GZipMiddleware  # noqa: E402
from starlette.middleware.base import BaseHTTPMiddleware
from cassandra.cluster import Session 
import logging
import uuid 

settings = get_settings()

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class LogRequestMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        # Log request body (if applicable)
        body = await request.body()
        
        # Call the next middleware or route handler
        response = await call_next(request)

        log_id = uuid.uuid4()
        method = request.method 
        url = str(request.url)
        body_content = body.decode() if body else None 
        status_code = response.status_code 

        # Get Cassandra session (logging into Cassandra)
        session: Session = get_cassandra_session()

        # Insert the log entry into Cassandra (assuming the 'request_logs' table is created)
        log_query = """
        INSERT INTO request_logs (log_id, request_method, request_url, request_body, response_status_code)
        VALUES (%s, %s, %s, %s, %s)
        """ 
        try:
            session.execute(log_query, (log_id, method, url, body_content, status_code))
            logger.info(f"Logged request: {method} {url} with status code {status_code}")
        except Exception as e:
            logger.error(f"Failed to log request to Cassandra: {e}")
        
        return response 
    
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
app.add_middleware(LogRequestMiddleware)

# include router
app.include_router(chatbot.router)
app.include_router(authenticate.router)
app.include_router(tasks.router)
