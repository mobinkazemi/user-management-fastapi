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

class DBRateLimitMiddleware(BaseHTTPMiddleware):
    def __init__(self, app):
        super().__init__(app)

    async def dispatch(self, request: Request, call_next):
        try:
            path = request.url.path
            user_token = request.headers.get("Authorization")
            if user_token and bool(decode_access_token(user_token.split(" ")[1])["mustChangePassword"]) :
                
                redirect_url = "localhost:8000/auth/login"
                return JSONResponse(
                    status_code=403,
                    content={"detail": "Password change required", "redirect": redirect_url}
                )

            if (not request.headers.get("Authorization") ):
                # محدودیت 10 درخواست در دقیقه برای لاگین
                client_ip = request.headers.get("X-Forwarded-For", request.client.host)
                self.enforce_rate_limit_with_ip(client_ip,10, window=60) 
                return await call_next(request)
            

            else:
                try:
                    auth_header = request.headers.get("Authorization")
                    if not auth_header:
                        raise HTTPException(status_code=401, detail="Authorization header missing")

                    # دیکود توکن
                    user_data = decode_access_token(auth_header.split(" ")[1]) if " " in auth_header else decode_access_token(auth_header)

                    if not user_data or "id" not in user_data:
                        raise HTTPException(status_code=401, detail="Invalid or expired token")

                    # گرفتن اطلاعات کاربر از دیتابیس
                    user = user_repo.findOne(id=user_data["id"])

                    if not user:
                        raise HTTPException(status_code=404, detail="User not found")
                    role = role_repo.findOne(id=user.get("userRoleId"))
                    if not role:
                        raise HTTPException(status_code=404, detail="Role not found")
                    # محدودیت درخواست در دقیقه
                    request_limit = role.get("maxRequestPerMinute")
                    user_token = auth_header.split(" ")[1]
                    if not user_token:
                        raise HTTPException(status_code=400, detail="User token not found")

                    # اعمال محدودیت
                    self.enforce_rate_limit(user_token, request_limit)

                    return await call_next(request)
                except HTTPException as http_exc:
                    # تبدیل به JSONResponse
                    return JSONResponse(
                        status_code=http_exc.status_code,
                        content={"detail": http_exc.detail}
                    )
        except HTTPException as http_exc:
            # تبدیل به JSONResponse
            return JSONResponse(
                status_code=http_exc.status_code,
                content={"detail": http_exc.detail}
            )     
    def enforce_rate_limit(self, key: str, limit: int, window: int = 60):
        
        now = int(time.time())
        window_start = now - (now % window)
        redis_key = f"ratelimit:{key}:{window_start}"

        try:
            current = redis_client.incr(redis_key)
            if current == 1:
                redis_client.expire(redis_key, window)
            if current > limit:
                raise HTTPException(status_code=429, detail="Too many requests")
        except redis.RedisError as e:
            raise HTTPException(status_code=500, detail="Redis error: " + str(e))


    def enforce_rate_limit_with_ip(self, ip: str, limit: int, window: int = 60):
        now = int(time.time())
        window_start = now - (now % window)
        redis_key = f"ratelimit:ip:{ip}:{window_start}"
        try:
            current = redis_client.incr(redis_key)
            if current == 1:
                redis_client.expire(redis_key, window)
            if current > limit:
                raise HTTPException(status_code=429, detail="Too many requests from this IP")
        except redis.RedisError as e:
            raise HTTPException(status_code=500, detail="Redis error: " + str(e))