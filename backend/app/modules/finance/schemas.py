from datetime import datetime
from uuid import UUID
from pydantic import BaseModel,Field,field_validator

class InvoiceCreate(BaseModel):
 invoice_number:str=Field(min_length=1,max_length=80)
 client_id:UUID
 project_id:UUID|None=None
 contract_id:UUID|None=None
 currency:str="INR"
 subtotal:float=0
 tax_amount:float=0
 total_amount:float=0
 due_at:datetime|None=None
 notes:str|None=None

 @field_validator("currency")
 @classmethod
 def valid_currency(cls,value):
  value=value.upper()
  if len(value)!=3: raise ValueError("Currency must be a 3-letter ISO code")
  return value

class InvoiceStatusUpdate(BaseModel):
 status:str

class InvoiceRead(InvoiceCreate):
 id:UUID
 organization_id:UUID
 status:str
 created_by_user_id:UUID
 created_at:datetime
 updated_at:datetime

class MilestoneCreate(BaseModel):
 name:str=Field(min_length=1,max_length=160)
 percentage:float|None=None
 amount:float
 due_at:datetime|None=None

class MilestoneRead(MilestoneCreate):
 id:UUID
 organization_id:UUID
 invoice_id:UUID
 status:str
 created_at:datetime

class PaymentCreate(BaseModel):
 amount:float=Field(gt=0)
 currency:str="INR"
 payment_method:str=Field(min_length=1,max_length=40)
 reference:str|None=None
 paid_at:datetime
 notes:str|None=None

class PaymentRead(PaymentCreate):
 id:UUID
 organization_id:UUID
 invoice_id:UUID
 created_by_user_id:UUID
 created_at:datetime
