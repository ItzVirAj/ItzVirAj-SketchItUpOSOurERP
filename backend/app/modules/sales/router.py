from datetime import datetime,timezone
from uuid import UUID
from fastapi import APIRouter,Depends,HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session
from ...db import get_db
from ..core.models import User
from ..core.dependencies import require_permission
from ..core.audit import record
from ..notifications.service import create_notification
from .models import Proposal,Contract
from .schemas import ProposalCreate,ProposalUpdate,ProposalRead,ContractCreate,ContractUpdate,ContractRead,ContractStatusUpdate

router=APIRouter()

def org_obj(db,model,user,obj_id):
    return db.scalar(select(model).where(model.id==obj_id,model.organization_id==user.organization_id))

def validate_links(db,user,lead_id=None,client_id=None,project_id=None):
    from ..crm.models import Lead,Client
    from ..projects.models import Project
    lead=org_obj(db,Lead,user,lead_id) if lead_id else None
    client=org_obj(db,Client,user,client_id) if client_id else None
    project=org_obj(db,Project,user,project_id) if project_id else None
    if lead_id and not lead: raise HTTPException(400,"Lead not found in your organization")
    if client_id and not client: raise HTTPException(400,"Client not found in your organization")
    if project_id and not project: raise HTTPException(400,"Project not found in your organization")
    return lead,client,project

@router.get("/proposals",response_model=list[ProposalRead])
def list_proposals(user:User=Depends(require_permission("sales.read")),db:Session=Depends(get_db)):
    return db.scalars(select(Proposal).where(Proposal.organization_id==user.organization_id).order_by(Proposal.updated_at.desc())).all()

@router.post("/proposals",response_model=ProposalRead,status_code=201)
def create_proposal(payload:ProposalCreate,user:User=Depends(require_permission("sales.create")),db:Session=Depends(get_db)):
    validate_links(db,user,payload.lead_id,payload.client_id,payload.project_id)
    proposal=Proposal(organization_id=user.organization_id,created_by_user_id=user.id,**payload.model_dump())
    db.add(proposal);db.flush();record(db,user.organization_id,user.id,"create","proposal",proposal.id,{"title":proposal.title});db.commit();db.refresh(proposal);return proposal

@router.post("/proposals/{proposal_id}/send",response_model=ProposalRead)
def send_proposal(proposal_id:UUID,user:User=Depends(require_permission("sales.create")),db:Session=Depends(get_db)):
    proposal=org_obj(db,Proposal,user,proposal_id)
    if not proposal: raise HTTPException(404,"Proposal not found")
    if proposal.status not in {"draft","revised"}:
        raise HTTPException(400,"Only draft or revised proposals can be sent")
    proposal.status="sent"
    proposal.updated_at=datetime.now(timezone.utc)
    record(db,user.organization_id,user.id,"status_change","proposal",proposal.id,{"from":"draft_or_revised","to":"sent"})
    db.commit();db.refresh(proposal);return proposal

@router.post("/proposals/{proposal_id}/accept",response_model=ContractRead,status_code=201)
def accept_proposal(proposal_id:UUID,user:User=Depends(require_permission("sales.create")),db:Session=Depends(get_db)):
    proposal=org_obj(db,Proposal,user,proposal_id)
    if not proposal: raise HTTPException(404,"Proposal not found")
    if proposal.status!="sent":
        raise HTTPException(400,"Only sent proposals can be accepted")
    existing_contract=db.scalar(select(Contract).where(Contract.organization_id==user.organization_id,Contract.proposal_id==proposal.id))
    if existing_contract:
        raise HTTPException(409,"A contract already exists for this proposal")
    if not proposal.client_id:
        raise HTTPException(400,"Proposal must be linked to a client before acceptance")
    from ..crm.models import Client
    client=org_obj(db,Client,user,proposal.client_id)
    if not client: raise HTTPException(400,"Proposal client not found")
    proposal.status="accepted"
    proposal.updated_at=datetime.now(timezone.utc)
    contract=Contract(
        organization_id=user.organization_id,
        proposal_id=proposal.id,
        lead_id=proposal.lead_id,
        client_id=proposal.client_id,
        project_id=proposal.project_id,
        title=proposal.title,
        status="draft",
        value=proposal.amount,
        currency=proposal.currency,
        terms=proposal.terms,
        created_by_user_id=user.id,
    )
    db.add(contract);db.flush()
    record(db,user.organization_id,user.id,"status_change","proposal",proposal.id,{"from":"sent","to":"accepted","contract_id":str(contract.id)})
    record(db,user.organization_id,user.id,"create","contract",contract.id,{"proposal_id":str(proposal.id)})
    db.commit();db.refresh(contract);return contract

