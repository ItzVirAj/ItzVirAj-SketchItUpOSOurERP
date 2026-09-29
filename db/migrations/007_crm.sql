CREATE TABLE clients(
 id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
 organization_id uuid NOT NULL REFERENCES organizations(id),
 name text NOT NULL,
 industry text,
 website text,
 email text,
 phone text,
 gst_number text,
 notes text,
 status text NOT NULL DEFAULT 'active',
 created_at timestamptz NOT NULL DEFAULT now(),
 updated_at timestamptz NOT NULL DEFAULT now()
);

CREATE TABLE contacts(
 id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
 organization_id uuid NOT NULL REFERENCES organizations(id),
 client_id uuid NOT NULL REFERENCES clients(id) ON DELETE CASCADE,
 name text NOT NULL,
 role text,
 email text,
 phone text,
 communication_preference text,
 birthday timestamptz,
 anniversary timestamptz,
 is_primary boolean NOT NULL DEFAULT false,
 created_at timestamptz NOT NULL DEFAULT now(),
 updated_at timestamptz NOT NULL DEFAULT now()
);

CREATE TABLE crm_pipelines(
 id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
 organization_id uuid NOT NULL REFERENCES organizations(id),
 name text NOT NULL,
 description text,
 is_active boolean NOT NULL DEFAULT true
);

CREATE TABLE crm_pipeline_stages(
 id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
 organization_id uuid NOT NULL REFERENCES organizations(id),
 pipeline_id uuid NOT NULL REFERENCES crm_pipelines(id) ON DELETE CASCADE,
 name text NOT NULL,
 position integer NOT NULL,
 probability numeric(5,2) NOT NULL DEFAULT 0,
 is_closed_won boolean NOT NULL DEFAULT false,
 is_closed_lost boolean NOT NULL DEFAULT false
);

CREATE TABLE leads(
 id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
 organization_id uuid NOT NULL REFERENCES organizations(id),
 pipeline_id uuid NOT NULL REFERENCES crm_pipelines(id),
 stage_id uuid NOT NULL REFERENCES crm_pipeline_stages(id),
 client_id uuid REFERENCES clients(id) ON DELETE SET NULL,
 contact_id uuid REFERENCES contacts(id) ON DELETE SET NULL,
 name text NOT NULL,
 company text,
 industry text,
 phone text,
 email text,
 source text NOT NULL,
 campaign text,
 estimated_value numeric(14,2),
 expected_close_date timestamptz,
 requirement_summary text,
 owner_user_id uuid REFERENCES users(id),
 temperature text NOT NULL DEFAULT 'Cold',
 next_follow_up_at timestamptz,
 lost_reason text,
 lost_notes text,
 tags text,
 created_at timestamptz NOT NULL DEFAULT now(),
 updated_at timestamptz NOT NULL DEFAULT now()
);

CREATE TABLE lead_activities(
 id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
 organization_id uuid NOT NULL REFERENCES organizations(id),
 lead_id uuid NOT NULL REFERENCES leads(id) ON DELETE CASCADE,
 actor_user_id uuid NOT NULL REFERENCES users(id),
 activity_type text NOT NULL,
 subject text NOT NULL,
 notes text,
 occurred_at timestamptz NOT NULL DEFAULT now()
);

CREATE TABLE lead_follow_ups(
 id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
 organization_id uuid NOT NULL REFERENCES organizations(id),
 lead_id uuid NOT NULL REFERENCES leads(id) ON DELETE CASCADE,
 assigned_user_id uuid NOT NULL REFERENCES users(id),
 due_at timestamptz NOT NULL,
 action text NOT NULL,
 completed_at timestamptz,
 notes text
);

CREATE INDEX idx_clients_org_name ON clients(organization_id,name);
CREATE INDEX idx_contacts_client_name ON contacts(client_id,name);
CREATE INDEX idx_pipelines_org_active ON crm_pipelines(organization_id,is_active);
CREATE INDEX idx_pipeline_stages_pipeline_position ON crm_pipeline_stages(pipeline_id,position);
CREATE INDEX idx_leads_org_updated ON leads(organization_id,updated_at DESC);
CREATE INDEX idx_leads_org_stage ON leads(organization_id,stage_id);
CREATE INDEX idx_leads_owner_followup ON leads(owner_user_id,next_follow_up_at);
CREATE INDEX idx_lead_activities_lead_time ON lead_activities(lead_id,occurred_at DESC);
CREATE INDEX idx_lead_followups_org_due ON lead_follow_ups(organization_id,due_at);

ALTER TABLE clients ENABLE ROW LEVEL SECURITY;
ALTER TABLE contacts ENABLE ROW LEVEL SECURITY;
ALTER TABLE crm_pipelines ENABLE ROW LEVEL SECURITY;
ALTER TABLE crm_pipeline_stages ENABLE ROW LEVEL SECURITY;
ALTER TABLE leads ENABLE ROW LEVEL SECURITY;
ALTER TABLE lead_activities ENABLE ROW LEVEL SECURITY;
ALTER TABLE lead_follow_ups ENABLE ROW LEVEL SECURITY;

INSERT INTO permissions(key,description) VALUES
 ('crm.read','View CRM clients, contacts, pipelines, and leads'),
 ('crm.create','Create and update CRM clients, contacts, leads, activities, and follow-ups')
ON CONFLICT (key) DO NOTHING;

INSERT INTO role_permissions(role_id,permission_id)
SELECT r.id,p.id
FROM roles r CROSS JOIN permissions p
WHERE r.name='founder_owner'
  AND p.key IN ('crm.read','crm.create')
ON CONFLICT DO NOTHING;
