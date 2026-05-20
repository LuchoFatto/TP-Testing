from typing import Dict, Optional

from fastapi import Header, HTTPException

from app.services.user_service import UserService



def build_token(username: str) -> str:
    return f"token-{username}"



def parse_token(token: str) -> Optional[str]:
    prefix = "token-"
    if not token.startswith(prefix):
        return None
    return token[len(prefix):]



def get_current_user(authorization: Optional[str] = Header(default=None)) -> Dict:
    if authorization is None:
        raise HTTPException(status_code=401, detail="Authorization header is required")

    parts = authorization.split(" ", 1)
    token = parts[1] if len(parts) == 2 and parts[0].lower() == "bearer" else authorization
    username = parse_token(token)

    if username is None:
        raise HTTPException(status_code=401, detail="Invalid token")

    user = UserService.get_user(username)
    if user is None:
        raise HTTPException(status_code=401, detail="Invalid token")

    return user
