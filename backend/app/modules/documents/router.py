from datetime import datetime,timezone
from uuid import UUID,uuid4
from fastapi import APIRouter,Depends,HTTPException
from sqlalchemy import select,func
from sqlalchemy.orm import Session
from ...db import get_db
from ...config import settings
from ..core.models import User
from ..core.dependencies import require_permission
from ..core.audit import record
from ..projects.models import Project
from ..crm.models import Client
from .models import DocumentFolder,Document,DocumentVersion
from .schemas import FolderCreate,FolderRead,DocumentCreate,DocumentRead,DocumentVersionCreate,DocumentVersionRead,UploadUrlRequest,UploadUrlRead,DownloadUrlRead
from .storage import presigned_upload,presigned_download
router=APIRouter()
def org_folder(db,user,id): return db.scalar(select(DocumentFolder).where(DocumentFolder.id==id,DocumentFolder.organization_id==user.organization_id))
def org_doc(db,user,id): return db.scalar(select(Document).where(Document.id==id,Document.organization_id==user.organization_id))
@router.get("/folders",response_model=list[FolderRead])
def folders(user:User=Depends(require_permission("documents.read")),db:Session=Depends(get_db)): return db.scalars(select(DocumentFolder).where(DocumentFolder.organization_id==user.organization_id).order_by(DocumentFolder.name)).all()
@router.post("/folders",response_model=FolderRead,status_code=201)
def create_folder(p:FolderCreate,user:User=Depends(require_permission("documents.create")),db:Session=Depends(get_db)):
 if p.parent_folder_id and not org_folder(db,user,p.parent_folder_id): raise HTTPException(400,"Parent folder not found")
 f=DocumentFolder(organization_id=user.organization_id,created_by_user_id=user.id,**p.model_dump());db.add(f);db.flush();record(db,user.organization_id,user.id,"create","document_folder",f.id,{"name":f.name});db.commit();db.refresh(f);return f
@router.post("/upload-url",response_model=UploadUrlRead)
def upload_url(p:UploadUrlRequest,user:User=Depends(require_permission("documents.create")),db:Session=Depends(get_db)):
 if p.folder_id and not org_folder(db,user,p.folder_id): raise HTTPException(400,"Folder not found")
 if p.client_id and not db.scalar(select(Client).where(Client.id==p.client_id,Client.organization_id==user.organization_id)): raise HTTPException(400,"Client not found")
 if p.project_id and not db.scalar(select(Project).where(Project.id==p.project_id,Project.organization_id==user.organization_id)): raise HTTPException(400,"Project not found")
 key=f"{user.organization_id}/{p.project_id or p.client_id or 'general'}/{uuid4()}/{p.name}"
 return {"storage_key":key,"upload_url":presigned_upload(key,p.mime_type),"expires_in":settings.storage_presign_seconds}

@router.get("",response_model=list[DocumentRead])
def documents(user:User=Depends(require_permission("documents.read")),db:Session=Depends(get_db),folder_id:UUID|None=None,client_id:UUID|None=None,project_id:UUID|None=None):
 q=select(Document).where(Document.organization_id==user.organization_id)
 if folder_id:q=q.where(Document.folder_id==folder_id)
 if client_id:q=q.where(Document.client_id==client_id)
 if project_id:q=q.where(Document.project_id==project_id)
 return db.scalars(q.order_by(Document.updated_at.desc())).all()
@router.post("",response_model=DocumentRead,status_code=201)
def create_document(p:DocumentCreate,user:User=Depends(require_permission("documents.create")),db:Session=Depends(get_db)):
 if p.folder_id and not org_folder(db,user,p.folder_id): raise HTTPException(400,"Folder not found")
 if p.client_id and not db.scalar(select(Client).where(Client.id==p.client_id,Client.organization_id==user.organization_id)): raise HTTPException(400,"Client not found")
 if p.project_id and not db.scalar(select(Project).where(Project.id==p.project_id,Project.organization_id==user.organization_id)): raise HTTPException(400,"Project not found")
 d=Document(organization_id=user.organization_id,uploaded_by_user_id=user.id,**p.model_dump());db.add(d);db.flush()
 v=DocumentVersion(organization_id=user.organization_id,document_id=d.id,version_number=1,storage_key=d.storage_key,mime_type=d.mime_type,size_bytes=d.size_bytes,checksum=d.checksum,uploaded_by_user_id=user.id);db.add(v)
 record(db,user.organization_id,user.id,"create","document",d.id,{"name":d.name});db.commit();db.refresh(d);return d
@router.get("/{document_id}/versions",response_model=list[DocumentVersionRead])
def versions(document_id:UUID,user:User=Depends(require_permission("documents.read")),db:Session=Depends(get_db)):
 if not org_doc(db,user,document_id): raise HTTPException(404,"Document not found")
 return db.scalars(select(DocumentVersion).where(DocumentVersion.document_id==document_id,DocumentVersion.organization_id==user.organization_id).order_by(DocumentVersion.version_number.desc())).all()
@router.post("/{document_id}/versions",response_model=DocumentVersionRead,status_code=201)
def add_version(document_id:UUID,p:DocumentVersionCreate,user:User=Depends(require_permission("documents.create")),db:Session=Depends(get_db)):
 d=org_doc(db,user,document_id)
 if not d: raise HTTPException(404,"Document not found")
 n=int(db.scalar(select(func.coalesce(func.max(DocumentVersion.version_number),0)).where(DocumentVersion.document_id==document_id,DocumentVersion.organization_id==user.organization_id)) or 0)+1
 v=DocumentVersion(organization_id=user.organization_id,document_id=document_id,version_number=n,uploaded_by_user_id=user.id,**p.model_dump());db.add(v)
 d.storage_key=p.storage_key;d.mime_type=p.mime_type;d.size_bytes=p.size_bytes;d.checksum=p.checksum;d.updated_at=datetime.now(timezone.utc)
 record(db,user.organization_id,user.id,"create","document_version",v.id,{"document_id":str(document_id),"version":n});db.commit();db.refresh(v);return v
@router.get("/{document_id}/download-url",response_model=DownloadUrlRead)
def download_url(document_id:UUID,user:User=Depends(require_permission("documents.read")),db:Session=Depends(get_db)):
 d=org_doc(db,user,document_id)
 if not d: raise HTTPException(404,"Document not found")
 return {"download_url":presigned_download(d.storage_key),"expires_in":settings.storage_presign_seconds}
