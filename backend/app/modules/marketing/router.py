from datetime import datetime,timezone,date
import csv,io
from uuid import UUID
from fastapi import APIRouter,Depends,HTTPException,UploadFile,File
from sqlalchemy import func,select
from sqlalchemy.orm import Session
from ...db import get_db
from ..core.models import User
from ..core.dependencies import require_permission
from ..core.audit import record
from ..crm.models import Lead,PipelineStage
from ..finance.models import Payment,Invoice
from ..sales.models import Contract
from .models import MarketingChannel,Campaign,CampaignChannel,ContentItem,Gig,Bid,MarketingMetric,BrandAsset
from .schemas import *

CONTENT_TRANSITIONS={"idea":{"draft"},"draft":{"design","review"},"design":{"review"},"review":{"approved","draft"},"approved":{"scheduled","draft"},"scheduled":{"published","approved"},"published":{"repurposed"},"repurposed":set()}

def update_fields(obj,payload):
 for key,value in payload.model_dump(exclude_unset=True).items(): setattr(obj,key,value)
 obj.updated_at=datetime.now(timezone.utc)


router=APIRouter()

def org_user(db,user,user_id):
 if user_id is None:return True
 return db.scalar(select(User.id).where(User.id==user_id,User.organization_id==user.organization_id,User.status=="active")) is not None

def require_org(db,user,model,object_id):
 obj=db.scalar(select(model).where(model.id==object_id,model.organization_id==user.organization_id))
 if not obj: raise HTTPException(400,"Referenced record not found in your organization")
 return obj


CSV_IMPORT_TYPES={"gigs","bids","metrics"}

def csv_int(row,key,default=None):
 value=row.get(key)
 if value in (None,""): return default
 return int(value)

def csv_float(row,key,default=None):
 value=row.get(key)
 if value in (None,""): return default
 return float(value)

def csv_date(row,key):
 value=row.get(key)
 if not value:return None
 return date.fromisoformat(value)

def csv_datetime(row,key):
 value=row.get(key)
 if not value:return None
 return datetime.fromisoformat(value.replace("Z","+00:00"))

def import_row(db,user,kind,row):
 if kind=="gigs":
  marketplace=(row.get("marketplace") or "").strip();title=(row.get("title") or "").strip()
  if not marketplace or not title: raise ValueError("marketplace and title are required")
  obj=db.scalar(select(Gig).where(Gig.organization_id==user.organization_id,Gig.marketplace==marketplace,Gig.title==title))
  values={"marketplace":marketplace,"title":title,"category":row.get("category") or None,"keywords":row.get("keywords") or None,"impressions":csv_int(row,"impressions",0),"clicks":csv_int(row,"clicks",0),"inquiries":csv_int(row,"inquiries",0),"orders":csv_int(row,"orders",0),"reviews":csv_int(row,"reviews",0),"last_optimised_at":csv_datetime(row,"last_optimised_at")}
  if obj:\n   for key,value in values.items(): setattr(obj,key,value)\n   obj.updated_at=datetime.now(timezone.utc)\n   return obj,"updated"
  obj=Gig(organization_id=user.organization_id,**values);db.add(obj);db.flush();return obj,"created"
 if kind=="bids":
  marketplace=(row.get("marketplace") or "Upwork").strip();job_url=(row.get("job_url") or "").strip() or None
  if not job_url: raise ValueError("job_url is required for bid imports")
  obj=db.scalar(select(Bid).where(Bid.organization_id==user.organization_id,Bid.job_url==job_url))
  gig_id=UUID(row["gig_id"]) if row.get("gig_id") else None
  if gig_id: require_org(db,user,Gig,gig_id)
  values={"gig_id":gig_id,"marketplace":marketplace,"job_url":job_url,"job_title":row.get("job_title") or None,"bid_amount":csv_float(row,"bid_amount"),"connects_used":csv_int(row,"connects_used"),"status":row.get("status") or "sent","outcome":row.get("outcome") or None,"learning_notes":row.get("learning_notes") or None}
  if values["status"] not in {"sent","viewed","interview","hired","declined"}: raise ValueError("invalid bid status")
  if obj:\n   for key,value in values.items(): setattr(obj,key,value)\n   obj.updated_at=datetime.now(timezone.utc)\n   return obj,"updated"
  obj=Bid(organization_id=user.organization_id,**values);db.add(obj);db.flush();return obj,"created"
 if kind=="metrics":
  period=csv_date(row,"period_start")
  if not period: raise ValueError("period_start is required")
  channel_id=UUID(row["channel_id"]) if row.get("channel_id") else None;campaign_id=UUID(row["campaign_id"]) if row.get("campaign_id") else None
  if channel_id: require_org(db,user,MarketingChannel,channel_id)
  if campaign_id: require_org(db,user,Campaign,campaign_id)
  obj=db.scalar(select(MarketingMetric).where(MarketingMetric.organization_id==user.organization_id,MarketingMetric.period_start==period,MarketingMetric.channel_id==channel_id,MarketingMetric.campaign_id==campaign_id))
  values={"channel_id":channel_id,"campaign_id":campaign_id,"period_start":period,"followers":csv_int(row,"followers"),"impressions":csv_int(row,"impressions"),"engagement_rate":csv_float(row,"engagement_rate"),"website_visits":csv_int(row,"website_visits"),"leads":csv_int(row,"leads"),"cost_per_lead":csv_float(row,"cost_per_lead"),"conversion_rate":csv_float(row,"conversion_rate"),"revenue":csv_float(row,"revenue")}
  if obj:\n   for key,value in values.items(): setattr(obj,key,value)\n   obj.updated_at=datetime.now(timezone.utc)\n   return obj,"updated"
  obj=MarketingMetric(organization_id=user.organization_id,**values);db.add(obj);db.flush();return obj,"created"
 raise ValueError("Unsupported import type")

