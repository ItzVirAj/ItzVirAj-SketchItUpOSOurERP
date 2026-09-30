from datetime import datetime, timezone
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select, func
from sqlalchemy.orm import Session
from ...db import get_db
from ..core.models import User, UserRole, Role
from ..core.dependencies import require_permission
from ..core.audit import record
from .models import Channel, ChannelMember, ChannelReadState, Message
from .schemas import ChannelCreate, ChannelRead, ChannelUnreadRead, MessageCreate, MessageRead, MemberAdd
from ..notifications.service import create_notification
from .realtime import manager
from .pubsub import bus

router=APIRouter()

def get_channel(db:Session,user:User,channel_id:UUID):
 return db.scalar(select(Channel).where(Channel.id==channel_id,Channel.organization_id==user.organization_id))

def can_access(db:Session,user:User,channel:Channel):
 if channel.archived_at is not None: return False
 if channel.channel_type=="public": return True
 return db.scalar(select(ChannelMember).where(ChannelMember.channel_id==channel.id,ChannelMember.user_id==user.id)) is not None

@router.get("/channels",response_model=list[ChannelRead])
def list_channels(user:User=Depends(require_permission("communications.read")),db:Session=Depends(get_db)):
 channels=db.scalars(select(Channel).where(Channel.organization_id==user.organization_id,Channel.archived_at.is_(None)).order_by(Channel.name.asc())).all()
 return [c for c in channels if c.channel_type=="public" or can_access(db,user,c)]

@router.post("/channels",response_model=ChannelRead,status_code=201)
def create_channel(payload:ChannelCreate,user:User=Depends(require_permission("communications.create")),db:Session=Depends(get_db)):
 if payload.channel_type not in {"public","private"}:
  raise HTTPException(400,"channel_type must be public or private")
 existing=db.scalar(select(Channel).where(Channel.organization_id==user.organization_id,Channel.name==payload.name))
 if existing: raise HTTPException(409,"A channel with this name already exists")
 channel=Channel(organization_id=user.organization_id,created_by_user_id=user.id,**payload.model_dump())
 db.add(channel);db.flush()
 db.add(ChannelMember(channel_id=channel.id,user_id=user.id))
 record(db,user.organization_id,user.id,"create","communication_channel",channel.id,{"name":channel.name})
 db.commit();db.refresh(channel);return channel

@router.post("/channels/{channel_id}/archive")
def archive_channel(channel_id:UUID,user:User=Depends(require_permission("communications.create")),db:Session=Depends(get_db)):
 channel=get_channel(db,user,channel_id)
 if not channel: raise HTTPException(404,"Channel not found")
 roles=db.scalars(select(Role.name).join(UserRole,UserRole.role_id==Role.id).where(UserRole.user_id==user.id)).all()
 is_admin=bool(set(roles).intersection({"founder_owner","admin_operations"}))
 if channel.created_by_user_id!=user.id and not is_admin:
  raise HTTPException(403,"Only the channel creator or an administrator can archive this channel")
 if channel.archived_at is not None:
  raise HTTPException(409,"Channel is already archived")
 channel.archived_at=datetime.now(timezone.utc)
 channel.updated_at=datetime.now(timezone.utc)
 record(db,user.organization_id,user.id,"archive","communication_channel",channel.id)
 db.commit()
 return {"channel_id":channel.id,"archived_at":channel.archived_at}

@router.post("/channels/{channel_id}/unarchive")
def unarchive_channel(channel_id:UUID,user:User=Depends(require_permission("communications.create")),db:Session=Depends(get_db)):
 channel=db.scalar(select(Channel).where(Channel.id==channel_id,Channel.organization_id==user.organization_id))
 if not channel: raise HTTPException(404,"Channel not found")
 roles=db.scalars(select(Role.name).join(UserRole,UserRole.role_id==Role.id).where(UserRole.user_id==user.id)).all()
 is_admin=bool(set(roles).intersection({"founder_owner","admin_operations"}))
 if channel.created_by_user_id!=user.id and not is_admin:
  raise HTTPException(403,"Only the channel creator or an administrator can restore this channel")
 if channel.archived_at is None:
  raise HTTPException(409,"Channel is not archived")
 channel.archived_at=None
 channel.updated_at=datetime.now(timezone.utc)
 record(db,user.organization_id,user.id,"unarchive","communication_channel",channel.id)
 db.commit()
 return {"channel_id":channel.id,"archived_at":None}

