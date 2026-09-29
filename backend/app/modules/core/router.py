from fastapi import APIRouter,Depends,HTTPException
from secrets import compare_digest
from sqlalchemy import select
from sqlalchemy.orm import Session
from ...db import get_db
from .models import User,Role,UserRole
from .schemas import LoginRequest,TokenResponse,UserCreate,UserRead,RoleRead
from ...config import settings
from .security import verify_password,hash_password,create_access_token
from .dependencies import current_user,require_roles
from .audit import record
router=APIRouter()
@router.post("/auth/bootstrap",response_model=UserRead,status_code=201)
def bootstrap(payload:UserCreate,bootstrap_secret:str,db:Session=Depends(get_db)):
 if not compare_digest(bootstrap_secret,settings.bootstrap_secret): raise HTTPException(403,"Invalid bootstrap secret")
 if db.scalar(select(User.id).limit(1)): raise HTTPException(409,"Bootstrap is already complete")
 from .models import Organization
 org=Organization(name="Sketchitup Solutions");db.add(org);db.flush()
 role=db.scalar(select(Role).where(Role.name=="founder_owner"))
 if not role: role=Role(name="founder_owner",description="Founder / Owner");db.add(role);db.flush()
 target=User(organization_id=org.id,email=payload.email.lower(),display_name=payload.display_name,password_hash=hash_password(payload.password),status="active");db.add(target);db.flush();db.add(UserRole(user_id=target.id,role_id=role.id));record(db,org.id,target.id,"bootstrap","user",target.id);db.commit();db.refresh(target);return target
@router.post("/auth/login",response_model=TokenResponse)
def login(payload:LoginRequest,db:Session=Depends(get_db)):
 user=db.scalar(select(User).where(User.email==payload.email.lower(),User.deleted_at.is_(None)))
 if not user or not user.password_hash or not verify_password(payload.password,user.password_hash): raise HTTPException(401,"Invalid credentials")
 if user.status!="active": raise HTTPException(403,"User is not active")
 roles=db.scalars(select(Role.name).join(UserRole,UserRole.role_id==Role.id).where(UserRole.user_id==user.id)).all();record(db,user.organization_id,user.id,"login","user",user.id);db.commit();return TokenResponse(access_token=create_access_token(user.id,user.organization_id,list(roles)))
@router.get("/auth/me",response_model=UserRead)
def me(user=Depends(current_user)): return user
@router.get("/users",response_model=list[UserRead])
def list_users(user=Depends(require_roles("founder_owner","admin_operations")),db:Session=Depends(get_db)):
 return db.scalars(select(User).where(User.organization_id==user.organization_id,User.deleted_at.is_(None)).order_by(User.display_name)).all()
@router.post("/users",response_model=UserRead,status_code=201)
def create_user(payload:UserCreate,user=Depends(require_roles("founder_owner","admin_operations")),db:Session=Depends(get_db)):
 if payload.organization_id!=user.organization_id and payload.organization_id is not None: raise HTTPException(403,"Cannot create outside your organization")
 email=payload.email.lower()
 if db.scalar(select(User).where(User.email==email,User.deleted_at.is_(None))): raise HTTPException(409,"Email already exists")
 target=User(organization_id=user.organization_id,email=email,display_name=payload.display_name,password_hash=hash_password(payload.password),status="active");db.add(target);db.flush()
 for role_id in payload.role_ids: db.add(UserRole(user_id=target.id,role_id=role_id))
 record(db,user.organization_id,user.id,"create","user",target.id,{"email":email});db.commit();db.refresh(target);return target
@router.get("/roles",response_model=list[RoleRead])
def list_roles(user=Depends(current_user),db:Session=Depends(get_db)): return db.scalars(select(Role).order_by(Role.name)).all()
