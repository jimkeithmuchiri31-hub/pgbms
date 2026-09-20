import uuid
from datetime import datetime

from sqlalchemy import (
    Column, String, Boolean, DateTime, Date, ForeignKey, UniqueConstraint, Numeric, Integer, Text
)
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import relationship

from app.database import Base


class Role(Base):
    __tablename__ = "roles"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(50), unique=True, nullable=False)
    description = Column(String(255))
    created_at = Column(DateTime, default=datetime.utcnow)

    permissions = relationship("RolePermission", back_populates="role")
    users = relationship("User", back_populates="role")


class Permission(Base):
    __tablename__ = "permissions"
    __table_args__ = (UniqueConstraint("module", "action", name="uq_module_action"),)

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    module = Column(String(50), nullable=False)
    action = Column(String(50), nullable=False)

    roles = relationship("RolePermission", back_populates="permission")


class RolePermission(Base):
    __tablename__ = "role_permissions"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    role_id = Column(UUID(as_uuid=True), ForeignKey("roles.id"), nullable=False)
    permission_id = Column(UUID(as_uuid=True), ForeignKey("permissions.id"), nullable=False)

    role = relationship("Role", back_populates="permissions")
    permission = relationship("Permission", back_populates="roles")


class Member(Base):
    __tablename__ = "members"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    brigade_number = Column(String(20), unique=True, nullable=False)
    first_name = Column(String(100), nullable=False)
    middle_name = Column(String(100))
    last_name = Column(String(100), nullable=False)
    date_of_birth = Column(Date)
    gender = Column(String(20))
    photo_key = Column(String(255))
    phone = Column(String(30))
    email = Column(String(255))
    address = Column(String(255))
    school = Column(String(150))
    school_class = Column(String(50))
    church_group = Column(String(100))
    membership_type = Column(String(50))
    member_category = Column(String(20), nullable=False, server_default="brigadier")  # 'officer' or 'brigadier'
    status = Column(String(30), default="active")
    join_date = Column(Date)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    guardians = relationship("Guardian", back_populates="member")
    user_account = relationship("User", back_populates="member", uselist=False)


class Guardian(Base):
    __tablename__ = "guardians"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    member_id = Column(UUID(as_uuid=True), ForeignKey("members.id"), nullable=False)
    name = Column(String(150), nullable=False)
    phone = Column(String(30))
    email = Column(String(255))
    relationship_type = Column(String(50))
    is_emergency_contact = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    member = relationship("Member", back_populates="guardians")


class User(Base):
    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    username = Column(String(50), unique=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    role_id = Column(UUID(as_uuid=True), ForeignKey("roles.id"), nullable=False)
    member_id = Column(UUID(as_uuid=True), ForeignKey("members.id"), nullable=True)
    is_active = Column(Boolean, default=True)
    must_change_password = Column(Boolean, default=True)
    last_login_at = Column(DateTime)
    deactivated_at = Column(DateTime)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    role = relationship("Role", back_populates="users")
    member = relationship("Member", back_populates="user_account")


class AuditLog(Base):
    __tablename__ = "audit_logs"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=True)
    action = Column(String(100), nullable=False)
    entity_type = Column(String(50))
    entity_id = Column(UUID(as_uuid=True))
    details = Column(JSONB)
    ip_address = Column(String(45))
    created_at = Column(DateTime, default=datetime.utcnow)


class MeetingType(Base):
    __tablename__ = "meeting_types"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(100), unique=True, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)


class AttendanceRecord(Base):
    __tablename__ = "attendance_records"
    __table_args__ = (
        UniqueConstraint("member_id", "meeting_type_id", "date", name="uq_attendance_member_meeting_date"),
    )

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    member_id = Column(UUID(as_uuid=True), ForeignKey("members.id"), nullable=False)
    meeting_type_id = Column(UUID(as_uuid=True), ForeignKey("meeting_types.id"), nullable=False)
    date = Column(Date, nullable=False)
    status = Column(String(20), nullable=False)
    remarks = Column(String(255))
    recorded_by = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    member = relationship("Member")
    meeting_type = relationship("MeetingType")


