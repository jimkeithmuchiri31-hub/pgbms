import uuid
from datetime import date as date_type
from typing import Optional, List

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.database import get_db
from app import models
from app.schemas import (
    CourseCreate, CourseOut,
    TrainingRecordCreate, TrainingRecordUpdate, TrainingRecordOut,
    BadgeCreate, BadgeOut, MemberBadgeAward, MemberBadgeOut,
    CertificateCreate, CertificateOut,
)
from app.deps import require_permission
from app.certificates import generate_certificate_number, generate_verification_code

router = APIRouter(prefix="/api/v1/training", tags=["training"])


@router.get("/courses", response_model=List[CourseOut])
def list_courses(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(require_permission("training", "view")),
):
    return db.query(models.Course).order_by(models.Course.name).all()


@router.post("/courses", response_model=CourseOut, status_code=201)
def create_course(
    payload: CourseCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(require_permission("training", "create")),
):
    course = models.Course(**payload.model_dump())
    db.add(course)
    db.commit()
    db.refresh(course)
    return course


@router.get("/records", response_model=List[TrainingRecordOut])
def list_training_records(
    member_id: Optional[uuid.UUID] = Query(None),
    course_id: Optional[uuid.UUID] = Query(None),
    db: Session = Depends(get_db),
    current_user: models.User = Depends(require_permission("training", "view")),
):
    query = db.query(models.TrainingRecord)
    if member_id:
        query = query.filter(models.TrainingRecord.member_id == member_id)
    if course_id:
        query = query.filter(models.TrainingRecord.course_id == course_id)
    return query.order_by(models.TrainingRecord.created_at.desc()).all()


@router.post("/records", response_model=TrainingRecordOut, status_code=201)
def enroll_member(
    payload: TrainingRecordCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(require_permission("training", "create")),
):
    if not db.query(models.Member).filter(models.Member.id == payload.member_id).first():
        raise HTTPException(status_code=404, detail="Member not found")
    if not db.query(models.Course).filter(models.Course.id == payload.course_id).first():
        raise HTTPException(status_code=404, detail="Course not found")

    record = models.TrainingRecord(**payload.model_dump())
    db.add(record)
    db.commit()
    db.refresh(record)

    db.add(models.AuditLog(
        user_id=current_user.id, action="training.enrolled",
        entity_type="training_record", entity_id=record.id,
    ))
    db.commit()
    return record


@router.put("/records/{record_id}", response_model=TrainingRecordOut)
def update_training_record(
    record_id: uuid.UUID,
    payload: TrainingRecordUpdate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(require_permission("training", "edit")),
):
    record = db.query(models.TrainingRecord).filter(models.TrainingRecord.id == record_id).first()
    if not record:
        raise HTTPException(status_code=404, detail="Training record not found")

    for field, value in payload.model_dump(exclude_unset=True).items():
        setattr(record, field, value)
    db.commit()
    db.refresh(record)

    db.add(models.AuditLog(
        user_id=current_user.id, action="training.updated",
        entity_type="training_record", entity_id=record.id,
    ))
    db.commit()
    return record


@router.get("/badges", response_model=List[BadgeOut])
def list_badges(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(require_permission("training", "view")),
):
    return db.query(models.Badge).order_by(models.Badge.name).all()


@router.post("/badges", response_model=BadgeOut, status_code=201)
def create_badge(
    payload: BadgeCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(require_permission("training", "create")),
):
    badge = models.Badge(**payload.model_dump())
    db.add(badge)
    db.commit()
    db.refresh(badge)
    return badge


@router.post("/badges/award", response_model=MemberBadgeOut, status_code=201)
def award_badge(
    payload: MemberBadgeAward,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(require_permission("training", "edit")),
):
    if not db.query(models.Member).filter(models.Member.id == payload.member_id).first():
        raise HTTPException(status_code=404, detail="Member not found")
    if not db.query(models.Badge).filter(models.Badge.id == payload.badge_id).first():
        raise HTTPException(status_code=404, detail="Badge not found")

    award = models.MemberBadge(
        member_id=payload.member_id,
        badge_id=payload.badge_id,
        awarded_date=payload.awarded_date or date_type.today(),
        awarded_by=current_user.id,
    )
    db.add(award)
    db.commit()
    db.refresh(award)

    db.add(models.AuditLog(
        user_id=current_user.id, action="badge.awarded",
        entity_type="member_badge", entity_id=award.id,
    ))
    db.commit()
    return award


@router.get("/badges/member/{member_id}", response_model=List[MemberBadgeOut])
def list_member_badges(
    member_id: uuid.UUID,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(require_permission("training", "view")),
):
    return db.query(models.MemberBadge).filter(models.MemberBadge.member_id == member_id).all()


@router.get("/certificates", response_model=List[CertificateOut])
def list_certificates(
    member_id: Optional[uuid.UUID] = Query(None),
    db: Session = Depends(get_db),
    current_user: models.User = Depends(require_permission("training", "view")),
):
    query = db.query(models.Certificate)
    if member_id:
        query = query.filter(models.Certificate.member_id == member_id)
    return query.order_by(models.Certificate.created_at.desc()).all()


@router.post("/certificates", response_model=CertificateOut, status_code=201)
def issue_certificate(
    payload: CertificateCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(require_permission("training", "create")),
):
    if not db.query(models.Member).filter(models.Member.id == payload.member_id).first():
        raise HTTPException(status_code=404, detail="Member not found")

    issue_date = payload.issue_date or date_type.today()
    certificate = models.Certificate(
        member_id=payload.member_id,
        course_id=payload.course_id,
        certificate_number=generate_certificate_number(issue_date.year),
        issue_date=issue_date,
        issued_by=current_user.id,
        verification_code=generate_verification_code(),
    )
    db.add(certificate)
    db.commit()
    db.refresh(certificate)

    db.add(models.AuditLog(
        user_id=current_user.id, action="certificate.issued",
        entity_type="certificate", entity_id=certificate.id,
    ))
    db.commit()
    return certificate