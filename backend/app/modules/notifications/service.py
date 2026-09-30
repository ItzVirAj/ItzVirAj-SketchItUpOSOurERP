from uuid import UUID
from sqlalchemy.orm import Session
from .models import Notification
def create_notification(db:Session,organization_id:UUID,user_id:UUID,type:str,title:str,body:str|None=None,entity_type:str|None=None,entity_id:UUID|None=None,action_url:str|None=None):
 n=Notification(organization_id=organization_id,user_id=user_id,type=type,title=title,body=body,entity_type=entity_type,entity_id=entity_id,action_url=action_url)
 db.add(n);return n