class Course(Base):
    __tablename__ = "courses"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(150), nullable=False)
    description = Column(String(500))
    category = Column(String(100))
    created_at = Column(DateTime, default=datetime.utcnow)


class TrainingRecord(Base):
    __tablename__ = "training_records"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    member_id = Column(UUID(as_uuid=True), ForeignKey("members.id"), nullable=False)
    course_id = Column(UUID(as_uuid=True), ForeignKey("courses.id"), nullable=False)
    trainer_name = Column(String(150))
    start_date = Column(Date)
    end_date = Column(Date)
    score = Column(String(20))
    remarks = Column(String(255))
    status = Column(String(30), default="in_progress")
    created_at = Column(DateTime, default=datetime.utcnow)

    member = relationship("Member")
    course = relationship("Course")


class Assessment(Base):
    __tablename__ = "assessments"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    training_record_id = Column(UUID(as_uuid=True), ForeignKey("training_records.id"), nullable=False)
    name = Column(String(150), nullable=False)
    score = Column(String(20))
    max_score = Column(String(20))
    date = Column(Date)
    created_at = Column(DateTime, default=datetime.utcnow)

    training_record = relationship("TrainingRecord")


class Badge(Base):
    __tablename__ = "badges"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(100), unique=True, nullable=False)
    description = Column(String(500))
    requirements = Column(String(500))
    created_at = Column(DateTime, default=datetime.utcnow)


class MemberBadge(Base):
    __tablename__ = "member_badges"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    member_id = Column(UUID(as_uuid=True), ForeignKey("members.id"), nullable=False)
    badge_id = Column(UUID(as_uuid=True), ForeignKey("badges.id"), nullable=False)
    awarded_date = Column(Date)
    awarded_by = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    member = relationship("Member")
    badge = relationship("Badge")


class Certificate(Base):
    __tablename__ = "certificates"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    member_id = Column(UUID(as_uuid=True), ForeignKey("members.id"), nullable=False)
    course_id = Column(UUID(as_uuid=True), ForeignKey("courses.id"), nullable=True)
    certificate_number = Column(String(50), unique=True, nullable=False)
    issue_date = Column(Date)
    issued_by = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=True)
    verification_code = Column(String(50), unique=True)
    file_key = Column(String(255))
    created_at = Column(DateTime, default=datetime.utcnow)

    member = relationship("Member")
    course = relationship("Course")


class Budget(Base):
    __tablename__ = "budgets"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(150), nullable=False)
    category = Column(String(100))
    amount = Column(Numeric(12, 2), nullable=False)
    period_start = Column(Date)
    period_end = Column(Date)
    created_by = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)


class IncomeRecord(Base):
    __tablename__ = "income_records"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    source = Column(String(50), nullable=False)
    member_id = Column(UUID(as_uuid=True), ForeignKey("members.id"), nullable=True)
    amount = Column(Numeric(12, 2), nullable=False)
    date = Column(Date, nullable=False)
    description = Column(String(255))
    recorded_by = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    member = relationship("Member")


class ExpenseRecord(Base):
    __tablename__ = "expense_records"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    category = Column(String(100), nullable=False)
    description = Column(String(255))
    amount = Column(Numeric(12, 2), nullable=False)
    date = Column(Date, nullable=False)
    payment_method = Column(String(50))
    receipt_file_key = Column(String(255))
    status = Column(String(30), default="pending")
    submitted_by = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=True)
    approved_by = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=True)
    approved_at = Column(DateTime)
    created_at = Column(DateTime, default=datetime.utcnow)


class Event(Base):
    __tablename__ = "events"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(200), nullable=False)
    event_type = Column(String(50), nullable=False)  # event, camp, trip, program
    description = Column(Text)
    location = Column(String(255))
    start_date = Column(Date, nullable=False)
    end_date = Column(Date)
    status = Column(String(30), default="planned")
    responsible_officer_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=True)
    created_by = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)


