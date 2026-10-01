from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import JWTError
from sqlalchemy.orm import Session

from app.database import get_db
from app.security import decode_token
from app import models

bearer_scheme = HTTPBearer()


def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
    db: Session = Depends(get_db),
) -> models.User:
    token = credentials.credentials
    try:
        payload = decode_token(token)
        if payload.get("type") != "access":
            raise HTTPException(status_code=401, detail="Invalid token type")
        user_id = payload.get("sub")
    except JWTError:
        raise HTTPException(status_code=401, detail="Could not validate credentials")

    user = db.query(models.User).filter(models.User.id == user_id).first()
    if user is None or not user.is_active:
        raise HTTPException(status_code=401, detail="User not found or inactive")
    return user


def require_permission(module: str, action: str):
    def checker(
        current_user: models.User = Depends(get_current_user),
        db: Session = Depends(get_db),
    ) -> models.User:
        if current_user.role.name == "SUPER_ADMIN":
            return current_user

        has_permission = (
            db.query(models.RolePermission)
            .join(models.Permission)
            .filter(
                models.RolePermission.role_id == current_user.role_id,
                models.Permission.module == module,
                models.Permission.action == action,
            )
            .first()
        )
        if not has_permission:
            raise HTTPException(status_code=403, detail="Not enough permissions")
        return current_user
    return checker