@router.post("/channels/{channel_id}/members",status_code=201)
def add_member(channel_id:UUID,payload:MemberAdd,user:User=Depends(require_permission("communications.create")),db:Session=Depends(get_db)):
 channel=get_channel(db,user,channel_id)
 if not channel or channel.archived_at is not None: raise HTTPException(404,"Channel not found")
 member_user=db.scalar(select(User).where(User.id==payload.user_id,User.organization_id==user.organization_id,User.status=="active"))
 if not member_user: raise HTTPException(400,"User must belong to your organization and be active")
 if db.scalar(select(ChannelMember).where(ChannelMember.channel_id==channel.id,ChannelMember.user_id==payload.user_id)):
  raise HTTPException(409,"User is already a channel member")
 db.add(ChannelMember(channel_id=channel.id,user_id=payload.user_id))
 record(db,user.organization_id,user.id,"add_member","communication_channel",channel.id,{"user_id":str(payload.user_id)})
 if channel.channel_type=="private":
  create_notification(db,user.organization_id,payload.user_id,"communications.channel_member_added","Added to private channel",f"You were added to #{channel.name}.","communication_channel",channel.id,f"/communications/channels/{channel.id}")
 db.commit();return {"channel_id":channel.id,"user_id":payload.user_id}



@router.delete("/channels/{channel_id}/members/{member_user_id}")
def remove_member(channel_id:UUID,member_user_id:UUID,user:User=Depends(require_permission("communications.create")),db:Session=Depends(get_db)):
 channel=get_channel(db,user,channel_id)
 if not channel or channel.archived_at is not None: raise HTTPException(404,"Channel not found")
 target=db.scalar(select(ChannelMember).where(ChannelMember.channel_id==channel.id,ChannelMember.user_id==member_user_id))
 if not target: raise HTTPException(404,"Channel member not found")
 roles=db.scalars(
  select(Role.name)
  .join(UserRole,UserRole.role_id==Role.id)
  .where(UserRole.user_id==user.id)
 ).all()
 is_admin=bool(set(roles).intersection({"founder_owner","admin_operations"}))
 if member_user_id!=user.id and channel.created_by_user_id!=user.id and not is_admin:
  raise HTTPException(403,"Only the channel creator or an administrator can remove another member")
 db.delete(target)
 record(db,user.organization_id,user.id,"remove_member","communication_channel",channel.id,{"user_id":str(member_user_id)})
 db.commit()
 return {"channel_id":channel.id,"user_id":member_user_id}

@router.get("/channels/unread",response_model=list[ChannelUnreadRead])
def channel_unread_counts(user:User=Depends(require_permission("communications.read")),db:Session=Depends(get_db)):
 channels=db.scalars(select(Channel).where(Channel.organization_id==user.organization_id,Channel.archived_at.is_(None)).order_by(Channel.name.asc())).all()
 visible=[]
 private_ids=[]
 for channel in channels:
  if channel.channel_type=="public":
   visible.append(channel)
  elif can_access(db,user,channel):
   visible.append(channel);private_ids.append(channel.id)
 if not visible:return []
 state_expr=select(ChannelReadState.channel_id,ChannelReadState.last_read_at).where(ChannelReadState.user_id==user.id).subquery()
 unread_q=select(Message.channel_id,func.count(Message.id)).outerjoin(
  state_expr,state_expr.c.channel_id==Message.channel_id
 ).where(
  Message.organization_id==user.organization_id,
  Message.sender_user_id!=user.id,
  (state_expr.c.last_read_at.is_(None)) | (Message.created_at>state_expr.c.last_read_at)
 ).group_by(Message.channel_id)
 counts={channel_id:int(count) for channel_id,count in db.execute(unread_q).all()}
 return [ChannelUnreadRead(channel_id=channel.id,unread_count=counts.get(channel.id,0)) for channel in visible]


