from datetime import datetime
from uuid import UUID
from pydantic import BaseModel, Field

class ChannelCreate(BaseModel):
 name:str=Field(min_length=1,max_length=120)
 description:str|None=None
 channel_type:str="public"

class ChannelRead(ChannelCreate):
 id:UUID
 organization_id:UUID
 created_by_user_id:UUID
 created_at:datetime
 updated_at:datetime

class MessageCreate(BaseModel):
 body:str=Field(min_length=1,max_length=10000)

class MessageRead(BaseModel):
 id:UUID
 organization_id:UUID
 channel_id:UUID
 sender_user_id:UUID
 body:str
 is_edited:bool
 created_at:datetime
 updated_at:datetime

class MemberAdd(BaseModel):
 user_id:UUID
