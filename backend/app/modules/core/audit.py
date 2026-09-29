from uuid import UUID
from sqlalchemy.orm import Session
from .models import AuditLog
def record(db:Session,organization_id:UUID|None,actor_user_id:UUID|None,action:str,entity_type:str,entity_id:UUID|None=None,metadata:dict|None=None)->None:
 db.add(AuditLog(organization_id=organization_id,actor_user_id=actor_user_id,action=action,entity_type=entity_type,entity_id=entity_id,metadata_=metadata or {}))