@router.post("/imports/csv",response_model=ImportResult)
def import_csv(import_type:str,file:UploadFile=File(...),user:User=Depends(require_permission("marketing.create")),db:Session=Depends(get_db)):
 if import_type not in CSV_IMPORT_TYPES: raise HTTPException(400,"import_type must be gigs, bids, or metrics")
 if not file.filename or not file.filename.lower().endswith(".csv"): raise HTTPException(400,"Only CSV files are supported")
 raw=file.file.read()
 if len(raw)>5*1024*1024: raise HTTPException(413,"CSV file exceeds 5 MB limit")
 try: text=raw.decode("utf-8-sig")
 except UnicodeDecodeError: raise HTTPException(400,"CSV must be UTF-8 encoded")
 reader=csv.DictReader(io.StringIO(text))
 if not reader.fieldnames: raise HTTPException(400,"CSV header is required")
 required={"gigs":{"marketplace","title"},"bids":{"job_url"},"metrics":{"period_start"}}[import_type]
 missing=required-set(reader.fieldnames)
 if missing: raise HTTPException(400,"Missing required columns: "+", ".join(sorted(missing)))
 rows=list(reader)
 if len(rows)>5000: raise HTTPException(413,"CSV cannot contain more than 5000 data rows")
 results=[];created=updated=failed=0
 for number,row in enumerate(rows,2):
  try:
   with db.begin_nested():
    obj,action=import_row(db,user,import_type,row);db.flush();record(db,user.organization_id,user.id,"import","marketing_"+import_type,obj.id,{"source":"csv","row":number,"filename":file.filename})
   results.append(ImportRowResult(row=number,status=action,record_id=obj.id));created+=action=="created";updated+=action=="updated"
  except Exception as exc:
   failed+=1;results.append(ImportRowResult(row=number,status="failed",error=str(exc)[:300]))
 db.commit()
 return ImportResult(import_type=import_type,total_rows=len(rows),created=created,updated=updated,failed=failed,rows=results)

@router.patch("/channels/{channel_id}",response_model=ChannelRead)
def update_channel(channel_id:UUID,payload:ChannelUpdate,user:User=Depends(require_permission("marketing.create")),db:Session=Depends(get_db)):
 obj=require_org(db,user,MarketingChannel,channel_id);data=payload.model_dump(exclude_unset=True)
 if "owner_user_id" in data and not org_user(db,user,data["owner_user_id"]): raise HTTPException(400,"Owner must be an active organization user")
 if "name" in data and data["name"]!=obj.name and db.scalar(select(MarketingChannel).where(MarketingChannel.organization_id==user.organization_id,MarketingChannel.name==data["name"],MarketingChannel.id!=obj.id)): raise HTTPException(409,"Channel already exists")
 if "status" in data and data["status"] not in {"active","paused","archived"}: raise HTTPException(400,"Invalid channel status")
 update_fields(obj,payload);record(db,user.organization_id,user.id,"update","marketing_channel",obj.id,data);db.commit();db.refresh(obj);return obj