class EventParticipant(Base):
    __tablename__ = "event_participants"
    __table_args__ = (UniqueConstraint("event_id", "member_id", name="uq_event_member"),)

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    event_id = Column(UUID(as_uuid=True), ForeignKey("events.id"), nullable=False)
    member_id = Column(UUID(as_uuid=True), ForeignKey("members.id"), nullable=False)
    participant_role = Column(String(50), default="participant")
    created_at = Column(DateTime, default=datetime.utcnow)

    event = relationship("Event")
    member = relationship("Member")


class EventRequirement(Base):
    __tablename__ = "event_requirements"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    event_id = Column(UUID(as_uuid=True), ForeignKey("events.id"), nullable=False)
    requirement_type = Column(String(50), nullable=False)  # transport, meals, materials, other
    description = Column(String(255))
    estimated_cost = Column(Numeric(12, 2))
    actual_cost = Column(Numeric(12, 2))
    created_at = Column(DateTime, default=datetime.utcnow)

    event = relationship("Event")


class Requisition(Base):
    __tablename__ = "requisitions"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    request_number = Column(String(30), unique=True, nullable=False)
    department = Column(String(50), nullable=False)
    requester_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    date = Column(Date, nullable=False)
    purpose = Column(Text)
    related_event_id = Column(UUID(as_uuid=True), ForeignKey("events.id"), nullable=True)
    items_description = Column(Text)
    estimated_cost = Column(Numeric(12, 2))
    required_by_date = Column(Date)
    priority = Column(String(20), default="normal")
    status = Column(String(30), default="pending")
    reviewed_by = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=True)
    decision_notes = Column(String(255))
    amount_approved = Column(Numeric(12, 2))
    amount_spent = Column(Numeric(12, 2))
    payment_reference = Column(String(100))
    created_at = Column(DateTime, default=datetime.utcnow)

    requester = relationship("User", foreign_keys=[requester_id])
    reviewer = relationship("User", foreign_keys=[reviewed_by])
    event = relationship("Event")


class InventoryItem(Base):
    __tablename__ = "inventory_items"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    category = Column(String(50), nullable=False)
    name = Column(String(150), nullable=False)
    description = Column(String(255))
    quantity = Column(Integer, default=0)
    condition = Column(String(30), default="good")
    location = Column(String(150))
    created_at = Column(DateTime, default=datetime.utcnow)


class ItemIssuance(Base):
    __tablename__ = "item_issuance"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    item_id = Column(UUID(as_uuid=True), ForeignKey("inventory_items.id"), nullable=False)
    member_id = Column(UUID(as_uuid=True), ForeignKey("members.id"), nullable=False)
    quantity_issued = Column(Integer, default=1)
    issue_date = Column(Date, nullable=False)
    return_date = Column(Date)
    condition_on_issue = Column(String(30))
    condition_on_return = Column(String(30))
    status = Column(String(30), default="issued")
    created_at = Column(DateTime, default=datetime.utcnow)

    item = relationship("InventoryItem")
    member = relationship("Member")


class LostFound(Base):
    __tablename__ = "lost_found"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    item_description = Column(String(255), nullable=False)
    status = Column(String(20), nullable=False)
    date = Column(Date, nullable=False)
    location = Column(String(150))
    member_id = Column(UUID(as_uuid=True), ForeignKey("members.id"), nullable=True)
    resolution_notes = Column(String(255))
    created_at = Column(DateTime, default=datetime.utcnow)

    member = relationship("Member")


class WelfareCase(Base):
    __tablename__ = "welfare_cases"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    member_id = Column(UUID(as_uuid=True), ForeignKey("members.id"), nullable=False)
    case_type = Column(String(100), nullable=False)
    description = Column(Text)
    status = Column(String(30), default="open")
    responsible_officer_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    member = relationship("Member")


class WelfareAssistance(Base):
    __tablename__ = "welfare_assistance"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    welfare_case_id = Column(UUID(as_uuid=True), ForeignKey("welfare_cases.id"), nullable=False)
    assistance_type = Column(String(100), nullable=False)
    description = Column(String(255))
    amount = Column(Numeric(12, 2))
    status = Column(String(30), default="pending")
    provided_by = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=True)
    provided_date = Column(Date)
    created_at = Column(DateTime, default=datetime.utcnow)

    welfare_case = relationship("WelfareCase")


