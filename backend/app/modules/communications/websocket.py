from uuid import UUID
from fastapi import APIRouter,WebSocket,WebSocketDisconnect
from sqlalchemy import select
from ...db import SessionLocal
from ..core.models import User,UserRole,Role,RolePermission,Permission
from ..core.security import decode_access_token
from .models import Channel,ChannelMember
from .realtime import manager

router=APIRouter()

def authenticate(token:str,db):
 try: user_id=UUID(decode_access_token(token)["sub"])
 except Exception:return None
 user=db.get(User,user_id)
 if not user or user.status!="active" or user.deleted_at:return None
 allowed=db.scalar(
  select(Permission.id)
  .join(RolePermission,RolePermission.permission_id==Permission.id)
  .join(UserRole,UserRole.role_id==RolePermission.role_id)
  .where(UserRole.user_id==user.id,Permission.key=="communications.read")
 )
 return user if allowed else None

def can_access(db,user,channel_id):
 channel=db.scalar(select(Channel).where(Channel.id==channel_id,Channel.organization_id==user.organization_id))
 if not channel:return None
 if channel.channel_type=="public":return channel
 member=db.scalar(select(ChannelMember).where(ChannelMember.channel_id==channel.id,ChannelMember.user_id==user.id))
 return channel if member else None

@router.websocket("/ws")
async def communication_websocket(websocket:WebSocket):
 token=websocket.query_params.get("token")
 if not token:
  await websocket.close(code=1008);return
 db=SessionLocal()
 user=authenticate(token,db)
 if not user:
  db.close();await websocket.close(code=1008);return
 await manager.connect(user.id,websocket)
 try:
  while True:
   data=await websocket.receive_json()
   if data.get("type")=="subscribe":
    try: channel_id=UUID(str(data.get("channel_id")))
    except Exception:
     await websocket.send_json({"type":"error","detail":"Invalid channel_id"});continue
    channel=can_access(db,user,channel_id)
    if not channel:
     await websocket.send_json({"type":"error","detail":"Channel not found"});continue
    await websocket.send_json({"type":"subscribed","channel_id":str(channel.id)})
   elif data.get("type")=="ping":
    await websocket.send_json({"type":"pong"})
 finally:
  manager.disconnect(user.id,websocket)
  db.close()
