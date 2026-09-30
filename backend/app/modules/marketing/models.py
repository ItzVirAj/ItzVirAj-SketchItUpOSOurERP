from datetime import date,datetime,timezone
from uuid import UUID,uuid4
from sqlalchemy import Date,DateTime,ForeignKey,Integer,JSON,Numeric,String,Text
from sqlalchemy.orm import Mapped,mapped_column
from ..core.base import BaseModel

class MarketingChannel(BaseModel):
 __tablename__="marketing_channels"
 id:Mapped[UUID]=mapped_column(primary_key=True,default=uuid4)
 organization_id:Mapped[UUID]=mapped_column(ForeignKey("organizations.id",ondelete="CASCADE"))
 name:Mapped[str]=mapped_column(String(120)); platform:Mapped[str]=mapped_column(String(60))
 profile_url:Mapped[str|None]=mapped_column(String(500)); owner_user_id:Mapped[UUID|None]=mapped_column(ForeignKey("users.id",ondelete="SET NULL"))
 status:Mapped[str]=mapped_column(String(30),default="active"); goals:Mapped[str|None]=mapped_column(Text); credentials_pointer:Mapped[str|None]=mapped_column(String(500))
 created_at:Mapped[datetime]=mapped_column(DateTime(timezone=True),default=lambda:datetime.now(timezone.utc)); updated_at:Mapped[datetime]=mapped_column(DateTime(timezone=True),default=lambda:datetime.now(timezone.utc))

class Campaign(BaseModel):
 __tablename__="marketing_campaigns"
 id:Mapped[UUID]=mapped_column(primary_key=True,default=uuid4); organization_id:Mapped[UUID]=mapped_column(ForeignKey("organizations.id",ondelete="CASCADE"))
 name:Mapped[str]=mapped_column(String(180)); objective:Mapped[str|None]=mapped_column(Text); audience:Mapped[str|None]=mapped_column(Text); budget:Mapped[float|None]=mapped_column(Numeric(14,2))
 starts_at:Mapped[datetime|None]=mapped_column(DateTime(timezone=True)); ends_at:Mapped[datetime|None]=mapped_column(DateTime(timezone=True)); utm_parameters:Mapped[dict|None]=mapped_column(JSON)
 owner_user_id:Mapped[UUID|None]=mapped_column(ForeignKey("users.id",ondelete="SET NULL")); created_at:Mapped[datetime]=mapped_column(DateTime(timezone=True),default=lambda:datetime.now(timezone.utc)); updated_at:Mapped[datetime]=mapped_column(DateTime(timezone=True),default=lambda:datetime.now(timezone.utc))

class CampaignChannel(BaseModel):
 __tablename__="marketing_campaign_channels"
 campaign_id:Mapped[UUID]=mapped_column(ForeignKey("marketing_campaigns.id",ondelete="CASCADE"),primary_key=True); channel_id:Mapped[UUID]=mapped_column(ForeignKey("marketing_channels.id",ondelete="CASCADE"),primary_key=True)

class ContentItem(BaseModel):
 __tablename__="marketing_content_items"
 id:Mapped[UUID]=mapped_column(primary_key=True,default=uuid4); organization_id:Mapped[UUID]=mapped_column(ForeignKey("organizations.id",ondelete="CASCADE"))
 campaign_id:Mapped[UUID|None]=mapped_column(ForeignKey("marketing_campaigns.id",ondelete="SET NULL")); channel_id:Mapped[UUID|None]=mapped_column(ForeignKey("marketing_channels.id",ondelete="SET NULL"))
 title:Mapped[str]=mapped_column(String(240)); idea:Mapped[str|None]=mapped_column(Text); format:Mapped[str]=mapped_column(String(40),default="post"); owner_user_id:Mapped[UUID|None]=mapped_column(ForeignKey("users.id",ondelete="SET NULL")); approval_status:Mapped[str]=mapped_column(String(30),default="idea")
 publish_at:Mapped[datetime|None]=mapped_column(DateTime(timezone=True)); asset_links:Mapped[list|None]=mapped_column(JSON); caption:Mapped[str|None]=mapped_column(Text); hashtags:Mapped[str|None]=mapped_column(Text)
 created_at:Mapped[datetime]=mapped_column(DateTime(timezone=True),default=lambda:datetime.now(timezone.utc)); updated_at:Mapped[datetime]=mapped_column(DateTime(timezone=True),default=lambda:datetime.now(timezone.utc))

class Gig(BaseModel):
 __tablename__="marketing_gigs"
 id:Mapped[UUID]=mapped_column(primary_key=True,default=uuid4); organization_id:Mapped[UUID]=mapped_column(ForeignKey("organizations.id",ondelete="CASCADE")); marketplace:Mapped[str]=mapped_column(String(60)); title:Mapped[str]=mapped_column(String(240)); category:Mapped[str|None]=mapped_column(String(120)); keywords:Mapped[str|None]=mapped_column(Text); price_packages:Mapped[dict|None]=mapped_column(JSON); portfolio_items:Mapped[list|None]=mapped_column(JSON)
 impressions:Mapped[int]=mapped_column(Integer,default=0); clicks:Mapped[int]=mapped_column(Integer,default=0); inquiries:Mapped[int]=mapped_column(Integer,default=0); orders:Mapped[int]=mapped_column(Integer,default=0); reviews:Mapped[int]=mapped_column(Integer,default=0); last_optimised_at:Mapped[datetime|None]=mapped_column(DateTime(timezone=True)); created_at:Mapped[datetime]=mapped_column(DateTime(timezone=True),default=lambda:datetime.now(timezone.utc)); updated_at:Mapped[datetime]=mapped_column(DateTime(timezone=True),default=lambda:datetime.now(timezone.utc))

