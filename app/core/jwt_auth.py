import json
import os
from datetime import datetime, timedelta

from fastapi import Depends, HTTPException, status
from pytz import timezone
from jose import jwt
from jose.exceptions import ExpiredSignatureError
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from app.schemas.requests.authentication_requests import UserJWTData

security = HTTPBearer()


def create_access_token(user_data: dict, algorithm: str = "HS256") -> str:
    now = datetime.now(tz=timezone("America/Sao_Paulo"))

    sub = {
        "email": user_data.get("email"),
        "user_id": user_data.get("user_id")
    }

    payload = {
        "type": "access_token",
        "exp": now + timedelta(hours=24),
        "iat": now,
        "sub": json.dumps(sub)
    }

    return jwt.encode(payload, os.getenv("JWT_SECRET"), algorithm=algorithm)


def decode_access_token(credentials: HTTPAuthorizationCredentials = Depends(security)) -> UserJWTData:
    token = credentials.credentials
    try:
        payload = jwt.decode(token, os.getenv("JWT_SECRET"), algorithms=["HS256"])
        return UserJWTData(**json.loads(payload.get("sub")))
    except ExpiredSignatureError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token expirado.")
    except Exception:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token inválido.")