class Meeting(Base):
    __tablename__ = "meetings"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    meeting_type = Column(String(30), nullable=False)  # officer, general
    date = Column(DateTime, nullable=False)
    agenda = Column(Text)
    minutes = Column(Text)
    status = Column(String(30), default="scheduled")
    created_by = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)


class MeetingParticipant(Base):
    __tablename__ = "meeting_participants"
    __table_args__ = (UniqueConstraint("meeting_id", "user_id", name="uq_meeting_user"),)

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    meeting_id = Column(UUID(as_uuid=True), ForeignKey("meetings.id"), nullable=False)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    attended = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    meeting = relationship("Meeting")
    user = relationship("User")


class MeetingActionItem(Base):
    __tablename__ = "meeting_action_items"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    meeting_id = Column(UUID(as_uuid=True), ForeignKey("meetings.id"), nullable=False)
    description = Column(String(255), nullable=False)
    responsible_user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=True)
    deadline = Column(Date)
    status = Column(String(30), default="open")
    created_at = Column(DateTime, default=datetime.utcnow)

    meeting = relationship("Meeting")


class Announcement(Base):
    __tablename__ = "announcements"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    title = Column(String(200), nullable=False)
    content = Column(Text, nullable=False)
    target_audience = Column(String(50), default="all")
    scheduled_at = Column(DateTime)
    created_by = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)


class Notification(Base):
    __tablename__ = "notifications"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    title = Column(String(200), nullable=False)
    message = Column(String(500))
    is_read = Column(Boolean, default=False)
    related_entity_type = Column(String(50))
    related_entity_id = Column(UUID(as_uuid=True))
    created_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User")


class Message(Base):
    __tablename__ = "messages"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    sender_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    recipient_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    content = Column(Text, nullable=False)
    is_read = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    sender = relationship("User", foreign_keys=[sender_id])
    recipient = relationship("User", foreign_keys=[recipient_id])


class Document(Base):
    __tablename__ = "documents"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    title = Column(String(200), nullable=False)
    category = Column(String(100))
    file_key = Column(String(255), nullable=False)
    linked_entity_type = Column(String(50))
    linked_entity_id = Column(UUID(as_uuid=True))
    current_version = Column(Integer, default=1)
    uploaded_by = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)


class DocumentVersion(Base):
    __tablename__ = "document_versions"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    document_id = Column(UUID(as_uuid=True), ForeignKey("documents.id"), nullable=False)
    version_number = Column(Integer, nullable=False)
    file_key = Column(String(255), nullable=False)
    changed_by = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=True)
    change_note = Column(String(255))
    created_at = Column(DateTime, default=datetime.utcnow)

    document = relationship("Document")


class VisitorLog(Base):
    __tablename__ = "visitor_log"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    visitor_name = Column(String(150), nullable=False)
    purpose = Column(String(255))
    host_member_id = Column(UUID(as_uuid=True), ForeignKey("members.id"), nullable=True)
    check_in_time = Column(DateTime, default=datetime.utcnow)
    check_out_time = Column(DateTime)
    created_at = Column(DateTime, default=datetime.utcnow)


class GalleryAlbum(Base):
    __tablename__ = "gallery_albums"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    title = Column(String(200), nullable=False)
    description = Column(String(255))
    created_by = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)


class GalleryPhoto(Base):
    __tablename__ = "gallery_photos"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    album_id = Column(UUID(as_uuid=True), ForeignKey("gallery_albums.id"), nullable=False)
    file_key = Column(String(255), nullable=False)
    caption = Column(String(255))
    uploaded_by = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    album = relationship("GalleryAlbum")


class SystemSetting(Base):
    __tablename__ = "system_settings"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    key = Column(String(100), unique=True, nullable=False)
    value = Column(String(500))
    updated_by = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=True)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)