import uuid
from datetime import date as date_type
from typing import Optional, List

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.database import get_db
from app import models
from app.schemas import AttendanceBulkCreate, AttendanceOut, MeetingTypeOut
from app.deps import require_permission

router = APIRouter(prefix="/api/v1/attendance", tags=["attendance"])


@router.get("/meeting-types", response_model=List[MeetingTypeOut])
def list_meeting_types(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(require_permission("attendance", "view")),
):
    return db.query(models.MeetingType).order_by(models.MeetingType.name).all()


@router.post("/bulk", response_model=List[AttendanceOut])
def mark_attendance_bulk(
    payload: AttendanceBulkCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(require_permission("attendance", "create")),
):
    meeting_type = db.query(models.MeetingType).filter(models.MeetingType.id == payload.meeting_type_id).first()
    if not meeting_type:
        raise HTTPException(status_code=404, detail="Meeting type not found")

    results = []
    for entry in payload.records:
        existing = (
            db.query(models.AttendanceRecord)
            .filter(
                models.AttendanceRecord.member_id == entry.member_id,
                models.AttendanceRecord.meeting_type_id == payload.meeting_type_id,
                models.AttendanceRecord.date == payload.date,
            )
            .first()
        )
        if existing:
            existing.status = entry.status
            existing.remarks = entry.remarks
            existing.recorded_by = current_user.id
            record = existing
        else:
            record = models.AttendanceRecord(
                member_id=entry.member_id,
                meeting_type_id=payload.meeting_type_id,
                date=payload.date,
                status=entry.status,
                remarks=entry.remarks,
                recorded_by=current_user.id,
            )
            db.add(record)
        results.append(record)

    db.commit()
    for r in results:
        db.refresh(r)

    db.add(models.AuditLog(
        user_id=current_user.id, action="attendance.bulk_marked",
        entity_type="meeting_type", entity_id=payload.meeting_type_id,
        details={"date": str(payload.date), "count": len(results)},
    ))
    db.commit()

    return results


@router.get("", response_model=List[AttendanceOut])
def list_attendance(
    member_id: Optional[uuid.UUID] = Query(None),
    meeting_type_id: Optional[uuid.UUID] = Query(None),
    date_from: Optional[date_type] = Query(None),
    date_to: Optional[date_type] = Query(None),
    db: Session = Depends(get_db),
    current_user: models.User = Depends(require_permission("attendance", "view")),
):
    query = db.query(models.AttendanceRecord)
    if member_id:
        query = query.filter(models.AttendanceRecord.member_id == member_id)
    if meeting_type_id:
        query = query.filter(models.AttendanceRecord.meeting_type_id == meeting_type_id)
    if date_from:
        query = query.filter(models.AttendanceRecord.date >= date_from)
    if date_to:
        query = query.filter(models.AttendanceRecord.date <= date_to)

    return query.order_by(models.AttendanceRecord.date.desc()).limit(500).all()s