@router.patch("/campaigns/{campaign_id}",response_model=CampaignRead)
def update_campaign(campaign_id:UUID,payload:CampaignUpdate,user:User=Depends(require_permission("marketing.create")),db:Session=Depends(get_db)):
 obj=require_org(db,user,Campaign,campaign_id);data=payload.model_dump(exclude_unset=True);starts=data.get("starts_at",obj.starts_at);ends=data.get("ends_at",obj.ends_at)
 if starts and ends and ends<=starts: raise HTTPException(400,"ends_at must be after starts_at")
 if "owner_user_id" in data and not org_user(db,user,data["owner_user_id"]): raise HTTPException(400,"Owner must be an active organization user")
 update_fields(obj,payload);record(db,user.organization_id,user.id,"update","marketing_campaign",obj.id,data);db.commit();db.refresh(obj);return obj

@router.patch("/content/{content_id}",response_model=ContentRead)
def update_content(content_id:UUID,payload:ContentUpdate,user:User=Depends(require_permission("marketing.create")),db:Session=Depends(get_db)):
 obj=require_org(db,user,ContentItem,content_id);data=payload.model_dump(exclude_unset=True)
 if "campaign_id" in data and data["campaign_id"]: require_org(db,user,Campaign,data["campaign_id"])
 if "channel_id" in data and data["channel_id"]: require_org(db,user,MarketingChannel,data["channel_id"])
 if "approval_status" in data:
  new=data["approval_status"]
  if new not in CONTENT_TRANSITIONS: raise HTTPException(400,"Invalid content workflow status")
  if new!=obj.approval_status and new not in CONTENT_TRANSITIONS[obj.approval_status]: raise HTTPException(409,f"Invalid content transition: {obj.approval_status} -> {new}")
  if new in {"scheduled","published"} and not data.get("publish_at",obj.publish_at): raise HTTPException(400,"publish_at is required when scheduling or publishing content")
 update_fields(obj,payload);record(db,user.organization_id,user.id,"update","marketing_content",obj.id,data);db.commit();db.refresh(obj);return obj

@router.patch("/gigs/{gig_id}",response_model=GigRead)
def update_gig(gig_id:UUID,payload:GigUpdate,user:User=Depends(require_permission("marketing.create")),db:Session=Depends(get_db)):
 obj=require_org(db,user,Gig,gig_id);update_fields(obj,payload);record(db,user.organization_id,user.id,"update","marketing_gig",obj.id,payload.model_dump(exclude_unset=True));db.commit();db.refresh(obj);return obj

@router.patch("/bids/{bid_id}",response_model=BidRead)
def update_bid(bid_id:UUID,payload:BidUpdate,user:User=Depends(require_permission("marketing.create")),db:Session=Depends(get_db)):
 obj=require_org(db,user,Bid,bid_id);data=payload.model_dump(exclude_unset=True)
 if "gig_id" in data and data["gig_id"]: require_org(db,user,Gig,data["gig_id"])
 if "status" in data and data["status"] not in {"sent","viewed","interview","hired","declined"}: raise HTTPException(400,"Invalid bid status")
 update_fields(obj,payload);record(db,user.organization_id,user.id,"update","marketing_bid",obj.id,data);db.commit();db.refresh(obj);return obj

@router.patch("/metrics/{metric_id}",response_model=MetricRead)
def update_metric(metric_id:UUID,payload:MetricUpdate,user:User=Depends(require_permission("marketing.create")),db:Session=Depends(get_db)):
 obj=require_org(db,user,MarketingMetric,metric_id);data=payload.model_dump(exclude_unset=True)
 if "channel_id" in data and data["channel_id"]: require_org(db,user,MarketingChannel,data["channel_id"])
 if "campaign_id" in data and data["campaign_id"]: require_org(db,user,Campaign,data["campaign_id"])
 update_fields(obj,payload);record(db,user.organization_id,user.id,"update","marketing_metric",obj.id,data);db.commit();db.refresh(obj);return obj

@router.get("/channels",response_model=list[ChannelRead])
def list_channels(user:User=Depends(require_permission("marketing.read")),db:Session=Depends(get_db)):
 return db.scalars(select(MarketingChannel).where(MarketingChannel.organization_id==user.organization_id).order_by(MarketingChannel.name)).all()

