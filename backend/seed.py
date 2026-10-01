from app.database import SessionLocal
from app import models
from app.security import hash_password

db = SessionLocal()

ROLE_NAMES = [
    "SUPER_ADMIN", "ADMIN", "OFFICER", "TREASURER",
    "TRAINING_OFFICER", "SECRETARY", "VIEWER",
]

roles = {}
for name in ROLE_NAMES:
    existing = db.query(models.Role).filter(models.Role.name == name).first()
    roles[name] = existing if existing else models.Role(name=name)
    if not existing:
        db.add(roles[name])
        db.flush()

db.commit()

existing_admin = db.query(models.User).filter(models.User.username == "SUPERADMIN").first()
if not existing_admin:
    admin_user = models.User(
        username="SUPERADMIN",
        password_hash=hash_password("ChangeMe2026"),
        role_id=roles["SUPER_ADMIN"].id,
        must_change_password=True,
    )
    db.add(admin_user)
    db.commit()
    print("Created SUPERADMIN user with temporary password: ChangeMe2026")
else:
    print("SUPERADMIN user already exists — skipped")


def ensure_permission(module: str, action: str) -> models.Permission:
    perm = (
        db.query(models.Permission)
        .filter(models.Permission.module == module, models.Permission.action == action)
        .first()
    )
    if not perm:
        perm = models.Permission(module=module, action=action)
        db.add(perm)
        db.flush()
    return perm


def ensure_role_permission(role_name: str, module: str, action: str):
    perm = ensure_permission(module, action)
    role = roles[role_name]
    exists = (
        db.query(models.RolePermission)
        .filter(models.RolePermission.role_id == role.id, models.RolePermission.permission_id == perm.id)
        .first()
    )
    if not exists:
        db.add(models.RolePermission(role_id=role.id, permission_id=perm.id))


MEMBERS_MATRIX = {
    "ADMIN": ["view", "create", "edit", "delete"],
    "OFFICER": ["view", "edit"],
    "TREASURER": ["view"],
}
for role_name, actions in MEMBERS_MATRIX.items():
    for action in actions:
        ensure_role_permission(role_name, "members", action)

ATTENDANCE_MATRIX = {
    "ADMIN": ["view", "create", "edit", "delete"],
    "OFFICER": ["view", "create", "edit"],
    "TREASURER": ["view"],
}
for role_name, actions in ATTENDANCE_MATRIX.items():
    for action in actions:
        ensure_role_permission(role_name, "attendance", action)

TRAINING_MATRIX = {
    "ADMIN": ["view", "create", "edit", "delete"],
    "TRAINING_OFFICER": ["view", "create", "edit", "delete"],
    "OFFICER": ["view"],
}
for role_name, actions in TRAINING_MATRIX.items():
    for action in actions:
        ensure_role_permission(role_name, "training", action)

db.commit()

MEETING_TYPES = ["Saturday Training", "General Meeting", "Officer Meeting", "Crash Program"]
for name in MEETING_TYPES:
    if not db.query(models.MeetingType).filter(models.MeetingType.name == name).first():
        db.add(models.MeetingType(name=name))

db.commit()
db.close()
print("Seed complete.")