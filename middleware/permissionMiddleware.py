from fastapi import Request, HTTPException
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware
from auth.functions.decode_token import decode_access_token
from shared.classes.authorization_manager import AuthorizationManager


authManager = AuthorizationManager()

whiteList = [
    {"url": "/openapi.json", "method": "GET"},
]


class PermissionMiddleware(BaseHTTPMiddleware):
    def __init__(self, app):
        super().__init__(app)

    async def dispatch(self, request: Request, call_next):
        path = request.url.path
        method = request.method

        user_token = request.headers.get("Authorization")

        if not user_token:
            return await call_next(request)

        payload = decode_access_token(user_token.split(" ")[1])

        # first try: "path" matched exactly
        if authManager.hasAccess(path, method, payload["roleId"]):
            return await call_next(request)

        # second try: "path" matched with dynamic part
        elif authManager.hasAccess(path, method, payload["roleId"], dynamic=True):
            return await call_next(request)

        # third try: if not found in permissions, check whitelist
        for item in whiteList:
            if item["url"] == path and item["method"] == method:
                return await call_next(request)

        return JSONResponse(status_code=403, content={"detail": "عدم دسترسی"})
