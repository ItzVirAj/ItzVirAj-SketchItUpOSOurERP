from datetime import datetime,timezone
from fastapi import APIRouter,Depends,HTTPException,status
from sqlalchemy import select
from sqlalchemy.orm import Session
from ...db import get_db
from ..core.models import User
from ..core.dependencies import require_permission
from ..core.audit import record
from ..projects.models import Project
from .models import Event
from .schemas import EventCreate,EventUpdate,EventRead

router=APIRouter()

def org_project(db:Session,user:User,project_id):
    return db.scalar(select(Project).where(Project.id==project_id,Project.organization_id==user.organization_id))

def validate_event_times(starts_at,ends_at):
    if starts_at is not None and ends_at is not None and ends_at<=starts_at:
        raise HTTPException(status_code=400,detail="ends_at must be after starts_at")

@router.get("",response_model=list[EventRead])
def list_events(user:User=Depends(require_permission("calendar.read")),db:Session=Depends(get_db)):
    return db.scalars(
        select(Event).where(Event.organization_id==user.organization_id).order_by(Event.starts_at.asc())
    ).all()

@router.post("",response_model=EventRead,status_code=201)
def create_event(payload:EventCreate,user:User=Depends(require_permission("calendar.create")),db:Session=Depends(get_db)):
    if payload.project_id and not org_project(db,user,payload.project_id):
        raise HTTPException(status_code=400,detail="Project must belong to your organization")
    event=Event(organization_id=user.organization_id,created_by_user_id=user.id,**payload.model_dump())
    db.add(event);db.flush()
    record(db,user.organization_id,user.id,"create","event",event.id,{"title":event.title})
    db.commit();db.refresh(event)
    return event

@router.patch("/{event_id}",response_model=EventRead)
def update_event(event_id,payload:EventUpdate,user:User=Depends(require_permission("calendar.create")),db:Session=Depends(get_db)):
    event=db.scalar(select(Event).where(Event.id==event_id,Event.organization_id==user.organization_id))
    if not event:
        raise HTTPException(status_code=404,detail="Event not found")
    data=payload.model_dump(exclude_unset=True)
    starts_at=data.get("starts_at",event.starts_at)
    ends_at=data.get("ends_at",event.ends_at)
    validate_event_times(starts_at,ends_at)
    if data.get("project_id") and not org_project(db,user,data["project_id"]):
        raise HTTPException(status_code=400,detail="Project must belong to your organization")
    for key,value in data.items():
        setattr(event,key,value)
    event.updated_at=datetime.now(timezone.utc)
    record(db,user.organization_id,user.id,"update","event",event.id)
    db.commit();db.refresh(event)
    return event

@router.delete("/{event_id}",status_code=status.HTTP_204_NO_CONTENT)
def delete_event(event_id,user:User=Depends(require_permission("calendar.create")),db:Session=Depends(get_db)):
    event=db.scalar(select(Event).where(Event.id==event_id,Event.organization_id==user.organization_id))
    if not event:
        raise HTTPException(status_code=404,detail="Event not found")
    record(db,user.organization_id,user.id,"delete","event",event.id)
    db.delete(event);db.commit()
