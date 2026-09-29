from uuid import UUID
from fastapi import Depends,HTTPException,status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy import select
from sqlalchemy.orm import Session
from ...db import get_db
from .models import User,UserRole,Role,RolePermission,Permission
from .security import decode_access_token
oauth=OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")
def current_user(token:str=Depends(oauth),db:Session=Depends(get_db))->User:
 try: uid=UUID(decode_access_token(token)["sub"])
 except Exception: raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Invalid or expired access token")
 user=db.get(User,uid)
 if not user or user.status!="active" or user.deleted_at: raise HTTPException(status_code=401,detail="User is not active")
 return user
def require_roles(*allowed:str):
 def dependency(user:User=Depends(current_user),db:Session=Depends(get_db))->User:
  roles=db.scalars(select(Role.name).join(UserRole,UserRole.role_id==Role.id).where(UserRole.user_id==user.id)).all()
  if not set(roles).intersection(allowed): raise HTTPException(status_code=403,detail="Insufficient permissions")
  return user
 return dependency
def require_permission(permission_key:str):
 def dependency(user:User=Depends(current_user),db:Session=Depends(get_db))->User:
  allowed=db.scalar(select(Permission.id).join(RolePermission,RolePermission.permission_id==Permission.id).join(UserRole,UserRole.role_id==RolePermission.role_id).where(UserRole.user_id==user.id,Permission.key==permission_key))
  if not allowed: raise HTTPException(status_code=403,detail="Insufficient permissions")
  return user
 return dependency
