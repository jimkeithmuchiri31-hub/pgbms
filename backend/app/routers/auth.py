import os
from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException, Request, Response
from jose import JWTError
from sqlalchemy.orm import Session

from app.database import get_db
from app import models
from app.schemas import LoginRequest, TokenResponse, ChangePasswordRequest
from app.security import verify_password, hash_password, create_access_token, create_refresh_token, decode_token
from app.deps import get_current_user
from app.rate_limit import limiter

router = APIRouter(prefix="/api/v1/auth", tags=["auth"])

REFRESH_COOKIE_NAME = "refresh_token"
IS_PRODUCTION = os.getenv("ENVIRONMENT") == "production"


def set_refresh_cookie(response: Response, token: str):
    response.set_cookie(
        key=REFRESH_COOKIE_NAME,
        value=token,
        httponly=True,
        secure=IS_PRODUCTION,
        samesite="lax",
        max_age=7 * 24 * 60 * 60,
        path="/api/v1/auth",
    )


@router.post("/login", response_model=TokenResponse)
@limiter.limit("5/minute")
def login(request: Request, response: Response, payload: LoginRequest, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.username == payload.username).first()
    if not user or not verify_password(payload.password, user.password_hash):
        raise HTTPException(status_code=401, detail="Invalid username or password")
    if not user.is_active:
        raise HTTPException(status_code=401, detail="Account is deactivated")

    user.last_login_at = datetime.utcnow()
    db.commit()

    access_token = create_access_token({"sub": str(user.id), "role_id": str(user.role_id)})
    refresh_token = create_refresh_token({"sub": str(user.id)})
    set_refresh_cookie(response, refresh_token)

    return TokenResponse(access_token=access_token, must_change_password=user.must_change_password)


@router.post("/refresh", response_model=TokenResponse)
def refresh(request: Request, response: Response, db: Session = Depends(get_db)):
    token = request.cookies.get(REFRESH_COOKIE_NAME)
    if not token:
        raise HTTPException(status_code=401, detail="No refresh token provided")

    try:
        payload = decode_token(token)
        if payload.get("type") != "refresh":
            raise HTTPException(status_code=401, detail="Invalid token type")
        user_id = payload.get("sub")
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid or expired refresh token")

    user = db.query(models.User).filter(models.User.id == user_id).first()
    if user is None or not user.is_active:
        raise HTTPException(status_code=401, detail="User not found or inactive")

    new_access_token = create_access_token({"sub": str(user.id), "role_id": str(user.role_id)})
    new_refresh_token = create_refresh_token({"sub": str(user.id)})
    set_refresh_cookie(response, new_refresh_token)

    return TokenResponse(access_token=new_access_token, must_change_password=user.must_change_password)


@router.post("/logout")
def logout(response: Response):
    response.delete_cookie(key=REFRESH_COOKIE_NAME, path="/api/v1/auth")
    return {"detail": "Logged out"}


@router.post("/change-password")
def change_password(
    payload: ChangePasswordRequest,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    if not verify_password(payload.current_password, current_user.password_hash):
        raise HTTPException(status_code=400, detail="Current password is incorrect")

    current_user.password_hash = hash_password(payload.new_password)
    current_user.must_change_password = False
    db.commit()
    return {"detail": "Password updated"}


@router.get("/me")
def get_me(current_user: models.User = Depends(get_current_user)):
    return {
        "id": str(current_user.id),
        "username": current_user.username,
        "role": current_user.role.name,
        "must_change_password": current_user.must_change_password,
        "program_branch": current_user.member.program_branch if current_user.member else None,
    }