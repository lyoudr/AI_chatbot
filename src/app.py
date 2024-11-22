from routes import chatbot, authenticate, tasks, tests
from utils.rate_limit import limiter
from settings import get_settings
from cassandra_database import get_cassandra_session

from fastapi import FastAPI, Request, HTTPException  # noqa: E402
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

# Logging Middleware
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

# WAF Middleware
"""
1. Inspect headers, query parameters, and payloads for malicious content.
2. Block suspicious IPs.
3. Rate-limit requests to prevent DoS attacks.
"""
class WAFMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        # Example: Block requests with suspicious headers
        if "X-Suspicious-Header" in request.headers:
            raise HTTPException(status_code = 403, detail="Forbidden: Suspicious header detected.")
        
        # Example: Block IP addresses
        blocked_ips = {"192.168.1.1"}
        client_ip = request.client.host 
        if client_ip in blocked_ips:
            raise HTTPException(status_code=403, detail="Forbidden: Your IP is blocked.")
        
        # Example: Check for malicious payloads
        if request.method == "POST":
            body = await request.body()
            if b"<script>" in body: # Detect potential XSS
                raise HTTPException(status_code=403, detail="Forbidden: Malicious payload detected.")

        return await call_next(request)

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
app.add_middleware(WAFMiddleware)

# include router
app.include_router(chatbot.router)
app.include_router(authenticate.router)
app.include_router(tasks.router)
app.include_router(tests.router)


app.state.limiter = limiter

