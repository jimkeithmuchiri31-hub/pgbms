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

db.close()
print("Seed complete.")