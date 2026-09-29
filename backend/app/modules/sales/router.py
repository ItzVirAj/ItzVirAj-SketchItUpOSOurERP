from datetime import datetime,timezone
from uuid import UUID
from fastapi import APIRouter,Depends,HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session
from ...db import get_db
from ..core.models import User
from ..core.dependencies import require_permission
from ..core.audit import record
from .models import Proposal,Contract
from .schemas import ProposalCreate,ProposalUpdate,ProposalRead,ContractCreate,ContractUpdate,ContractRead

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
