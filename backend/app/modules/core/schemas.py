from uuid import UUID
from pydantic import BaseModel,EmailStr,Field
class LoginRequest(BaseModel): email:EmailStr; password:str=Field(min_length=8)
class TokenResponse(BaseModel): access_token:str; refresh_token:str; token_type:str="bearer"
class RefreshRequest(BaseModel): refresh_token:str=Field(min_length=20)
class UserCreate(BaseModel): email:EmailStr; display_name:str=Field(min_length=1,max_length=200); password:str=Field(min_length=8); organization_id:UUID|None=None; role_ids:list[UUID]=Field(default_factory=list)
class UserRead(BaseModel): id:UUID; email:EmailStr; display_name:str; status:str; organization_id:UUID|None
class RoleRead(BaseModel): id:UUID; name:str; description:str|None
class PermissionRead(BaseModel): id:UUID; key:str; description:str|None
class AuditLogRead(BaseModel): id:UUID; action:str; entity_type:str; entity_id:UUID|None; actor_user_id:UUID|None; metadata_:dict; created_at:datetime