@router.post("/channels",response_model=ChannelRead,status_code=201)
def create_channel(payload:ChannelCreate,user:User=Depends(require_permission("marketing.create")),db:Session=Depends(get_db)):
 if not org_user(db,user,payload.owner_user_id): raise HTTPException(400,"Owner must be an active organization user")
 if db.scalar(select(MarketingChannel).where(MarketingChannel.organization_id==user.organization_id,MarketingChannel.name==payload.name)): raise HTTPException(409,"Channel already exists")
 obj=MarketingChannel(organization_id=user.organization_id,**payload.model_dump());db.add(obj);db.flush();record(db,user.organization_id,user.id,"create","marketing_channel",obj.id,{"name":obj.name});db.commit();db.refresh(obj);return obj

@router.get("/campaigns",response_model=list[CampaignRead])
def list_campaigns(user:User=Depends(require_permission("marketing.read")),db:Session=Depends(get_db)):
 return db.scalars(select(Campaign).where(Campaign.organization_id==user.organization_id).order_by(Campaign.updated_at.desc())).all()

@router.post("/campaigns",response_model=CampaignRead,status_code=201)
def create_campaign(payload:CampaignCreate,user:User=Depends(require_permission("marketing.create")),db:Session=Depends(get_db)):
 if payload.starts_at and payload.ends_at and payload.ends_at<=payload.starts_at: raise HTTPException(400,"ends_at must be after starts_at")
 if not org_user(db,user,payload.owner_user_id): raise HTTPException(400,"Owner must be an active organization user")
 obj=Campaign(organization_id=user.organization_id,**payload.model_dump());db.add(obj);db.flush();record(db,user.organization_id,user.id,"create","marketing_campaign",obj.id,{"name":obj.name});db.commit();db.refresh(obj);return obj

@router.post("/campaigns/{campaign_id}/channels",status_code=201)
def add_campaign_channel(campaign_id:UUID,payload:CampaignChannelAdd,user:User=Depends(require_permission("marketing.create")),db:Session=Depends(get_db)):
 require_org(db,user,Campaign,campaign_id);require_org(db,user,MarketingChannel,payload.channel_id)
 if db.scalar(select(CampaignChannel).where(CampaignChannel.campaign_id==campaign_id,CampaignChannel.channel_id==payload.channel_id)): raise HTTPException(409,"Channel already linked")
 db.add(CampaignChannel(campaign_id=campaign_id,channel_id=payload.channel_id));db.commit();return {"campaign_id":campaign_id,"channel_id":payload.channel_id}

@router.get("/content",response_model=list[ContentRead])
def list_content(user:User=Depends(require_permission("marketing.read")),db:Session=Depends(get_db)):
 return db.scalars(select(ContentItem).where(ContentItem.organization_id==user.organization_id).order_by(ContentItem.publish_at.asc().nullslast(),ContentItem.created_at.desc())).all()

@router.post("/content",response_model=ContentRead,status_code=201)
def create_content(payload:ContentCreate,user:User=Depends(require_permission("marketing.create")),db:Session=Depends(get_db)):
 if not org_user(db,user,payload.owner_user_id): raise HTTPException(400,"Owner must be an active organization user")
 if payload.campaign_id: require_org(db,user,Campaign,payload.campaign_id)
 if payload.channel_id: require_org(db,user,MarketingChannel,payload.channel_id)
 obj=ContentItem(organization_id=user.organization_id,**payload.model_dump());db.add(obj);db.flush();record(db,user.organization_id,user.id,"create","marketing_content",obj.id,{"title":obj.title});db.commit();db.refresh(obj);return obj

@router.get("/gigs",response_model=list[GigRead])
def list_gigs(user:User=Depends(require_permission("marketing.read")),db:Session=Depends(get_db)):
 return db.scalars(select(Gig).where(Gig.organization_id==user.organization_id).order_by(Gig.updated_at.desc())).all()

@router.post("/gigs",response_model=GigRead,status_code=201)
def create_gig(payload:GigCreate,user:User=Depends(require_permission("marketing.create")),db:Session=Depends(get_db)):
 obj=Gig(organization_id=user.organization_id,**payload.model_dump());db.add(obj);db.flush();record(db,user.organization_id,user.id,"create","marketing_gig",obj.id,{"title":obj.title});db.commit();db.refresh(obj);return obj

