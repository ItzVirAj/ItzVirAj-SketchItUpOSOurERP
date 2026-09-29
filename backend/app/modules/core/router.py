from datetime import datetime,timedelta,timezone
from secrets import compare_digest
from fastapi import APIRouter,Depends,HTTPException
from sqlalchemy import select,delete
from sqlalchemy.orm import Session
from ...db import get_db
from .models import User,Role,UserRole,Organization,AuthSession,LoginAttempt,Permission
from .schemas import LoginRequest,TokenResponse,RefreshRequest,UserCreate,UserRead,RoleRead,PermissionRead,AuditLogRead
from ...config import settings
from .security import verify_password,hash_password,create_access_token,create_refresh_token,hash_refresh_token
from .dependencies import current_user,require_roles,require_permission
from .audit import record
router=APIRouter()
def issue_session(db:Session,user:User,roles:list[str])->TokenResponse:
 refresh_token=create_refresh_token()
 db.add(AuthSession(user_id=user.id,token_hash=hash_refresh_token(refresh_token),expires_at=datetime.now(timezone.utc)+timedelta(days=settings.refresh_token_expire_days)))
 return TokenResponse(access_token=create_access_token(user.id,user.organization_id,roles),refresh_token=refresh_token)
@router.post("/auth/bootstrap",response_model=UserRead,status_code=201)
def bootstrap(payload:UserCreate,bootstrap_secret:str,db:Session=Depends(get_db)):
 if not compare_digest(bootstrap_secret,settings.bootstrap_secret): raise HTTPException(403,"Invalid bootstrap secret")
 if db.scalar(select(User.id).limit(1)): raise HTTPException(409,"Bootstrap is already complete")
 org=Organization(name="Sketchitup Solutions");db.add(org);db.flush()
 role=db.scalar(select(Role).where(Role.name=="founder_owner"))
 if not role: role=Role(name="founder_owner",description="Founder / Owner");db.add(role);db.flush()
 target=User(organization_id=org.id,email=payload.email.lower(),display_name=payload.display_name,password_hash=hash_password(payload.password),status="active");db.add(target);db.flush();db.add(UserRole(user_id=target.id,role_id=role.id));record(db,org.id,target.id,"bootstrap","user",target.id);db.commit();db.refresh(target);return target
@router.post("/auth/login",response_model=TokenResponse)
def login(payload:LoginRequest,db:Session=Depends(get_db)):
 email=payload.email.lower(); now=datetime.now(timezone.utc); window=now-timedelta(minutes=15)
 attempts=db.scalar(select(LoginAttempt).where(LoginAttempt.identifier==email,LoginAttempt.success.is_(False),LoginAttempt.attempted_at>=window).order_by(LoginAttempt.attempted_at.desc()).limit(1))
 failed_count=len(db.scalars(select(LoginAttempt.id).where(LoginAttempt.identifier==email,LoginAttempt.success.is_(False),LoginAttempt.attempted_at>=window)).all())
 if failed_count>=5: raise HTTPException(429,"Too many failed login attempts. Try again later.")
 user=db.scalar(select(User).where(User.email==email,User.deleted_at.is_(None)))
 if not user or not user.password_hash or not verify_password(payload.password,user.password_hash):
  db.add(LoginAttempt(identifier=email,attempted_at=now,success=False));db.commit();raise HTTPException(401,"Invalid credentials")
 if user.status!="active": raise HTTPException(403,"User is not active")
 db.add(LoginAttempt(identifier=email,attempted_at=now,success=True))
 db.execute(delete(LoginAttempt).where(LoginAttempt.identifier==email,LoginAttempt.attempted_at<window))
 roles=db.scalars(select(Role.name).join(UserRole,UserRole.role_id==Role.id).where(UserRole.user_id==user.id)).all()
 result=issue_session(db,user,list(roles));record(db,user.organization_id,user.id,"login","user",user.id);db.commit();return result
@router.post("/auth/refresh",response_model=TokenResponse)
def refresh(payload:RefreshRequest,db:Session=Depends(get_db)):
 session=db.scalar(select(AuthSession).where(AuthSession.token_hash==hash_refresh_token(payload.refresh_token)))
 now=datetime.now(timezone.utc)
 if not session or session.revoked_at or session.expires_at<=now: raise HTTPException(401,"Invalid or expired refresh token")
 user=db.get(User,session.user_id)
 if not user or user.status!="active" or user.deleted_at: raise HTTPException(401,"User is not active")
 session.revoked_at=now
 roles=db.scalars(select(Role.name).join(UserRole,UserRole.role_id==Role.id).where(UserRole.user_id==user.id)).all()
 result=issue_session(db,user,list(roles));record(db,user.organization_id,user.id,"refresh","session",session.id);db.commit();return result
@router.post("/auth/logout",status_code=204)
def logout(payload:RefreshRequest,db:Session=Depends(get_db)):
 session=db.scalar(select(AuthSession).where(AuthSession.token_hash==hash_refresh_token(payload.refresh_token)))
 if session and not session.revoked_at: session.revoked_at=datetime.now(timezone.utc);db.commit()
@router.get("/auth/me",response_model=UserRead)
def me(user=Depends(current_user)): return user
@router.get("/users",response_model=list[UserRead])
def list_users(user=Depends(require_permission("users.read")),db:Session=Depends(get_db)):
 return db.scalars(select(User).where(User.organization_id==user.organization_id,User.deleted_at.is_(None)).order_by(User.display_name)).all()
@router.post("/users",response_model=UserRead,status_code=201)
def create_user(payload:UserCreate,user=Depends(require_permission("users.create")),db:Session=Depends(get_db)):
 if payload.organization_id!=user.organization_id and payload.organization_id is not None: raise HTTPException(403,"Cannot create outside your organization")
 email=payload.email.lower()
 if db.scalar(select(User).where(User.email==email,User.deleted_at.is_(None))): raise HTTPException(409,"Email already exists")
 target=User(organization_id=user.organization_id,email=email,display_name=payload.display_name,password_hash=hash_password(payload.password),status="active");db.add(target);db.flush()
 for role_id in payload.role_ids: db.add(UserRole(user_id=target.id,role_id=role_id))
 record(db,user.organization_id,user.id,"create","user",target.id,{"email":email});db.commit();db.refresh(target);return target
@router.get("/roles",response_model=list[RoleRead])
def list_roles(user=Depends(current_user),db:Session=Depends(get_db)): return db.scalars(select(Role).order_by(Role.name)).all()
@router.get("/permissions",response_model=list[PermissionRead])
def list_permissions(user=Depends(require_permission("roles.read")),db:Session=Depends(get_db)):
 return db.scalars(select(Permission).order_by(Permission.key)).all()
@router.get("/audit",response_model=list[AuditLogRead])
def list_audit(user=Depends(require_permission("audit.read")),db:Session=Depends(get_db)):
 from .models import AuditLog
 return db.scalars(select(AuditLog).where(AuditLog.organization_id==user.organization_id).order_by(AuditLog.created_at.desc()).limit(200)).all()
