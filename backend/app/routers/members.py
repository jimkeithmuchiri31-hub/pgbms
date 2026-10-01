import uuid
from datetime import datetime
from typing import Optional, List

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import or_

from app.database import get_db
from app import models
from app.schemas import MemberCreate, MemberUpdate, MemberOut
from app.deps import require_permission

router = APIRouter(prefix="/api/v1/members", tags=["members"])


@router.get("", response_model=List[MemberOut])
def list_members(
    search: Optional[str] = Query(None),
    category: Optional[str] = Query(None),
    status: Optional[str] = Query(None),
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db),
    current_user: models.User = Depends(require_permission("members", "view")),
):
    query = db.query(models.Member).filter(models.Member.is_active == True)

    if search:
        like = f"%{search}%"
        query = query.filter(
            or_(
                models.Member.first_name.ilike(like),
                models.Member.last_name.ilike(like),
                models.Member.brigade_number.ilike(like),
            )
        )
    if category:
        query = query.filter(models.Member.member_category == category)
    if status:
        query = query.filter(models.Member.status == status)

    offset = (page - 1) * page_size
    return query.order_by(models.Member.last_name).offset(offset).limit(page_size).all()


@router.post("", response_model=MemberOut, status_code=201)
def create_member(
    payload: MemberCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(require_permission("members", "create")),
):
    existing = db.query(models.Member).filter(models.Member.brigade_number == payload.brigade_number).first()
    if existing:
        raise HTTPException(status_code=400, detail="Brigade number already exists")

    member = models.Member(**payload.model_dump())
    db.add(member)
    db.commit()
    db.refresh(member)

    db.add(models.AuditLog(
        user_id=current_user.id, action="member.created",
        entity_type="member", entity_id=member.id,
    ))
    db.commit()

    return member


@router.get("/{member_id}", response_model=MemberOut)
def get_member(
    member_id: uuid.UUID,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(require_permission("members", "view")),
):
    member = db.query(models.Member).filter(models.Member.id == member_id).first()
    if not member:
        raise HTTPException(status_code=404, detail="Member not found")
    return member


@router.put("/{member_id}", response_model=MemberOut)
def update_member(
    member_id: uuid.UUID,
    payload: MemberUpdate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(require_permission("members", "edit")),
):
    member = db.query(models.Member).filter(models.Member.id == member_id).first()
    if not member:
        raise HTTPException(status_code=404, detail="Member not found")

    for field, value in payload.model_dump(exclude_unset=True).items():
        setattr(member, field, value)
    member.updated_at = datetime.utcnow()
    db.commit()
    db.refresh(member)

    db.add(models.AuditLog(
        user_id=current_user.id, action="member.updated",
        entity_type="member", entity_id=member.id,
    ))
    db.commit()

    return member


@router.delete("/{member_id}")
def deactivate_member(
    member_id: uuid.UUID,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(require_permission("members", "delete")),
):
    member = db.query(models.Member).filter(models.Member.id == member_id).first()
    if not member:
        raise HTTPException(status_code=404, detail="Member not found")

    member.is_active = False
    member.status = "inactive"
    db.commit()

    db.add(models.AuditLog(
        user_id=current_user.id, action="member.deactivated",
        entity_type="member", entity_id=member.id,
    ))
    db.commit()

    return {"detail": "Member deactivated"}v