@router.get("/bids",response_model=list[BidRead])
def list_bids(user:User=Depends(require_permission("marketing.read")),db:Session=Depends(get_db)):
 return db.scalars(select(Bid).where(Bid.organization_id==user.organization_id).order_by(Bid.created_at.desc())).all()

@router.post("/bids",response_model=BidRead,status_code=201)
def create_bid(payload:BidCreate,user:User=Depends(require_permission("marketing.create")),db:Session=Depends(get_db)):
 if payload.gig_id: require_org(db,user,Gig,payload.gig_id)
 obj=Bid(organization_id=user.organization_id,**payload.model_dump());db.add(obj);db.flush();record(db,user.organization_id,user.id,"create","marketing_bid",obj.id);db.commit();db.refresh(obj);return obj

@router.get("/metrics",response_model=list[MetricRead])
def list_metrics(user:User=Depends(require_permission("marketing.read")),db:Session=Depends(get_db)):
 return db.scalars(select(MarketingMetric).where(MarketingMetric.organization_id==user.organization_id).order_by(MarketingMetric.period_start.desc())).all()

@router.post("/metrics",response_model=MetricRead,status_code=201)
def create_metric(payload:MetricCreate,user:User=Depends(require_permission("marketing.create")),db:Session=Depends(get_db)):
 if payload.channel_id: require_org(db,user,MarketingChannel,payload.channel_id)
 if payload.campaign_id: require_org(db,user,Campaign,payload.campaign_id)
 obj=MarketingMetric(organization_id=user.organization_id,**payload.model_dump());db.add(obj);db.flush();record(db,user.organization_id,user.id,"create","marketing_metric",obj.id);db.commit();db.refresh(obj);return obj

@router.get("/assets",response_model=list[BrandAssetRead])
def list_assets(user:User=Depends(require_permission("marketing.read")),db:Session=Depends(get_db)):
 return db.scalars(select(BrandAsset).where(BrandAsset.organization_id==user.organization_id).order_by(BrandAsset.created_at.desc())).all()

@router.post("/assets",response_model=BrandAssetRead,status_code=201)
def create_asset(payload:BrandAssetCreate,user:User=Depends(require_permission("marketing.create")),db:Session=Depends(get_db)):
 obj=BrandAsset(organization_id=user.organization_id,created_by_user_id=user.id,**payload.model_dump());db.add(obj);db.flush();record(db,user.organization_id,user.id,"create","marketing_brand_asset",obj.id);db.commit();db.refresh(obj);return obj

@router.get("/attribution",response_model=list[AttributionRead])
def attribution(user:User=Depends(require_permission("marketing.read")),db:Session=Depends(get_db)):
 lead_count=select(func.count(Lead.id)).where(Lead.campaign_id==Campaign.id,Lead.organization_id==user.organization_id).scalar_subquery()
 won_count=select(func.count(Lead.id)).join(PipelineStage,PipelineStage.id==Lead.stage_id).where(Lead.campaign_id==Campaign.id,Lead.organization_id==user.organization_id,PipelineStage.is_closed_won.is_(True)).scalar_subquery()
 won_value=select(func.coalesce(func.sum(Lead.estimated_value),0)).join(PipelineStage,PipelineStage.id==Lead.stage_id).where(Lead.campaign_id==Campaign.id,Lead.organization_id==user.organization_id,PipelineStage.is_closed_won.is_(True)).scalar_subquery()
 collected=select(func.coalesce(func.sum(Payment.amount),0)).join(Invoice,Invoice.id==Payment.invoice_id).join(Contract,Contract.id==Invoice.contract_id).join(Lead,Lead.id==Contract.lead_id).where(Lead.campaign_id==Campaign.id,Lead.organization_id==user.organization_id).scalar_subquery()
 rows=db.execute(select(Campaign.id,Campaign.name,lead_count,won_count,won_value,collected).where(Campaign.organization_id==user.organization_id).order_by(Campaign.name)).all()
 return [AttributionRead(campaign_id=r[0],campaign_name=r[1],leads=int(r[2] or 0),won_leads=int(r[3] or 0),estimated_won_value=float(r[4] or 0),collected_revenue=float(r[5] or 0)) for r in rows]
