from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

from auth.functions.decode_token import decode_access_token

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


async def get_user_or_error(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="توکن یافت نشد",
    )

    payload = decode_access_token(token)

    if payload is None:
        raise credentials_exception
    return payload
