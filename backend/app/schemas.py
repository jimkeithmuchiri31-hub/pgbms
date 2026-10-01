import uuid
from datetime import date, datetime
from typing import Optional, List
from pydantic import BaseModel, ConfigDict


class LoginRequest(BaseModel):
    username: str
    password: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    must_change_password: bool


class ChangePasswordRequest(BaseModel):
    current_password: str
    new_password: str


class MemberCreate(BaseModel):
    brigade_number: str
    first_name: str
    middle_name: Optional[str] = None
    last_name: str
    date_of_birth: Optional[date] = None
    gender: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[str] = None
    address: Optional[str] = None
    school: Optional[str] = None
    school_class: Optional[str] = None
    church_group: Optional[str] = None
    membership_type: Optional[str] = None
    member_category: str = "brigadier"
    program_branch: Optional[str] = None
    join_date: Optional[date] = None


class MemberUpdate(BaseModel):
    first_name: Optional[str] = None
    middle_name: Optional[str] = None
    last_name: Optional[str] = None
    date_of_birth: Optional[date] = None
    gender: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[str] = None
    address: Optional[str] = None
    school: Optional[str] = None
    school_class: Optional[str] = None
    church_group: Optional[str] = None
    membership_type: Optional[str] = None
    program_branch: Optional[str] = None
    member_category: Optional[str] = None
    status: Optional[str] = None


class MemberOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    brigade_number: str
    first_name: str
    middle_name: Optional[str]
    last_name: str
    date_of_birth: Optional[date]
    gender: Optional[str]
    phone: Optional[str]
    email: Optional[str]
    address: Optional[str]
    school: Optional[str]
    school_class: Optional[str]
    church_group: Optional[str]
    membership_type: Optional[str]
    member_category: str
    program_branch: Optional[str]
    status: str
    join_date: Optional[date]
    is_active: bool
    created_at: datetime


class MeetingTypeOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: uuid.UUID
    name: str


class AttendanceMark(BaseModel):
    member_id: uuid.UUID
    status: str
    remarks: Optional[str] = None


class AttendanceBulkCreate(BaseModel):
    meeting_type_id: uuid.UUID
    date: date
    records: List[AttendanceMark]


class AttendanceOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: uuid.UUID
    member_id: uuid.UUID
    meeting_type_id: uuid.UUID
    date: date
    status: str
    remarks: Optional[str]
    created_at: datetime


class CourseCreate(BaseModel):
    name: str
    description: Optional[str] = None
    category: Optional[str] = None


class CourseOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: uuid.UUID
    name: str
    description: Optional[str]
    category: Optional[str]


class TrainingRecordCreate(BaseModel):
    member_id: uuid.UUID
    course_id: uuid.UUID
    trainer_name: Optional[str] = None
    start_date: Optional[date] = None


class TrainingRecordUpdate(BaseModel):
    end_date: Optional[date] = None
    score: Optional[str] = None
    remarks: Optional[str] = None
    status: Optional[str] = None


class TrainingRecordOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: uuid.UUID
    member_id: uuid.UUID
    course_id: uuid.UUID
    trainer_name: Optional[str]
    start_date: Optional[date]
    end_date: Optional[date]
    score: Optional[str]
    status: str
    created_at: datetime


class BadgeCreate(BaseModel):
    name: str
    description: Optional[str] = None
    requirements: Optional[str] = None


class BadgeOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: uuid.UUID
    name: str
    description: Optional[str]
    requirements: Optional[str]


class MemberBadgeAward(BaseModel):
    member_id: uuid.UUID
    badge_id: uuid.UUID
    awarded_date: Optional[date] = None


class MemberBadgeOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: uuid.UUID
    member_id: uuid.UUID
    badge_id: uuid.UUID
    awarded_date: Optional[date]


class CertificateCreate(BaseModel):
    member_id: uuid.UUID
    course_id: Optional[uuid.UUID] = None
    issue_date: Optional[date] = None


class CertificateOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: uuid.UUID
    member_id: uuid.UUID
    course_id: Optional[uuid.UUID]
    certificate_number: str
    issue_date: Optional[date]
    verification_code: Optional[str]