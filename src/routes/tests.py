import sys 
sys.path.append("src")

from utils.rate_limit import limiter
from fastapi import APIRouter, Request

router = APIRouter(prefix="/secure")


@router.get(
    "/",
    tags = ["tests"]
)
@limiter.limit("5/minute")
async def secure_endpoint(request: Request):
    return {"message": "This endpoint is rate-limiting."}