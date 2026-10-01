import uuid
from datetime import date, datetime
from typing import Optional
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
    status: str
    join_date: Optional[date]
    is_active: bool
    created_at: datetime