class Bid(BaseModel):
 __tablename__="marketing_bids"
 id:Mapped[UUID]=mapped_column(primary_key=True,default=uuid4); organization_id:Mapped[UUID]=mapped_column(ForeignKey("organizations.id",ondelete="CASCADE")); gig_id:Mapped[UUID|None]=mapped_column(ForeignKey("marketing_gigs.id",ondelete="SET NULL")); marketplace:Mapped[str]=mapped_column(String(60),default="Upwork"); job_url:Mapped[str|None]=mapped_column(String(1000)); job_title:Mapped[str|None]=mapped_column(String(240)); bid_amount:Mapped[float|None]=mapped_column(Numeric(14,2)); connects_used:Mapped[int|None]=mapped_column(Integer); status:Mapped[str]=mapped_column(String(30),default="sent"); outcome:Mapped[str|None]=mapped_column(Text); learning_notes:Mapped[str|None]=mapped_column(Text); created_at:Mapped[datetime]=mapped_column(DateTime(timezone=True),default=lambda:datetime.now(timezone.utc)); updated_at:Mapped[datetime]=mapped_column(DateTime(timezone=True),default=lambda:datetime.now(timezone.utc))

class MarketingMetric(BaseModel):
 __tablename__="marketing_metrics"
 id:Mapped[UUID]=mapped_column(primary_key=True,default=uuid4); organization_id:Mapped[UUID]=mapped_column(ForeignKey("organizations.id",ondelete="CASCADE")); channel_id:Mapped[UUID|None]=mapped_column(ForeignKey("marketing_channels.id",ondelete="SET NULL")); campaign_id:Mapped[UUID|None]=mapped_column(ForeignKey("marketing_campaigns.id",ondelete="SET NULL")); period_start:Mapped[date]=mapped_column(Date); followers:Mapped[int|None]=mapped_column(Integer); impressions:Mapped[int|None]=mapped_column(Integer); engagement_rate:Mapped[float|None]=mapped_column(Numeric(8,4)); website_visits:Mapped[int|None]=mapped_column(Integer); leads:Mapped[int|None]=mapped_column(Integer); cost_per_lead:Mapped[float|None]=mapped_column(Numeric(14,2)); conversion_rate:Mapped[float|None]=mapped_column(Numeric(8,4)); revenue:Mapped[float|None]=mapped_column(Numeric(14,2)); created_at:Mapped[datetime]=mapped_column(DateTime(timezone=True),default=lambda:datetime.now(timezone.utc))

class BrandAsset(BaseModel):
 __tablename__="marketing_brand_assets"
 id:Mapped[UUID]=mapped_column(primary_key=True,default=uuid4); organization_id:Mapped[UUID]=mapped_column(ForeignKey("organizations.id",ondelete="CASCADE")); name:Mapped[str]=mapped_column(String(240)); asset_type:Mapped[str]=mapped_column(String(60)); storage_url:Mapped[str|None]=mapped_column(String(1000)); description:Mapped[str|None]=mapped_column(Text); created_by_user_id:Mapped[UUID|None]=mapped_column(ForeignKey("users.id",ondelete="SET NULL")); created_at:Mapped[datetime]=mapped_column(DateTime(timezone=True),default=lambda:datetime.now(timezone.utc)); updated_at:Mapped[datetime]=mapped_column(DateTime(timezone=True),default=lambda:datetime.now(timezone.utc))


class Outreach(BaseModel):
 __tablename__="marketing_outreach"
 id:Mapped[UUID]=mapped_column(primary_key=True,default=uuid4)
 organization_id:Mapped[UUID]=mapped_column(ForeignKey("organizations.id",ondelete="CASCADE"))
 lead_id:Mapped[UUID|None]=mapped_column(ForeignKey("leads.id",ondelete="SET NULL"))
 campaign_id:Mapped[UUID|None]=mapped_column(ForeignKey("marketing_campaigns.id",ondelete="SET NULL"))
 owner_user_id:Mapped[UUID|None]=mapped_column(ForeignKey("users.id",ondelete="SET NULL"))
 contact_name:Mapped[str]=mapped_column(String(200))
 company:Mapped[str|None]=mapped_column(String(240))
 contact_method:Mapped[str]=mapped_column(String(30),default="email")
 target:Mapped[str|None]=mapped_column(String(500))
 status:Mapped[str]=mapped_column(String(30),default="planned")
 last_contacted_at:Mapped[datetime|None]=mapped_column(DateTime(timezone=True))
 next_follow_up_at:Mapped[datetime|None]=mapped_column(DateTime(timezone=True))
 notes:Mapped[str|None]=mapped_column(Text)
 created_at:Mapped[datetime]=mapped_column(DateTime(timezone=True),default=lambda:datetime.now(timezone.utc))
 updated_at:Mapped[datetime]=mapped_column(DateTime(timezone=True),default=lambda:datetime.now(timezone.utc))
