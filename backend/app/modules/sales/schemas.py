from datetime import datetime
from uuid import UUID
from pydantic import BaseModel,Field,field_validator

class ProposalCreate(BaseModel):
    title:str=Field(min_length=1,max_length=240)
    lead_id:UUID|None=None
    client_id:UUID|None=None
    project_id:UUID|None=None
    amount:float|None=None
    currency:str="INR"
    valid_until:datetime|None=None
    terms:str|None=None
    notes:str|None=None

class ProposalUpdate(BaseModel):
    title:str|None=Field(default=None,min_length=1,max_length=240)
    status:str|None=None
    lead_id:UUID|None=None
    client_id:UUID|None=None
    project_id:UUID|None=None
    amount:float|None=None
    currency:str|None=None
    valid_until:datetime|None=None
    terms:str|None=None
    notes:str|None=None

class ProposalRead(ProposalCreate):
    id:UUID
    organization_id:UUID
    status:str
    created_by_user_id:UUID
    created_at:datetime
    updated_at:datetime

class ContractCreate(BaseModel):
    title:str=Field(min_length=1,max_length=240)
    client_id:UUID
    proposal_id:UUID|None=None
    lead_id:UUID|None=None
    project_id:UUID|None=None
    contract_number:str|None=None
    signed_at:datetime|None=None
    start_date:datetime|None=None
    end_date:datetime|None=None
    value:float|None=None
    currency:str="INR"
    terms:str|None=None

class ContractStatusUpdate(BaseModel):
    status:str

    @field_validator("status")
    @classmethod
    def valid_status(cls,value):
        allowed={"draft","sent","signed","active","completed","terminated"}
        if value not in allowed: raise ValueError("Invalid contract status")
        return value

class ContractUpdate(BaseModel):
    title:str|None=Field(default=None,min_length=1,max_length=240)
    status:str|None=None
    contract_number:str|None=None
    proposal_id:UUID|None=None
    lead_id:UUID|None=None
    client_id:UUID|None=None
    project_id:UUID|None=None
    signed_at:datetime|None=None
    start_date:datetime|None=None
    end_date:datetime|None=None
    value:float|None=None
    currency:str|None=None
    terms:str|None=None

class ContractRead(ContractCreate):
    id:UUID
    organization_id:UUID
    status:str
    created_by_user_id:UUID
    created_at:datetime
    updated_at:datetime
