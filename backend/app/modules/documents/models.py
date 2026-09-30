from datetime import datetime,timezone
from uuid import UUID
from sqlalchemy import String,Text,Integer,BigInteger,ForeignKey,DateTime,UniqueConstraint
from sqlalchemy.orm import Mapped,mapped_column
from ..core.base import BaseModel
class DocumentFolder(BaseModel):
 __tablename__="document_folders"
 id:Mapped[UUID]=mapped_column(primary_key=True,default=uuid4); organization_id:Mapped[object]=mapped_column(ForeignKey("organizations.id",ondelete="CASCADE"),index=True)
 parent_folder_id:Mapped[UUID|None]=mapped_column(ForeignKey("document_folders.id",ondelete="CASCADE"),nullable=True,index=True); name:Mapped[str]=mapped_column(String(240)); description:Mapped[str|None]=mapped_column(Text)
 created_by_user_id:Mapped[object]=mapped_column(ForeignKey("users.id")); created_at:Mapped[datetime]=mapped_column(DateTime(timezone=True),default=lambda:datetime.now(timezone.utc)); updated_at:Mapped[datetime]=mapped_column(DateTime(timezone=True),default=lambda:datetime.now(timezone.utc))
class Document(BaseModel):
 __tablename__="documents"
 id:Mapped[object]=mapped_column(primary_key=True,default=uuid4); organization_id:Mapped[object]=mapped_column(ForeignKey("organizations.id",ondelete="CASCADE"),index=True)
 folder_id:Mapped[object|None]=mapped_column(ForeignKey("document_folders.id",ondelete="SET NULL"),nullable=True,index=True); name:Mapped[str]=mapped_column(String(240)); description:Mapped[str|None]=mapped_column(Text)
 storage_key:Mapped[str]=mapped_column(Text); mime_type:Mapped[str|None]=mapped_column(String(120)); size_bytes:Mapped[int|None]=mapped_column(BigInteger); checksum:Mapped[str|None]=mapped_column(String(128))
 client_id:Mapped[object|None]=mapped_column(ForeignKey("clients.id",ondelete="SET NULL"),nullable=True,index=True); project_id:Mapped[object|None]=mapped_column(ForeignKey("projects.id",ondelete="SET NULL"),nullable=True,index=True)
 uploaded_by_user_id:Mapped[object]=mapped_column(ForeignKey("users.id")); created_at:Mapped[datetime]=mapped_column(DateTime(timezone=True),default=lambda:datetime.now(timezone.utc)); updated_at:Mapped[datetime]=mapped_column(DateTime(timezone=True),default=lambda:datetime.now(timezone.utc))
class DocumentVersion(BaseModel):
 __tablename__="document_versions"; __table_args__=(UniqueConstraint("document_id","version_number"),)
 id:Mapped[object]=mapped_column(primary_key=True,default=uuid4); organization_id:Mapped[object]=mapped_column(ForeignKey("organizations.id",ondelete="CASCADE"),index=True)
 document_id:Mapped[object]=mapped_column(ForeignKey("documents.id",ondelete="CASCADE"),index=True); version_number:Mapped[int]=mapped_column(Integer)
 storage_key:Mapped[str]=mapped_column(Text); mime_type:Mapped[str|None]=mapped_column(String(120)); size_bytes:Mapped[int|None]=mapped_column(BigInteger); checksum:Mapped[str|None]=mapped_column(String(128))
 uploaded_by_user_id:Mapped[object]=mapped_column(ForeignKey("users.id")); created_at:Mapped[datetime]=mapped_column(DateTime(timezone=True),default=lambda:datetime.now(timezone.utc))