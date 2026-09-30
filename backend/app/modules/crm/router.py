from datetime import datetime,timezone
from uuid import UUID
from fastapi import APIRouter,Depends,HTTPException,Query
from sqlalchemy import select,func
from sqlalchemy.orm import Session
from ...db import get_db
from ..core.models import User
from ..core.dependencies import require_permission
from ..core.audit import record
from ..projects.models import Project
from ..notifications.service import create_notification
from ..marketing.models import Campaign
from .models import Client,Contact,Lead,LeadActivity,LeadFollowUp,Pipeline,PipelineStage
from .schemas import ClientCreate,ClientUpdate,ClientRead,ContactCreate,ContactRead,LeadCreate,LeadUpdate,LeadRead,ActivityCreate,ActivityRead,FollowUpCreate,FollowUpComplete,FollowUpRead,PipelineRead,StageRead,LeadConversionRead,LeadBulkStageUpdate

router=APIRouter()

def org_user(db,user,user_id):
    return db.scalar(select(User).where(User.id==user_id,User.organization_id==user.organization_id,User.deleted_at.is_(None)))

def pipeline_stage(db,user,pipeline_id,stage_id):
    return db.scalar(select(PipelineStage).where(PipelineStage.id==stage_id,PipelineStage.pipeline_id==pipeline_id,PipelineStage.organization_id==user.organization_id))

def org_client(db,user,client_id):
    return db.scalar(select(Client).where(Client.id==client_id,Client.organization_id==user.organization_id))

@router.get("/clients",response_model=list[ClientRead])
def list_clients(user:User=Depends(require_permission("crm.read")),db:Session=Depends(get_db)):
    return db.scalars(select(Client).where(Client.organization_id==user.organization_id).order_by(Client.name)).all()

@router.post("/clients",response_model=ClientRead,status_code=201)
def create_client(payload:ClientCreate,user:User=Depends(require_permission("crm.create")),db:Session=Depends(get_db)):
    client=Client(organization_id=user.organization_id,status="active",**payload.model_dump())
    db.add(client);db.flush();record(db,user.organization_id,user.id,"create","client",client.id,{"name":client.name});db.commit();db.refresh(client);return client

@router.patch("/clients/{client_id}",response_model=ClientRead)
def update_client(client_id:UUID,payload:ClientUpdate,user:User=Depends(require_permission("crm.create")),db:Session=Depends(get_db)):
    client=org_client(db,user,client_id)
    if not client: raise HTTPException(404,"Client not found")
    for key,value in payload.model_dump(exclude_unset=True).items(): setattr(client,key,value)
    client.updated_at=datetime.now(timezone.utc)
    record(db,user.organization_id,user.id,"update","client",client.id);db.commit();db.refresh(client);return client

@router.get("/clients/{client_id}/contacts",response_model=list[ContactRead])
def list_contacts(client_id:UUID,user:User=Depends(require_permission("crm.read")),db:Session=Depends(get_db)):
    if not org_client(db,user,client_id): raise HTTPException(404,"Client not found")
    return db.scalars(select(Contact).where(Contact.client_id==client_id,Contact.organization_id==user.organization_id).order_by(Contact.name)).all()

@router.post("/contacts",response_model=ContactRead,status_code=201)
def create_contact(payload:ContactCreate,user:User=Depends(require_permission("crm.create")),db:Session=Depends(get_db)):
    if not org_client(db,user,payload.client_id): raise HTTPException(400,"Client must belong to your organization")
    contact=Contact(organization_id=user.organization_id,**payload.model_dump())
    db.add(contact);db.flush();record(db,user.organization_id,user.id,"create","contact",contact.id,{"client_id":str(contact.client_id)});db.commit();db.refresh(contact);return contact

@router.get("/pipelines",response_model=list[PipelineRead])
def list_pipelines(user:User=Depends(require_permission("crm.read")),db:Session=Depends(get_db)):
    return db.scalars(select(Pipeline).where(Pipeline.organization_id==user.organization_id,Pipeline.is_active.is_(True)).order_by(Pipeline.name)).all()

@router.get("/pipelines/{pipeline_id}/stages",response_model=list[StageRead])
def list_stages(pipeline_id:UUID,user:User=Depends(require_permission("crm.read")),db:Session=Depends(get_db)):
    pipeline=db.scalar(select(Pipeline).where(Pipeline.id==pipeline_id,Pipeline.organization_id==user.organization_id))
    if not pipeline: raise HTTPException(404,"Pipeline not found")
    return db.scalars(select(PipelineStage).where(PipelineStage.pipeline_id==pipeline_id,PipelineStage.organization_id==user.organization_id).order_by(PipelineStage.position)).all()

