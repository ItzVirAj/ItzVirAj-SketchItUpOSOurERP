from datetime import datetime
from uuid import UUID
from pydantic import BaseModel,Field
class NotificationCreate(BaseModel):
 user_id:UUID; type:str=Field(min_length=1,max_length=60); title:str=Field(min_length=1,max_length=240); body:str|None=None; entity_type:str|None=None; entity_id:UUID|None=None; action_url:str|None=None
class NotificationRead(NotificationCreate):
 id:UUID; organization_id:UUID; is_read:bool; read_at:datetime|None=None; created_at:datetime
class NotificationReadUpdate(BaseModel): is_read:bool=True