import os
from sqlalchemy import select
from app.db import SessionLocal
from app.modules.core.models import Organization,Role,User,UserRole
from app.modules.core.security import hash_password

EMAIL="test@sketchitup.in"
PASSWORD=os.environ.get("TEST_USER_PASSWORD","Pass@123")

db=SessionLocal()
try:
    org=db.scalar(select(Organization).where(Organization.name=="Sketchitup Solutions"))
    if not org:
        org=Organization(name="Sketchitup Solutions")
        db.add(org); db.flush()
    role=db.scalar(select(Role).where(Role.name=="founder_owner"))
    if not role:
        role=Role(name="founder_owner",description="Founder / Owner")
        db.add(role); db.flush()
    user=db.scalar(select(User).where(User.email==EMAIL))
    if not user:
        user=User(organization_id=org.id,email=EMAIL,display_name="SketchItUp Test User",password_hash=hash_password(PASSWORD),status="active")
        db.add(user); db.flush()
    else:
        user.organization_id=org.id
        user.password_hash=hash_password(PASSWORD)
        user.status="active"
    if not db.scalar(select(UserRole).where(UserRole.user_id==user.id,UserRole.role_id==role.id)):
        db.add(UserRole(user_id=user.id,role_id=role.id))
    db.commit()
    print(f"Test user ready: {EMAIL}")
finally:
    db.close()
