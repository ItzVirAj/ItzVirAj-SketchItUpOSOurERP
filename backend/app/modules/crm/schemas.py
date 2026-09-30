from datetime import datetime
from uuid import UUID
from pydantic import BaseModel,Field,model_validator

class ClientCreate(BaseModel):
    name:str=Field(min_length=1,max_length=240)
    industry:str|None=None
    website:str|None=None
    email:str|None=None
    phone:str|None=None
    gst_number:str|None=None
    notes:str|None=None

class ClientUpdate(ClientCreate):
    name:str|None=Field(default=None,min_length=1,max_length=240)
    status:str|None=None

class ClientRead(ClientCreate):
    id:UUID
    organization_id:UUID
    status:str
    created_at:datetime
    updated_at:datetime

class ContactCreate(BaseModel):
    client_id:UUID
    name:str=Field(min_length=1,max_length=200)
    role:str|None=None
    email:str|None=None
    phone:str|None=None
    communication_preference:str|None=None
    birthday:datetime|None=None
    anniversary:datetime|None=None
    is_primary:bool=False

class ContactRead(ContactCreate):
    id:UUID
    organization_id:UUID
    created_at:datetime
    updated_at:datetime

class LeadCreate(BaseModel):
    pipeline_id:UUID
    stage_id:UUID
    name:str=Field(min_length=1,max_length=240)
    company:str|None=None
    industry:str|None=None
    phone:str|None=None
    email:str|None=None
    source:str=Field(min_length=1,max_length=80)
    campaign:str|None=None
    campaign_id:UUID|None=None
    estimated_value:float|None=None
    expected_close_date:datetime|None=None
    requirement_summary:str|None=None
    owner_user_id:UUID|None=None
    temperature:str="Cold"
    next_follow_up_at:datetime|None=None
    client_id:UUID|None=None
    contact_id:UUID|None=None
    tags:str|None=None
    lost_reason:str|None=None
    lost_notes:str|None=None

class LeadUpdate(BaseModel):
    pipeline_id:UUID|None=None
    stage_id:UUID|None=None
    name:str|None=None
    company:str|None=None
    industry:str|None=None
    phone:str|None=None
    email:str|None=None
    source:str|None=None
    campaign:str|None=None
    campaign_id:UUID|None=None
    estimated_value:float|None=None
    expected_close_date:datetime|None=None
    requirement_summary:str|None=None
    owner_user_id:UUID|None=None
    temperature:str|None=None
    next_follow_up_at:datetime|None=None
    client_id:UUID|None=None
    contact_id:UUID|None=None
    lost_reason:str|None=None
    lost_notes:str|None=None
    tags:str|None=None

class LeadRead(LeadCreate):
    id:UUID
    organization_id:UUID
    lost_reason:str|None
    lost_notes:str|None
    created_at:datetime
    updated_at:datetime

class ActivityCreate(BaseModel):
    activity_type:str=Field(min_length=1,max_length=30)
    subject:str=Field(min_length=1,max_length=240)
    notes:str|None=None
    occurred_at:datetime|None=None

class ActivityRead(ActivityCreate):
    id:UUID
    organization_id:UUID
    lead_id:UUID
    actor_user_id:UUID

class FollowUpCreate(BaseModel):
    due_at:datetime
    action:str=Field(min_length=1,max_length=240)
    notes:str|None=None

class FollowUpComplete(BaseModel):
    notes:str|None=None

class FollowUpRead(FollowUpCreate):
    id:UUID
    organization_id:UUID
    lead_id:UUID
    assigned_user_id:UUID
    completed_at:datetime|None

class LeadConversionRead(BaseModel):
    lead_id:UUID
    client_id:UUID
    contact_id:UUID
    project_id:UUID

class PipelineRead(BaseModel):
    id:UUID
    organization_id:UUID
    name:str
    description:str|None
    is_active:bool

class StageRead(BaseModel):
    id:UUID
    organization_id:UUID
    pipeline_id:UUID
    name:str
    position:int
    probability:float
    is_closed_won:bool
    is_closed_lost:bool

class LeadBulkStageUpdate(BaseModel):
    lead_ids:list[UUID]=Field(min_length=1,max_length=100)
    stage_id:UUID
