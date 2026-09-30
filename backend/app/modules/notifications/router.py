from datetime import datetime,timezone
from uuid import UUID
from fastapi import APIRouter,Depends,HTTPException
from sqlalchemy import select,update
from sqlalchemy.orm import Session
from ...db import get_db
from ..core.models import User
from ..core.dependencies import require_permission
from .models import Notification
from .schemas import NotificationRead,NotificationReadUpdate
router=APIRouter()
@router.get("",response_model=list[NotificationRead])
def list_notifications(user:User=Depends(require_permission("notifications.read")),db:Session=Depends(get_db),unread_only:bool=False,limit:int=50):
 limit=max(1,min(limit,100));q=select(Notification).where(Notification.organization_id==user.organization_id,Notification.user_id==user.id)
 if unread_only:q=q.where(Notification.is_read.is_(False))
 return db.scalars(q.order_by(Notification.created_at.desc()).limit(limit)).all()
@router.post("/{notification_id}/read",response_model=NotificationRead)
def mark_read(notification_id:UUID,p:NotificationReadUpdate=NotificationReadUpdate(),user:User=Depends(require_permission("notifications.read")),db:Session=Depends(get_db)):
 n=db.scalar(select(Notification).where(Notification.id==notification_id,Notification.organization_id==user.organization_id,Notification.user_id==user.id))
 if not n: raise HTTPException(404,"Notification not found")
 n.is_read=p.is_read;n.read_at=datetime.now(timezone.utc) if p.is_read else None;db.commit();db.refresh(n);return n
@router.post("/read-all")
def mark_all_read(user:User=Depends(require_permission("notifications.read")),db:Session=Depends(get_db)):
 result=db.execute(update(Notification).where(Notification.organization_id==user.organization_id,Notification.user_id==user.id,Notification.is_read.is_(False)).values(is_read=True,read_at=datetime.now(timezone.utc)))
 db.commit();return {"updated":result.rowcount}