@router.post("/channels/{channel_id}/read")
def mark_channel_read(channel_id:UUID,user:User=Depends(require_permission("communications.read")),db:Session=Depends(get_db)):
 channel=get_channel(db,user,channel_id)
 if not channel or not can_access(db,user,channel): raise HTTPException(404,"Channel not found")
 now=datetime.now(timezone.utc)
 state=db.scalar(select(ChannelReadState).where(ChannelReadState.channel_id==channel.id,ChannelReadState.user_id==user.id))
 if state: state.last_read_at=now
 else: db.add(ChannelReadState(channel_id=channel.id,user_id=user.id,last_read_at=now))
 db.commit()
 return {"channel_id":channel.id,"last_read_at":now}

@router.get("/channels/{channel_id}/messages",response_model=list[MessageRead])
def list_messages(channel_id:UUID,user:User=Depends(require_permission("communications.read")),db:Session=Depends(get_db),limit:int=50,before:datetime|None=None):
 channel=get_channel(db,user,channel_id)
 if not channel or not can_access(db,user,channel): raise HTTPException(404,"Channel not found")
 limit=max(1,min(limit,100))
 q=select(Message).where(Message.organization_id==user.organization_id,Message.channel_id==channel.id)
 if before:q=q.where(Message.created_at<before)
 return db.scalars(q.order_by(Message.created_at.desc()).limit(limit)).all()

@router.post("/channels/{channel_id}/messages",response_model=MessageRead,status_code=201)
async def send_message(channel_id:UUID,payload:MessageCreate,user:User=Depends(require_permission("communications.create")),db:Session=Depends(get_db)):
 channel=get_channel(db,user,channel_id)
 if not channel or not can_access(db,user,channel): raise HTTPException(404,"Channel not found")
 message=Message(organization_id=user.organization_id,channel_id=channel.id,sender_user_id=user.id,body=payload.body.strip())
 if not message.body: raise HTTPException(400,"Message body cannot be empty")
 db.add(message);db.flush()
 record(db,user.organization_id,user.id,"create","communication_message",message.id,{"channel_id":str(channel.id)})
 member_ids=db.scalars(select(ChannelMember.user_id).where(ChannelMember.channel_id==channel.id,ChannelMember.user_id!=user.id)).all()
 if channel.channel_type=="private":
  recipients=member_ids
 else:
  recipients=db.scalars(select(User.id).where(User.organization_id==user.organization_id,User.status=="active",User.id!=user.id)).all()
 preview=message.body if len(message.body)<=120 else message.body[:117]+"..."
 for recipient_id in recipients:
  create_notification(db,user.organization_id,recipient_id,"communications.message",f"New message in #{channel.name}",f"{user.display_name}: {preview}","communication_message",message.id,f"/communications/channels/{channel.id}")
 db.commit();db.refresh(message)
 event={"type":"message.created","channel_id":str(channel.id),"message":{"id":str(message.id),"sender_user_id":str(user.id),"body":message.body,"created_at":message.created_at.isoformat()}}
 if not await bus.publish(recipients,event):
  await manager.broadcast(recipients,event)
 return message

@router.patch("/messages/{message_id}",response_model=MessageRead)
async def edit_message(message_id:UUID,payload:MessageCreate,user:User=Depends(require_permission("communications.create")),db:Session=Depends(get_db)):
 message=db.scalar(select(Message).where(Message.id==message_id,Message.organization_id==user.organization_id))
 if not message: raise HTTPException(404,"Message not found")
 if message.sender_user_id!=user.id: raise HTTPException(403,"You can only edit your own messages")
 body=payload.body.strip()
 if not body: raise HTTPException(400,"Message body cannot be empty")
 message.body=body;message.is_edited=True;message.updated_at=datetime.now(timezone.utc)
 record(db,user.organization_id,user.id,"update","communication_message",message.id)
 db.commit();db.refresh(message)
 channel=db.get(Channel,message.channel_id)
 if channel and channel.channel_type=="public":
  recipients=db.scalars(select(User.id).where(User.organization_id==user.organization_id,User.status=="active",User.id!=user.id)).all()
 else:
  recipients=db.scalars(select(ChannelMember.user_id).where(ChannelMember.channel_id==message.channel_id,ChannelMember.user_id!=user.id)).all()
 if message.channel_id:
  event={"type":"message.updated","channel_id":str(message.channel_id),"message":{"id":str(message.id),"sender_user_id":str(message.sender_user_id),"body":message.body,"is_edited":message.is_edited,"updated_at":message.updated_at.isoformat()}}
  if not await bus.publish(recipients,event):
   await manager.broadcast(recipients,event)
 return message
