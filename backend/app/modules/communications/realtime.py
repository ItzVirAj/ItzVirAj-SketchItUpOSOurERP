from collections import defaultdict
from uuid import UUID
from fastapi import WebSocket

class ConnectionManager:
 def __init__(self):
  self.connections:dict[UUID,set[WebSocket]]=defaultdict(set)

 async def connect(self,user_id:UUID,websocket:WebSocket):
  await websocket.accept()
  self.connections[user_id].add(websocket)

 def disconnect(self,user_id:UUID,websocket:WebSocket):
  sockets=self.connections.get(user_id)
  if not sockets:return
  sockets.discard(websocket)
  if not sockets:self.connections.pop(user_id,None)

 async def send_to_user(self,user_id:UUID,payload:dict):
  stale=[]
  for websocket in list(self.connections.get(user_id,set())):
   try: await websocket.send_json(payload)
   except Exception: stale.append(websocket)
  for websocket in stale:self.disconnect(user_id,websocket)

 async def broadcast(self,user_ids:list[UUID],payload:dict):
  for user_id in set(user_ids):
   await self.send_to_user(user_id,payload)

manager=ConnectionManager()
