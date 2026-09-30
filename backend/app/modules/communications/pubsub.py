import asyncio
import json
from uuid import UUID
from .realtime import manager

class RealtimeBus:
 def __init__(self):
  self.redis=None
  self.task=None
  self.url=None
  self.stopping=False

 async def start(self,url:str|None):
  if not url:return
  self.url=url
  self.stopping=False
  try:
   from redis.asyncio import Redis
   self.redis=Redis.from_url(url,decode_responses=True)
   await self.redis.ping()
   self.task=asyncio.create_task(self._listen())
  except Exception:
   if self.redis:
    await self.redis.aclose()
   self.redis=None

 async def _listen(self):
  from redis.asyncio import Redis
  while not self.stopping and self.url:
   pubsub=None
   try:
    if self.redis is None:
     self.redis=Redis.from_url(self.url,decode_responses=True)
     await self.redis.ping()
    pubsub=self.redis.pubsub()
    await pubsub.subscribe("sketchitup:communications")
    async for item in pubsub.listen():
     if self.stopping: return
     if item.get("type")!="message":continue
     payload=json.loads(item["data"])
     event=payload.get("event")
     if not isinstance(event,dict):continue
     user_ids=payload.get("user_ids",[])
     valid_ids=[]
     for value in user_ids:
      try: valid_ids.append(UUID(str(value)))
      except (ValueError,TypeError): continue
     if valid_ids:
      await manager.broadcast(valid_ids,event)
   except asyncio.CancelledError:
    raise
   except Exception:
    if self.redis:
     try: await self.redis.aclose()
     except Exception: pass
    self.redis=None
    if not self.stopping:
     await asyncio.sleep(2)
   finally:
    if pubsub:
     try: await pubsub.close()
     except Exception: pass

 async def publish(self,user_ids:list[UUID],event:dict):
  if not self.redis:return False
  try:
   payload={"user_ids":[str(user_id) for user_id in set(user_ids)],"event":event}
   await self.redis.publish("sketchitup:communications",json.dumps(payload))
   return True
  except Exception:
   try: await self.redis.aclose()
   except Exception: pass
   self.redis=None
   return False

 async def stop(self):
  self.stopping=True
  if self.task:
   self.task.cancel()
   try: await self.task
   except asyncio.CancelledError: pass
   self.task=None
  if self.redis:
   try: await self.redis.aclose()
   except Exception: pass
  self.redis=None

bus=RealtimeBus()