@router.get("/leads",response_model=list[LeadRead])
def list_leads(
    user:User=Depends(require_permission("crm.read")),db:Session=Depends(get_db),
    search:str|None=Query(default=None,max_length=120),pipeline_id:UUID|None=None,stage_id:UUID|None=None,
    owner_user_id:UUID|None=None,temperature:str|None=None,client_id:UUID|None=None,
    limit:int=Query(default=50,ge=1,le=100),offset:int=Query(default=0,ge=0)
):
    q=select(Lead).where(Lead.organization_id==user.organization_id)
    if search:
        term=f"%{search.strip()}%";q=q.where((Lead.name.ilike(term))|(Lead.company.ilike(term))|(Lead.email.ilike(term))|(Lead.phone.ilike(term)))
    if pipeline_id: q=q.where(Lead.pipeline_id==pipeline_id)
    if stage_id: q=q.where(Lead.stage_id==stage_id)
    if owner_user_id: q=q.where(Lead.owner_user_id==owner_user_id)
    if client_id: q=q.where(Lead.client_id==client_id)
    if temperature:
        if temperature not in {"Cold","Warm","Hot"}: raise HTTPException(400,"Temperature must be Cold, Warm, or Hot")
        q=q.where(Lead.temperature==temperature)
    return db.scalars(q.order_by(Lead.updated_at.desc()).offset(offset).limit(limit)).all()

@router.post("/leads/bulk-stage",response_model=dict)
def bulk_update_stage(payload:LeadBulkStageUpdate,user:User=Depends(require_permission("crm.create")),db:Session=Depends(get_db)):
    stage=db.scalar(select(PipelineStage).where(PipelineStage.id==payload.stage_id,PipelineStage.organization_id==user.organization_id))
    if not stage: raise HTTPException(404,"Stage not found")
    leads=db.scalars(select(Lead).where(Lead.id.in_(payload.lead_ids),Lead.organization_id==user.organization_id)).all()
    if len(leads)!=len(set(payload.lead_ids)): raise HTTPException(400,"One or more leads were not found in your organization")
    if stage.is_closed_lost:
        missing=[str(l.id) for l in leads if not l.lost_reason]
        if missing: raise HTTPException(400,"Lost reason is required before moving leads to a Lost stage")
    if not stage.is_closed_won:
        missing=[str(l.id) for l in leads if not l.next_follow_up_at]
        if missing: raise HTTPException(400,"Active leads require a next follow-up date")
    now=datetime.now(timezone.utc)
    for lead in leads:
        if lead.pipeline_id!=stage.pipeline_id: raise HTTPException(400,"All selected leads must belong to the target pipeline")
        lead.stage_id=stage.id;lead.updated_at=now
        record(db,user.organization_id,user.id,"bulk_stage_change","lead",lead.id,{"stage_id":str(stage.id)})
    db.commit();return {"updated":len(leads),"stage_id":stage.id}

@router.post("/leads",response_model=LeadRead,status_code=201)
def create_lead(payload:LeadCreate,user:User=Depends(require_permission("crm.create")),db:Session=Depends(get_db)):
    stage=pipeline_stage(db,user,payload.pipeline_id,payload.stage_id)
    if not stage: raise HTTPException(400,"Stage does not belong to the selected pipeline")
    if not payload.owner_user_id: raise HTTPException(400,"Lead owner is required")
    if not org_user(db,user,payload.owner_user_id): raise HTTPException(400,"Lead owner must belong to your organization")
    if stage.is_closed_lost and not payload.lost_reason: raise HTTPException(400,"Lost reason is required")
    if not stage.is_closed_won and not payload.next_follow_up_at: raise HTTPException(400,"Active leads require a next follow-up date")
    if payload.campaign_id and not db.scalar(select(Campaign.id).where(Campaign.id==payload.campaign_id,Campaign.organization_id==user.organization_id)):
        raise HTTPException(400,"Campaign must belong to your organization")
    if payload.client_id and not org_client(db,user,payload.client_id): raise HTTPException(400,"Client must belong to your organization")
    if payload.contact_id:
        contact=db.scalar(select(Contact).where(Contact.id==payload.contact_id,Contact.organization_id==user.organization_id))
        if not contact or (payload.client_id and contact.client_id!=payload.client_id): raise HTTPException(400,"Contact must belong to the selected client")
    if payload.temperature not in {"Cold","Warm","Hot"}: raise HTTPException(400,"Temperature must be Cold, Warm, or Hot")
    lead=Lead(organization_id=user.organization_id,**payload.model_dump())
    db.add(lead);db.flush();record(db,user.organization_id,user.id,"create","lead",lead.id,{"name":lead.name});db.commit();db.refresh(lead);return lead

