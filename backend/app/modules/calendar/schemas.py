from datetime import datetime
from uuid import UUID
from pydantic import BaseModel,Field,model_validator

class EventCreate(BaseModel):
    title:str=Field(min_length=1,max_length=240)
    description:str|None=None
    event_type:str=Field(default="meeting",min_length=1,max_length=40)
    starts_at:datetime
    ends_at:datetime
    location:str|None=Field(default=None,max_length=500)
    is_all_day:bool=False
    project_id:UUID|None=None

    @model_validator(mode="after")
    def validate_times(self):
        if self.ends_at<=self.starts_at:
            raise ValueError("ends_at must be after starts_at")
        return self

class EventUpdate(BaseModel):
    title:str|None=Field(default=None,min_length=1,max_length=240)
    description:str|None=None
    event_type:str|None=Field(default=None,min_length=1,max_length=40)
    starts_at:datetime|None=None
    ends_at:datetime|None=None
    location:str|None=Field(default=None,max_length=500)
    is_all_day:bool|None=None
    project_id:UUID|None=None

class EventRead(EventCreate):
    id:UUID
    organization_id:UUID
    created_by_user_id:UUID
    created_at:datetime
    updated_at:datetime
