from fastapi import APIRouter, HTTPException

from app.dependencies.auth import build_token
from app.schemas import LoginRequest, RegisterRequest
from app.services.user_service import UserService


router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/register")
def register(payload: RegisterRequest):
    try:
        user = UserService.register_customer(payload.username, payload.password)
        return {
            "message": "User registered successfully",
            "user": {"username": user["username"], "role": user["role"]},
        }
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc))


@router.post("/login")
def login(payload: LoginRequest):
    user = UserService.authenticate(payload.username, payload.password)
    if user is None:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = build_token(user["username"])
    return {
        "message": "Login successful",
        "token": token,
        "user": {"username": user["username"], "role": user["role"]},
    }
