import asyncio
from sqlalchemy import select,text
from ..core.models import Organization
from ...db import SessionLocal
from .automation import generate_overdue_notifications

_LOCK_KEY=78140321
_INTERVAL_SECONDS=3600

async def overdue_notification_loop():
 while True:
  try:
   db=SessionLocal()
   try:
    locked=bool(db.scalar(select(text("pg_try_advisory_lock(:key)")).params(key=_LOCK_KEY)))
    if locked:
     try:
      org_ids=db.scalars(select(Organization.id)).all()
      for organization_id in org_ids:
       generate_overdue_notifications(db,organization_id)
     finally:
      db.execute(text("SELECT pg_advisory_unlock(:key)")).params(key=_LOCK_KEY)
      db.commit()
   finally:
    db.close()
  except Exception:
   pass
  await asyncio.sleep(_INTERVAL_SECONDS)