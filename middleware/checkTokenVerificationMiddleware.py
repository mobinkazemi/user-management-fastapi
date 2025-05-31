from fastapi import Request, HTTPException
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware
import redis
import time
from auth.functions.decode_token import decode_access_token
from roles.repository import RoleRepository
from users.repository import UserRepository


from db.redis import redis_client

user_repo = UserRepository()
role_repo = RoleRepository()

class checkTokenVerificationMiddleware(BaseHTTPMiddleware):
    def __init__(self, app):
        super().__init__(app)

    async def dispatch(self, request: Request, call_next):
        try:
            path = request.url.path
            if request.method == "POST" and path == "/auth/login":     
                return await call_next(request)
            user_token = request.headers.get("Authorization")
            try:
                userId = decode_access_token(user_token.split(" ")[1])["id"] if user_token else None
            except Exception as e:
                raise HTTPException(status_code=401, detail="token is invalid or expired")
            if not user_token:
                raise HTTPException(status_code=401, detail="Authorization header missing") 
            if not userId:
                raise HTTPException(status_code=401, detail="Invalid or expired token")
            redisToken = redis_client.get(f"USER_LOGGED_IN:{userId}")
            if redisToken != user_token.split(" ")[1]:
                raise HTTPException(status_code=401, detail="Invalid or expired token")
        except HTTPException as http_exc:
            # تبدیل به JSONResponse
            return JSONResponse(
                status_code=http_exc.status_code,
                content={"detail": http_exc.detail}
            )   
        return await call_next(request)  
