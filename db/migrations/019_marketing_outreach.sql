CREATE TABLE marketing_outreach (
 id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
 organization_id uuid NOT NULL REFERENCES organizations(id) ON DELETE CASCADE,
 lead_id uuid REFERENCES leads(id) ON DELETE SET NULL,
 campaign_id uuid REFERENCES marketing_campaigns(id) ON DELETE SET NULL,
 owner_user_id uuid REFERENCES users(id) ON DELETE SET NULL,
 contact_name varchar(200) NOT NULL,
 company varchar(240),
 contact_method varchar(30) NOT NULL DEFAULT 'email',
 target varchar(500),
 status varchar(30) NOT NULL DEFAULT 'planned',
 last_contacted_at timestamptz,
 next_follow_up_at timestamptz,
 notes text,
 created_at timestamptz NOT NULL DEFAULT now(),
 updated_at timestamptz NOT NULL DEFAULT now(),
 CONSTRAINT marketing_outreach_method_chk CHECK (contact_method IN ('email','linkedin','whatsapp','phone','other')),
 CONSTRAINT marketing_outreach_status_chk CHECK (status IN ('planned','contacted','replied','qualified','not_interested','converted','closed'))
);
CREATE INDEX idx_mkt_outreach_org_followup ON marketing_outreach(organization_id,next_follow_up_at);
CREATE INDEX idx_mkt_outreach_org_status ON marketing_outreach(organization_id,status);
CREATE INDEX idx_mkt_outreach_campaign ON marketing_outreach(campaign_id);
CREATE INDEX idx_mkt_outreach_lead ON marketing_outreach(lead_id);
ALTER TABLE marketing_outreach ENABLE ROW LEVEL SECURITY;
