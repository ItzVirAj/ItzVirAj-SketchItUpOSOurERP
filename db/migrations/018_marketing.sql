CREATE TABLE marketing_channels (
 id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
 organization_id uuid NOT NULL REFERENCES organizations(id) ON DELETE CASCADE,
 name varchar(120) NOT NULL,
 platform varchar(60) NOT NULL,
 profile_url varchar(500),
 owner_user_id uuid REFERENCES users(id) ON DELETE SET NULL,
 status varchar(30) NOT NULL DEFAULT 'active',
 goals text,
 credentials_pointer varchar(500),
 created_at timestamptz NOT NULL DEFAULT now(),
 updated_at timestamptz NOT NULL DEFAULT now(),
 CONSTRAINT marketing_channels_status_chk CHECK (status IN ('active','paused','archived')),
 CONSTRAINT marketing_channels_org_name_uniq UNIQUE (organization_id,name)
);
CREATE TABLE marketing_campaigns (
 id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
 organization_id uuid NOT NULL REFERENCES organizations(id) ON DELETE CASCADE,
 name varchar(180) NOT NULL,
 objective text,
 audience text,
 budget numeric(14,2),
 starts_at timestamptz,
 ends_at timestamptz,
 utm_parameters jsonb,
 owner_user_id uuid REFERENCES users(id) ON DELETE SET NULL,
 created_at timestamptz NOT NULL DEFAULT now(),
 updated_at timestamptz NOT NULL DEFAULT now()
);
CREATE TABLE marketing_campaign_channels (
 campaign_id uuid NOT NULL REFERENCES marketing_campaigns(id) ON DELETE CASCADE,
 channel_id uuid NOT NULL REFERENCES marketing_channels(id) ON DELETE CASCADE,
 PRIMARY KEY (campaign_id,channel_id)
);
CREATE TABLE marketing_content_items (
 id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
 organization_id uuid NOT NULL REFERENCES organizations(id) ON DELETE CASCADE,
 campaign_id uuid REFERENCES marketing_campaigns(id) ON DELETE SET NULL,
 channel_id uuid REFERENCES marketing_channels(id) ON DELETE SET NULL,
 title varchar(240) NOT NULL,
 idea text,
 format varchar(40) NOT NULL DEFAULT 'post',
 owner_user_id uuid REFERENCES users(id) ON DELETE SET NULL,
 approval_status varchar(30) NOT NULL DEFAULT 'idea',
 publish_at timestamptz,
 asset_links jsonb,
 caption text,
 hashtags text,
 created_at timestamptz NOT NULL DEFAULT now(),
 updated_at timestamptz NOT NULL DEFAULT now(),
 CONSTRAINT marketing_content_format_chk CHECK (format IN ('post','carousel','video','article')),
 CONSTRAINT marketing_content_status_chk CHECK (approval_status IN ('idea','draft','design','review','approved','scheduled','published','repurposed'))
);
CREATE TABLE marketing_gigs (
 id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
 organization_id uuid NOT NULL REFERENCES organizations(id) ON DELETE CASCADE,
 marketplace varchar(60) NOT NULL,
 title varchar(240) NOT NULL,
 category varchar(120),
 keywords text,
 price_packages jsonb,
 portfolio_items jsonb,
 impressions integer NOT NULL DEFAULT 0,
 clicks integer NOT NULL DEFAULT 0,
 inquiries integer NOT NULL DEFAULT 0,
 orders integer NOT NULL DEFAULT 0,
 reviews integer NOT NULL DEFAULT 0,
 last_optimised_at timestamptz,
 created_at timestamptz NOT NULL DEFAULT now(),
 updated_at timestamptz NOT NULL DEFAULT now()
);
CREATE TABLE marketing_bids (
 id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
 organization_id uuid NOT NULL REFERENCES organizations(id) ON DELETE CASCADE,
 gig_id uuid REFERENCES marketing_gigs(id) ON DELETE SET NULL,
 marketplace varchar(60) NOT NULL DEFAULT 'Upwork',
 job_url varchar(1000),
 job_title varchar(240),
 bid_amount numeric(14,2),
 connects_used integer,
 status varchar(30) NOT NULL DEFAULT 'sent',
 outcome text,
 learning_notes text,
 created_at timestamptz NOT NULL DEFAULT now(),
 updated_at timestamptz NOT NULL DEFAULT now(),
 CONSTRAINT marketing_bid_status_chk CHECK (status IN ('sent','viewed','interview','hired','declined'))
);
CREATE TABLE marketing_metrics (
 id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
 organization_id uuid NOT NULL REFERENCES organizations(id) ON DELETE CASCADE,
 channel_id uuid REFERENCES marketing_channels(id) ON DELETE SET NULL,
 campaign_id uuid REFERENCES marketing_campaigns(id) ON DELETE SET NULL,
 period_start date NOT NULL,
 followers integer,
 impressions integer,
 engagement_rate numeric(8,4),
 website_visits integer,
 leads integer,
 cost_per_lead numeric(14,2),
 conversion_rate numeric(8,4),
 revenue numeric(14,2),
 created_at timestamptz NOT NULL DEFAULT now(),
 UNIQUE (organization_id,channel_id,campaign_id,period_start)
);
CREATE TABLE marketing_brand_assets (
 id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
 organization_id uuid NOT NULL REFERENCES organizations(id) ON DELETE CASCADE,
 name varchar(240) NOT NULL,
 asset_type varchar(60) NOT NULL,
 storage_url varchar(1000),
 description text,
 created_by_user_id uuid REFERENCES users(id) ON DELETE SET NULL,
 created_at timestamptz NOT NULL DEFAULT now(),
 updated_at timestamptz NOT NULL DEFAULT now()
);
ALTER TABLE leads ADD COLUMN IF NOT EXISTS campaign_id uuid REFERENCES marketing_campaigns(id) ON DELETE SET NULL;
CREATE INDEX idx_mkt_channels_org_status ON marketing_channels(organization_id,status);
CREATE INDEX idx_mkt_campaigns_org_updated ON marketing_campaigns(organization_id,updated_at DESC);
CREATE INDEX idx_mkt_content_org_publish ON marketing_content_items(organization_id,publish_at);
CREATE INDEX idx_mkt_content_campaign ON marketing_content_items(campaign_id);
CREATE INDEX idx_mkt_gigs_org_marketplace ON marketing_gigs(organization_id,marketplace);
CREATE INDEX idx_mkt_bids_org_created ON marketing_bids(organization_id,created_at DESC);
CREATE INDEX idx_mkt_metrics_org_period ON marketing_metrics(organization_id,period_start DESC);
CREATE INDEX idx_mkt_assets_org_created ON marketing_brand_assets(organization_id,created_at DESC);
CREATE INDEX idx_leads_org_campaign ON leads(organization_id,campaign_id);
ALTER TABLE marketing_channels ENABLE ROW LEVEL SECURITY;
ALTER TABLE marketing_campaigns ENABLE ROW LEVEL SECURITY;
ALTER TABLE marketing_campaign_channels ENABLE ROW LEVEL SECURITY;
ALTER TABLE marketing_content_items ENABLE ROW LEVEL SECURITY;
ALTER TABLE marketing_gigs ENABLE ROW LEVEL SECURITY;
ALTER TABLE marketing_bids ENABLE ROW LEVEL SECURITY;
ALTER TABLE marketing_metrics ENABLE ROW LEVEL SECURITY;
ALTER TABLE marketing_brand_assets ENABLE ROW LEVEL SECURITY;
INSERT INTO permissions (id,key,description) VALUES
(gen_random_uuid(),'marketing.read','Read marketing records'),
(gen_random_uuid(),'marketing.create','Create and update marketing records')
ON CONFLICT (key) DO NOTHING;
INSERT INTO role_permissions(role_id,permission_id)
SELECT r.id,p.id FROM roles r CROSS JOIN permissions p
WHERE r.name='founder_owner' AND p.key IN ('marketing.read','marketing.create')
ON CONFLICT DO NOTHING;
