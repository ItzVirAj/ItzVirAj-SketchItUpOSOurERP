from datetime import datetime
from uuid import UUID
from pydantic import BaseModel,Field
class ExpenseCreate(BaseModel):
 category:str=Field(min_length=1,max_length=80)
 description:str=Field(min_length=1)
 amount:float=Field(gt=0)
 currency:str="INR"
 project_id:UUID|None=None
 incurred_at:datetime
class ExpenseRead(ExpenseCreate):
 id:UUID
 organization_id:UUID
 status:str
 created_by_user_id:UUID
 created_at:datetime