@router.patch("/leads/{lead_id}",response_model=LeadRead)
def update_lead(lead_id:UUID,payload:LeadUpdate,user:User=Depends(require_permission("crm.create")),db:Session=Depends(get_db)):
    lead=db.scalar(select(Lead).where(Lead.id==lead_id,Lead.organization_id==user.organization_id))
    if not lead: raise HTTPException(404,"Lead not found")
    data=payload.model_dump(exclude_unset=True)
    pipeline_id=data.get("pipeline_id",lead.pipeline_id)
    stage_id=data.get("stage_id",lead.stage_id)
    stage=pipeline_stage(db,user,pipeline_id,stage_id)
    if not stage: raise HTTPException(400,"Stage does not belong to the selected pipeline")
    owner_id=data.get("owner_user_id",lead.owner_user_id)
    if not owner_id: raise HTTPException(400,"Lead owner is required")
    if not org_user(db,user,owner_id): raise HTTPException(400,"Lead owner must belong to your organization")
    next_follow_up=data.get("next_follow_up_at",lead.next_follow_up_at)
    if not stage.is_closed_won and not next_follow_up: raise HTTPException(400,"Active leads require a next follow-up date")
    lost_reason=data.get("lost_reason",lead.lost_reason)
    if stage.is_closed_lost and not lost_reason: raise HTTPException(400,"Lost reason is required")
    campaign_id=data.get("campaign_id",lead.campaign_id)
    if campaign_id and not db.scalar(select(Campaign.id).where(Campaign.id==campaign_id,Campaign.organization_id==user.organization_id)):
        raise HTTPException(400,"Campaign must belong to your organization")
    client_id=data.get("client_id",lead.client_id)
    if client_id and not org_client(db,user,client_id): raise HTTPException(400,"Client must belong to your organization")
    contact_id=data.get("contact_id",lead.contact_id)
    if contact_id:
        contact=db.scalar(select(Contact).where(Contact.id==contact_id,Contact.organization_id==user.organization_id))
        if not contact or (client_id and contact.client_id!=client_id): raise HTTPException(400,"Contact must belong to the selected client")
    temperature=data.get("temperature",lead.temperature)
    if temperature not in {"Cold","Warm","Hot"}: raise HTTPException(400,"Temperature must be Cold, Warm, or Hot")
    for key,value in data.items(): setattr(lead,key,value)
    lead.updated_at=datetime.now(timezone.utc)
    record(db,user.organization_id,user.id,"update","lead",lead.id,{"stage_id":str(stage.id)});db.commit();db.refresh(lead);return lead

@router.get("/leads/{lead_id}/activities",response_model=list[ActivityRead])
def list_activities(lead_id:UUID,user:User=Depends(require_permission("crm.read")),db:Session=Depends(get_db)):
    lead=db.scalar(select(Lead).where(Lead.id==lead_id,Lead.organization_id==user.organization_id))
    if not lead: raise HTTPException(404,"Lead not found")
    return db.scalars(select(LeadActivity).where(LeadActivity.lead_id==lead_id,LeadActivity.organization_id==user.organization_id).order_by(LeadActivity.occurred_at.desc())).all()

@router.post("/leads/{lead_id}/activities",response_model=ActivityRead,status_code=201)
def create_activity(lead_id:UUID,payload:ActivityCreate,user:User=Depends(require_permission("crm.create")),db:Session=Depends(get_db)):
    lead=db.scalar(select(Lead).where(Lead.id==lead_id,Lead.organization_id==user.organization_id))
    if not lead: raise HTTPException(404,"Lead not found")
    activity=LeadActivity(organization_id=user.organization_id,lead_id=lead.id,actor_user_id=user.id,occurred_at=payload.occurred_at or datetime.now(timezone.utc),**payload.model_dump(exclude={"occurred_at"}))
    db.add(activity);db.flush();record(db,user.organization_id,user.id,"create","lead_activity",activity.id,{"lead_id":str(lead.id)});db.commit();db.refresh(activity);return activity

@router.post("/leads/{lead_id}/follow-ups",response_model=FollowUpRead,status_code=201)
def create_follow_up(lead_id:UUID,payload:FollowUpCreate,user:User=Depends(require_permission("crm.create")),db:Session=Depends(get_db)):
    lead=db.scalar(select(Lead).where(Lead.id==lead_id,Lead.organization_id==user.organization_id))
    if not lead: raise HTTPException(404,"Lead not found")
    follow=LeadFollowUp(organization_id=user.organization_id,lead_id=lead.id,assigned_user_id=lead.owner_user_id or user.id,**payload.model_dump())
    db.add(follow);db.flush();lead.next_follow_up_at=payload.due_at;lead.updated_at=datetime.now(timezone.utc)
    record(db,user.organization_id,user.id,"create","lead_follow_up",follow.id,{"lead_id":str(lead.id)})
    if follow.assigned_user_id:
        create_notification(db,user.organization_id,follow.assigned_user_id,"crm.follow_up","New CRM follow-up",f"Follow-up for {lead.name} is due.","lead",lead.id,f"/crm/leads/{lead.id}")
    db.commit();db.refresh(follow);return follow

