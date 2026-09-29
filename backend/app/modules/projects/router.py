from fastapi import APIRouter,Depends,HTTPException,status
from sqlalchemy import select
from sqlalchemy.orm import Session
from ...db import get_db
from ..core.models import User
from ..core.dependencies import require_permission
from ..core.audit import record
from ..crm.models import Client
from .models import Project,Task
from .schemas import ProjectCreate,ProjectUpdate,ProjectRead,TaskCreate,TaskUpdate,TaskRead
router=APIRouter()
def org_user(db,user,user_id):
 return db.scalar(select(User).where(User.id==user_id,User.organization_id==user.organization_id,User.deleted_at.is_(None)))
@router.get("",response_model=list[ProjectRead])
def list_projects(user:User=Depends(require_permission("projects.read")),db:Session=Depends(get_db)):
 return db.scalars(select(Project).where(Project.organization_id==user.organization_id).order_by(Project.created_at.desc())).all()
@router.post("",response_model=ProjectRead,status_code=201)
def create_project(payload:ProjectCreate,user:User=Depends(require_permission("projects.create")),db:Session=Depends(get_db)):
 if payload.owner_user_id and not org_user(db,user,payload.owner_user_id): raise HTTPException(400,"Project owner must belong to your organization")
 if payload.client_id and not db.scalar(select(Client).where(Client.id==payload.client_id,Client.organization_id==user.organization_id)): raise HTTPException(400,"Project client must belong to your organization")
 project=Project(organization_id=user.organization_id,**payload.model_dump())
 db.add(project);db.flush();record(db,user.organization_id,user.id,"create","project",project.id,{"name":project.name});db.commit();db.refresh(project);return project
@router.patch("/{project_id}",response_model=ProjectRead)
def update_project(project_id,payload:ProjectUpdate,user:User=Depends(require_permission("projects.create")),db:Session=Depends(get_db)):
 project=db.scalar(select(Project).where(Project.id==project_id,Project.organization_id==user.organization_id))
 if not project: raise HTTPException(404,"Project not found")
 if payload.owner_user_id and not org_user(db,user,payload.owner_user_id): raise HTTPException(400,"Project owner must belong to your organization")
 if payload.client_id and not db.scalar(select(Client).where(Client.id==payload.client_id,Client.organization_id==user.organization_id)): raise HTTPException(400,"Project client must belong to your organization")
 for key,value in payload.model_dump(exclude_unset=True).items(): setattr(project,key,value)
 project.updated_at=__import__("datetime").datetime.now(__import__("datetime").timezone.utc)
 record(db,user.organization_id,user.id,"update","project",project.id);db.commit();db.refresh(project);return project
@router.delete("/{project_id}",status_code=204)
def delete_project(project_id,user:User=Depends(require_permission("projects.create")),db:Session=Depends(get_db)):
 project=db.scalar(select(Project).where(Project.id==project_id,Project.organization_id==user.organization_id))
 if not project: raise HTTPException(404,"Project not found")
 record(db,user.organization_id,user.id,"delete","project",project.id);db.delete(project);db.commit()
@router.get("/{project_id}/tasks",response_model=list[TaskRead])
def list_tasks(project_id,user:User=Depends(require_permission("tasks.read")),db:Session=Depends(get_db)):
 project=db.scalar(select(Project).where(Project.id==project_id,Project.organization_id==user.organization_id))
 if not project: raise HTTPException(404,"Project not found")
 return db.scalars(select(Task).where(Task.project_id==project.id,Task.organization_id==user.organization_id).order_by(Task.created_at.desc())).all()
@router.post("/{project_id}/tasks",response_model=TaskRead,status_code=201)
def create_task(project_id,payload:TaskCreate,user:User=Depends(require_permission("tasks.create")),db:Session=Depends(get_db)):
 project=db.scalar(select(Project).where(Project.id==project_id,Project.organization_id==user.organization_id))
 if not project: raise HTTPException(404,"Project not found")
 if payload.assignee_user_id and not org_user(db,user,payload.assignee_user_id): raise HTTPException(400,"Task assignee must belong to your organization")
 task=Task(organization_id=user.organization_id,project_id=project.id,**payload.model_dump())
 db.add(task);db.flush();record(db,user.organization_id,user.id,"create","task",task.id,{"project_id":str(project.id)});db.commit();db.refresh(task);return task
@router.patch("/{project_id}/tasks/{task_id}",response_model=TaskRead)
def update_task(project_id,task_id,payload:TaskUpdate,user:User=Depends(require_permission("tasks.create")),db:Session=Depends(get_db)):
 task=db.scalar(select(Task).where(Task.id==task_id,Task.project_id==project_id,Task.organization_id==user.organization_id))
 if not task: raise HTTPException(404,"Task not found")
 if payload.assignee_user_id and not org_user(db,user,payload.assignee_user_id): raise HTTPException(400,"Task assignee must belong to your organization")
 for key,value in payload.model_dump(exclude_unset=True).items(): setattr(task,key,value)
 task.updated_at=__import__("datetime").datetime.now(__import__("datetime").timezone.utc)
 record(db,user.organization_id,user.id,"update","task",task.id);db.commit();db.refresh(task);return task
@router.delete("/{project_id}/tasks/{task_id}",status_code=204)
def delete_task(project_id,task_id,user:User=Depends(require_permission("tasks.create")),db:Session=Depends(get_db)):
 task=db.scalar(select(Task).where(Task.id==task_id,Task.project_id==project_id,Task.organization_id==user.organization_id))
 if not task: raise HTTPException(404,"Task not found")
 record(db,user.organization_id,user.id,"delete","task",task.id);db.delete(task);db.commit()
