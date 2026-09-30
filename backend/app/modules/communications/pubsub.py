import asyncio
import json
from uuid import UUID
from .realtime import manager

class RealtimeBus:
 def __init__(self):
  self.redis=None
  self.task=None

 async def start(self,url:str|None):
  if not url:return
  try:
   from redis.asyncio import Redis
   self.redis=Redis.from_url(url,decode_responses=True)
   await self.redis.ping()
   self.task=asyncio.create_task(self._listen())
  except Exception:
   if self.redis: await self.redis.aclose()
   self.redis=None

 async def _listen(self):
  pubsub=self.redis.pubsub()
  await pubsub.subscribe("sketchitup:communications")
  try:
   async for item in pubsub.listen():
    if item.get("type")!="message":continue
    payload=json.loads(item["data"])
    await manager.send_to_user(UUID(payload["user_id"]),payload["event"])
  except asyncio.CancelledError:
   raise
  except Exception:
   pass
  finally:
   await pubsub.close()

 async def publish(self,user_ids:list[UUID],event:dict):
  if not self.redis:return False
  try:
   for user_id in set(user_ids):
    await self.redis.publish("sketchitup:communications",json.dumps({"user_id":str(user_id),"event":event}))
   return True
  except Exception:
   return False

 async def stop(self):
  if self.task:
   self.task.cancel()
   try: await self.task
   except asyncio.CancelledError: pass
  if self.redis: await self.redis.aclose()

bus=RealtimeBus()
