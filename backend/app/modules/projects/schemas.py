from datetime import datetime
from uuid import UUID
from pydantic import BaseModel,Field
class ProjectCreate(BaseModel):
 name:str=Field(min_length=1,max_length=200)
 client_name:str|None=Field(default=None,max_length=200)
 description:str|None=None
 status:str="planned"
 owner_user_id:UUID|None=None
 start_date:datetime|None=None
 due_date:datetime|None=None
class ProjectUpdate(BaseModel):
 name:str|None=Field(default=None,min_length=1,max_length=200)
 client_name:str|None=Field(default=None,max_length=200)
 description:str|None=None
 status:str|None=None
 owner_user_id:UUID|None=None
 start_date:datetime|None=None
 due_date:datetime|None=None
class ProjectRead(ProjectCreate):
 id:UUID
 organization_id:UUID
 created_at:datetime
 updated_at:datetime
class TaskCreate(BaseModel):
 title:str=Field(min_length=1,max_length=240)
 description:str|None=None
 status:str="todo"
 priority:str="medium"
 assignee_user_id:UUID|None=None
 due_date:datetime|None=None
class TaskUpdate(BaseModel):
 title:str|None=Field(default=None,min_length=1,max_length=240)
 description:str|None=None
 status:str|None=None
 priority:str|None=None
 assignee_user_id:UUID|None=None
 due_date:datetime|None=None
class TaskRead(TaskCreate):
 id:UUID
 organization_id:UUID
 project_id:UUID
 created_at:datetime
 updated_at:datetime
