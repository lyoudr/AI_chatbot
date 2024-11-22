from slowapi.util import get_remote_address
from slowapi import Limiter 

# Rate Limit
limiter = Limiter(key_func=get_remote_address)