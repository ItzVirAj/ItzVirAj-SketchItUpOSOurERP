from datetime import date,datetime
from uuid import UUID
from pydantic import BaseModel,Field

class ChannelCreate(BaseModel):
 name:str=Field(min_length=1,max_length=120); platform:str=Field(min_length=1,max_length=60); profile_url:str|None=None; owner_user_id:UUID|None=None; status:str="active"; goals:str|None=None; credentials_pointer:str|None=None
class ChannelUpdate(BaseModel):
 name:str|None=Field(default=None,min_length=1,max_length=120); platform:str|None=Field(default=None,min_length=1,max_length=60); profile_url:str|None=None; owner_user_id:UUID|None=None; status:str|None=None; goals:str|None=None; credentials_pointer:str|None=None
class ChannelRead(ChannelCreate):
 id:UUID; organization_id:UUID; created_at:datetime; updated_at:datetime

class CampaignCreate(BaseModel):
 name:str=Field(min_length=1,max_length=180); objective:str|None=None; audience:str|None=None; budget:float|None=None; starts_at:datetime|None=None; ends_at:datetime|None=None; utm_parameters:dict|None=None; owner_user_id:UUID|None=None
class CampaignUpdate(BaseModel):
 name:str|None=Field(default=None,min_length=1,max_length=180); objective:str|None=None; audience:str|None=None; budget:float|None=None; starts_at:datetime|None=None; ends_at:datetime|None=None; utm_parameters:dict|None=None; owner_user_id:UUID|None=None
class CampaignRead(CampaignCreate):
 id:UUID; organization_id:UUID; created_at:datetime; updated_at:datetime
class CampaignChannelAdd(BaseModel):
 channel_id:UUID

class ContentCreate(BaseModel):
 title:str=Field(min_length=1,max_length=240); idea:str|None=None; campaign_id:UUID|None=None; channel_id:UUID|None=None; format:str="post"; owner_user_id:UUID|None=None; approval_status:str="idea"; publish_at:datetime|None=None; asset_links:list|None=None; caption:str|None=None; hashtags:str|None=None
class ContentUpdate(BaseModel):
 title:str|None=Field(default=None,min_length=1,max_length=240); idea:str|None=None; campaign_id:UUID|None=None; channel_id:UUID|None=None; format:str|None=None; owner_user_id:UUID|None=None; approval_status:str|None=None; publish_at:datetime|None=None; asset_links:list|None=None; caption:str|None=None; hashtags:str|None=None
class ContentRead(ContentCreate):
 id:UUID; organization_id:UUID; created_at:datetime; updated_at:datetime

class GigCreate(BaseModel):
 marketplace:str=Field(min_length=1,max_length=60); title:str=Field(min_length=1,max_length=240); category:str|None=None; keywords:str|None=None; price_packages:dict|None=None; portfolio_items:list|None=None; impressions:int=0; clicks:int=0; inquiries:int=0; orders:int=0; reviews:int=0; last_optimised_at:datetime|None=None
class GigUpdate(BaseModel):
 marketplace:str|None=None; title:str|None=None; category:str|None=None; keywords:str|None=None; price_packages:dict|None=None; portfolio_items:list|None=None; impressions:int|None=None; clicks:int|None=None; inquiries:int|None=None; orders:int|None=None; reviews:int|None=None; last_optimised_at:datetime|None=None
class GigRead(GigCreate):
 id:UUID; organization_id:UUID; created_at:datetime; updated_at:datetime

class BidCreate(BaseModel):
 gig_id:UUID|None=None; marketplace:str="Upwork"; job_url:str|None=None; job_title:str|None=None; bid_amount:float|None=None; connects_used:int|None=None; status:str="sent"; outcome:str|None=None; learning_notes:str|None=None
class BidUpdate(BaseModel):
 gig_id:UUID|None=None; marketplace:str|None=None; job_url:str|None=None; job_title:str|None=None; bid_amount:float|None=None; connects_used:int|None=None; status:str|None=None; outcome:str|None=None; learning_notes:str|None=None
class BidRead(BidCreate):
 id:UUID; organization_id:UUID; created_at:datetime; updated_at:datetime

class MetricCreate(BaseModel):
 channel_id:UUID|None=None; campaign_id:UUID|None=None; period_start:date; followers:int|None=None; impressions:int|None=None; engagement_rate:float|None=None; website_visits:int|None=None; leads:int|None=None; cost_per_lead:float|None=None; conversion_rate:float|None=None; revenue:float|None=None
class MetricUpdate(BaseModel):
 channel_id:UUID|None=None; campaign_id:UUID|None=None; period_start:date|None=None; followers:int|None=None; impressions:int|None=None; engagement_rate:float|None=None; website_visits:int|None=None; leads:int|None=None; cost_per_lead:float|None=None; conversion_rate:float|None=None; revenue:float|None=None
class MetricRead(MetricCreate):
 id:UUID; organization_id:UUID; created_at:datetime

class BrandAssetCreate(BaseModel):
 name:str=Field(min_length=1,max_length=240); asset_type:str=Field(min_length=1,max_length=60); storage_url:str|None=None; description:str|None=None
class BrandAssetRead(BrandAssetCreate):
 id:UUID; organization_id:UUID; created_by_user_id:UUID|None; created_at:datetime; updated_at:datetime

class AttributionRead(BaseModel):
 campaign_id:UUID; campaign_name:str; leads:int; won_leads:int; estimated_won_value:float; collected_revenue:float

class ImportRowResult(BaseModel):
 row:int; status:str; record_id:UUID|None=None; error:str|None=None
class ImportResult(BaseModel):
 import_type:str; total_rows:int; created:int; updated:int; failed:int; rows:list[ImportRowResult]


class OutreachCreate(BaseModel):
 lead_id:UUID|None=None; campaign_id:UUID|None=None; owner_user_id:UUID|None=None
 contact_name:str=Field(min_length=1,max_length=200); company:str|None=None
 contact_method:str="email"; target:str|None=None; status:str="planned"
 last_contacted_at:datetime|None=None; next_follow_up_at:datetime|None=None; notes:str|None=None

class OutreachUpdate(BaseModel):
 lead_id:UUID|None=None; campaign_id:UUID|None=None; owner_user_id:UUID|None=None
 contact_name:str|None=Field(default=None,min_length=1,max_length=200); company:str|None=None
 contact_method:str|None=None; target:str|None=None; status:str|None=None
 last_contacted_at:datetime|None=None; next_follow_up_at:datetime|None=None; notes:str|None=None

class OutreachRead(OutreachCreate):
 id:UUID; organization_id:UUID; created_at:datetime; updated_at:datetime

class MarketingKPIRead(BaseModel):
 period_start:date; period_end:date
 impressions:int; website_visits:int; leads:int; won_leads:int
 estimated_won_value:float; collected_revenue:float
 content_published:int; active_campaigns:int
 gigs:int; bids:int; interviews:int; hires:int
 outreach_total:int; outreach_due:int; outreach_overdue:int

class MarketingKPIDashboardRead(BaseModel):
 current:MarketingKPIRead
 previous:MarketingKPIRead
