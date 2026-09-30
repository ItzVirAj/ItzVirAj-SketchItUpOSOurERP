from datetime import datetime
from uuid import UUID
from pydantic import BaseModel,Field
class FolderCreate(BaseModel): name:str=Field(min_length=1,max_length=240); description:str|None=None; parent_folder_id:UUID|None=None
class FolderRead(FolderCreate): id:UUID; organization_id:UUID; created_by_user_id:UUID; created_at:datetime; updated_at:datetime
class DocumentCreate(BaseModel):
 name:str=Field(min_length=1,max_length=240); description:str|None=None; storage_key:str=Field(min_length=1,max_length=1000); mime_type:str|None=None; size_bytes:int|None=Field(default=None,ge=0); checksum:str|None=None; folder_id:UUID|None=None; client_id:UUID|None=None; project_id:UUID|None=None
class DocumentRead(DocumentCreate): id:UUID; organization_id:UUID; uploaded_by_user_id:UUID; created_at:datetime; updated_at:datetime
class DocumentVersionCreate(BaseModel): storage_key:str=Field(min_length=1,max_length=1000); mime_type:str|None=None; size_bytes:int|None=Field(default=None,ge=0); checksum:str|None=None
class DocumentVersionRead(DocumentVersionCreate): id:UUID; organization_id:UUID; document_id:UUID; version_number:int; uploaded_by_user_id:UUID; created_at:datetime
class UploadUrlRequest(BaseModel):
 name:str=Field(min_length=1,max_length=240)
 mime_type:str|None=None
 folder_id:UUID|None=None
 client_id:UUID|None=None
 project_id:UUID|None=None

class UploadUrlRead(BaseModel):
 storage_key:str
 upload_url:str
 expires_in:int

class DownloadUrlRead(BaseModel):
 download_url:str
 expires_in:int