@router.patch("/proposals/{proposal_id}",response_model=ProposalRead)
def update_proposal(proposal_id:UUID,payload:ProposalUpdate,user:User=Depends(require_permission("sales.create")),db:Session=Depends(get_db)):
    proposal=org_obj(db,Proposal,user,proposal_id)
    if not proposal: raise HTTPException(404,"Proposal not found")
    data=payload.model_dump(exclude_unset=True)
    validate_links(db,user,data.get("lead_id",proposal.lead_id),data.get("client_id",proposal.client_id),data.get("project_id",proposal.project_id))
    for key,value in data.items(): setattr(proposal,key,value)
    proposal.updated_at=datetime.now(timezone.utc)
    record(db,user.organization_id,user.id,"update","proposal",proposal.id);db.commit();db.refresh(proposal);return proposal

@router.get("/contracts",response_model=list[ContractRead])
def list_contracts(user:User=Depends(require_permission("sales.read")),db:Session=Depends(get_db)):
    return db.scalars(select(Contract).where(Contract.organization_id==user.organization_id).order_by(Contract.updated_at.desc())).all()

@router.post("/contracts",response_model=ContractRead,status_code=201)
def create_contract(payload:ContractCreate,user:User=Depends(require_permission("sales.create")),db:Session=Depends(get_db)):
    validate_links(db,user,payload.lead_id,payload.client_id,payload.project_id)
    if payload.proposal_id and not org_obj(db,Proposal,user,payload.proposal_id):
        raise HTTPException(400,"Proposal not found in your organization")
    contract=Contract(organization_id=user.organization_id,created_by_user_id=user.id,**payload.model_dump())
    db.add(contract);db.flush();record(db,user.organization_id,user.id,"create","contract",contract.id,{"title":contract.title});db.commit();db.refresh(contract);return contract

@router.post("/contracts/{contract_id}/status",response_model=ContractRead)
def update_contract_status(contract_id:UUID,payload:ContractStatusUpdate,user:User=Depends(require_permission("sales.create")),db:Session=Depends(get_db)):
    contract=org_obj(db,Contract,user,contract_id)
    if not contract: raise HTTPException(404,"Contract not found")
    allowed={
        "draft":{"sent","terminated"},
        "sent":{"signed","terminated"},
        "signed":{"active","terminated"},
        "active":{"completed","terminated"},
        "completed":set(),
        "terminated":set(),
    }
    current=contract.status
    status=payload.status
    if status not in allowed.get(current,set()):
        raise HTTPException(400,f"Invalid contract transition: {current} -> {status}")
    if status=="signed" and not contract.signed_at:
        contract.signed_at=datetime.now(timezone.utc)
    if status=="active" and not contract.signed_at:
        raise HTTPException(400,"Contract must be signed before activation")
    if status=="active" and contract.project_id:
        from ..projects.models import Project
        project=org_obj(db,Project,user,contract.project_id)
        if not project: raise HTTPException(400,"Contract project not found")
        if project.status in {"planned","draft"}:
            project.status="active"
            project.updated_at=datetime.now(timezone.utc)
    contract.status=status
    contract.updated_at=datetime.now(timezone.utc)
    record(db,user.organization_id,user.id,"status_change","contract",contract.id,{"from":current,"to":status})
    db.commit();db.refresh(contract);return contract

@router.patch("/contracts/{contract_id}",response_model=ContractRead)
def update_contract(contract_id:UUID,payload:ContractUpdate,user:User=Depends(require_permission("sales.create")),db:Session=Depends(get_db)):
    contract=org_obj(db,Contract,user,contract_id)
    if not contract: raise HTTPException(404,"Contract not found")
    data=payload.model_dump(exclude_unset=True)
    validate_links(db,user,data.get("lead_id",contract.lead_id),data.get("client_id",contract.client_id),data.get("project_id",contract.project_id))
    if data.get("proposal_id") and not org_obj(db,Proposal,user,data["proposal_id"]):
        raise HTTPException(400,"Proposal not found in your organization")
    for key,value in data.items(): setattr(contract,key,value)
    contract.updated_at=datetime.now(timezone.utc)
    record(db,user.organization_id,user.id,"update","contract",contract.id);db.commit();db.refresh(contract);return contract
