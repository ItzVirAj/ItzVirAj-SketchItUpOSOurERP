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
    event=payload.get("event")
    if not isinstance(event,dict):continue
    user_ids=payload.get("user_ids",[])
    await manager.broadcast([UUID(value) for value in user_ids],event)
  except asyncio.CancelledError:
   raise
  except Exception:
   pass
  finally:
   await pubsub.close()

 async def publish(self,user_ids:list[UUID],event:dict):
  if not self.redis:return False
  try:
   payload={"user_ids":[str(user_id) for user_id in set(user_ids)],"event":event}
   await self.redis.publish("sketchitup:communications",json.dumps(payload))
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