@router.post("/leads/{lead_id}/follow-ups/{follow_up_id}/complete",response_model=FollowUpRead)
def complete_follow_up(lead_id:UUID,follow_up_id:UUID,payload:FollowUpComplete|None=None,user:User=Depends(require_permission("crm.create")),db:Session=Depends(get_db)):
    lead=db.scalar(select(Lead).where(Lead.id==lead_id,Lead.organization_id==user.organization_id))
    if not lead: raise HTTPException(404,"Lead not found")
    follow=db.scalar(select(LeadFollowUp).where(LeadFollowUp.id==follow_up_id,LeadFollowUp.lead_id==lead_id,LeadFollowUp.organization_id==user.organization_id))
    if not follow: raise HTTPException(404,"Follow-up not found")
    if follow.completed_at: return follow
    follow.completed_at=datetime.now(timezone.utc)
    if payload and payload.notes is not None: follow.notes=payload.notes
    next_follow=db.scalar(select(LeadFollowUp).where(LeadFollowUp.lead_id==lead_id,LeadFollowUp.organization_id==user.organization_id,LeadFollowUp.completed_at.is_(None),LeadFollowUp.id!=follow.id).order_by(LeadFollowUp.due_at).limit(1))
    lead.next_follow_up_at=next_follow.due_at if next_follow else None
    lead.updated_at=datetime.now(timezone.utc)
    record(db,user.organization_id,user.id,"complete","lead_follow_up",follow.id,{"lead_id":str(lead_id)})
    db.commit();db.refresh(follow);return follow

@router.get("/leads/{lead_id}/follow-ups",response_model=list[FollowUpRead])
def list_follow_ups(lead_id:UUID,user:User=Depends(require_permission("crm.read")),db:Session=Depends(get_db)):
    lead=db.scalar(select(Lead).where(Lead.id==lead_id,Lead.organization_id==user.organization_id))
    if not lead: raise HTTPException(404,"Lead not found")
    return db.scalars(select(LeadFollowUp).where(LeadFollowUp.lead_id==lead_id,LeadFollowUp.organization_id==user.organization_id).order_by(LeadFollowUp.due_at)).all()


@router.post("/leads/{lead_id}/convert",response_model=LeadConversionRead)
def convert_lead(lead_id:UUID,user:User=Depends(require_permission("crm.create")),db:Session=Depends(get_db)):
    lead=db.scalar(select(Lead).where(Lead.id==lead_id,Lead.organization_id==user.organization_id))
    if not lead:
        raise HTTPException(404,"Lead not found")
    stage=db.scalar(select(PipelineStage).where(PipelineStage.id==lead.stage_id,PipelineStage.organization_id==user.organization_id))
    if not stage or not stage.is_closed_won:
        raise HTTPException(400,"Only a Won lead can be converted")
    if lead.client_id:
        client=org_client(db,user,lead.client_id)
        if not client:
            raise HTTPException(400,"Linked client does not belong to your organization")
    else:
        client=Client(
            organization_id=user.organization_id,
            name=lead.company or lead.name,
            industry=lead.industry,
            email=lead.email,
            phone=lead.phone,
            notes=lead.requirement_summary,
            status="active",
        )
        db.add(client);db.flush()
        record(db,user.organization_id,user.id,"create","client",client.id,{"source_lead_id":str(lead.id)})

    if lead.contact_id:
        contact=db.scalar(select(Contact).where(Contact.id==lead.contact_id,Contact.organization_id==user.organization_id))
        if not contact:
            raise HTTPException(400,"Linked contact does not belong to your organization")
    else:
        contact=Contact(
            organization_id=user.organization_id,
            client_id=client.id,
            name=lead.name,
            email=lead.email,
            phone=lead.phone,
            is_primary=True,
        )
        db.add(contact);db.flush()
        record(db,user.organization_id,user.id,"create","contact",contact.id,{"source_lead_id":str(lead.id)})

    project=Project(
        organization_id=user.organization_id,
        client_id=client.id,
        client_name=client.name,
        name=f"{lead.name} — Project",
        description=lead.requirement_summary,
        status="planned",
        owner_user_id=lead.owner_user_id,
    )
    db.add(project);db.flush()

    lead.client_id=client.id
    lead.contact_id=contact.id
    lead.updated_at=datetime.now(timezone.utc)
    record(db,user.organization_id,user.id,"convert","lead",lead.id,{
        "client_id":str(client.id),
        "contact_id":str(contact.id),
        "project_id":str(project.id),
    })
    db.commit()
    return LeadConversionRead(
        lead_id=lead.id,
        client_id=client.id,
        contact_id=contact.id,
        project_id=project.id,
    )
