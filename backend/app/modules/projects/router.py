from fastapi import APIRouter,Depends,HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session
from ...db import get_db
from ..core.models import User
from ..core.dependencies import current_user,require_permission
from ..core.audit import record
from .models import Project,Task
from .schemas import ProjectCreate,ProjectRead,TaskCreate,TaskRead
router=APIRouter()
@router.get("",response_model=list[ProjectRead])
def list_projects(user:User=Depends(require_permission("projects.read")),db:Session=Depends(get_db)):
 return db.scalars(select(Project).where(Project.organization_id==user.organization_id).order_by(Project.created_at.desc())).all()
@router.post("",response_model=ProjectRead,status_code=201)
def create_project(payload:ProjectCreate,user:User=Depends(require_permission("projects.create")),db:Session=Depends(get_db)):
 if payload.owner_user_id:
  owner=db.scalar(select(User).where(User.id==payload.owner_user_id,User.organization_id==user.organization_id,User.deleted_at.is_(None)))
  if not owner: raise HTTPException(400,"Project owner must belong to your organization")
 project=Project(organization_id=user.organization_id,**payload.model_dump())
 db.add(project);db.flush();record(db,user.organization_id,user.id,"create","project",project.id,{"name":project.name});db.commit();db.refresh(project);return project
@router.get("/{project_id}/tasks",response_model=list[TaskRead])
def list_tasks(project_id,user:User=Depends(require_permission("tasks.read")),db:Session=Depends(get_db)):
 project=db.scalar(select(Project).where(Project.id==project_id,Project.organization_id==user.organization_id))
 if not project: raise HTTPException(404,"Project not found")
 return db.scalars(select(Task).where(Task.project_id==project.id,Task.organization_id==user.organization_id).order_by(Task.created_at.desc())).all()
@router.post("/{project_id}/tasks",response_model=TaskRead,status_code=201)
def create_task(project_id,payload:TaskCreate,user:User=Depends(require_permission("tasks.create")),db:Session=Depends(get_db)):
 project=db.scalar(select(Project).where(Project.id==project_id,Project.organization_id==user.organization_id))
 if not project: raise HTTPException(404,"Project not found")
 if payload.assignee_user_id:
  assignee=db.scalar(select(User).where(User.id==payload.assignee_user_id,User.organization_id==user.organization_id,User.deleted_at.is_(None)))
  if not assignee: raise HTTPException(400,"Task assignee must belong to your organization")
 task=Task(organization_id=user.organization_id,project_id=project.id,**payload.model_dump())
 db.add(task);db.flush();record(db,user.organization_id,user.id,"create","task",task.id,{"project_id":str(project.id)});db.commit();db.refresh(task);return task
