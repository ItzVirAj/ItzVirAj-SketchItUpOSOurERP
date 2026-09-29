CREATE TABLE proposals(
 id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
 organization_id uuid NOT NULL REFERENCES organizations(id),
 lead_id uuid REFERENCES leads(id) ON DELETE SET NULL,
 client_id uuid REFERENCES clients(id) ON DELETE SET NULL,
 project_id uuid REFERENCES projects(id) ON DELETE SET NULL,
 title text NOT NULL,
 status text NOT NULL DEFAULT 'draft',
 amount numeric(14,2),
 currency varchar(3) NOT NULL DEFAULT 'INR',
 valid_until timestamptz,
 terms text,
 notes text,
 created_by_user_id uuid NOT NULL REFERENCES users(id),
 created_at timestamptz NOT NULL DEFAULT now(),
 updated_at timestamptz NOT NULL DEFAULT now()
);

CREATE TABLE contracts(
 id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
 organization_id uuid NOT NULL REFERENCES organizations(id),
 proposal_id uuid REFERENCES proposals(id) ON DELETE SET NULL,
 lead_id uuid REFERENCES leads(id) ON DELETE SET NULL,
 client_id uuid NOT NULL REFERENCES clients(id),
 project_id uuid REFERENCES projects(id) ON DELETE SET NULL,
 title text NOT NULL,
 status text NOT NULL DEFAULT 'draft',
 contract_number varchar(80),
 signed_at timestamptz,
 start_date timestamptz,
 end_date timestamptz,
 value numeric(14,2),
 currency varchar(3) NOT NULL DEFAULT 'INR',
 terms text,
 created_by_user_id uuid NOT NULL REFERENCES users(id),
 created_at timestamptz NOT NULL DEFAULT now(),
 updated_at timestamptz NOT NULL DEFAULT now()
);

CREATE INDEX idx_proposals_org_updated ON proposals(organization_id,updated_at DESC);
CREATE INDEX idx_proposals_lead ON proposals(lead_id);
CREATE INDEX idx_proposals_client ON proposals(client_id);
CREATE INDEX idx_contracts_org_updated ON contracts(organization_id,updated_at DESC);
CREATE INDEX idx_contracts_client ON contracts(client_id);
CREATE INDEX idx_contracts_project ON contracts(project_id);

ALTER TABLE proposals ENABLE ROW LEVEL SECURITY;
ALTER TABLE contracts ENABLE ROW LEVEL SECURITY;

INSERT INTO permissions(key,description) VALUES
 ('sales.read','View sales proposals and contracts'),
 ('sales.create','Create and update sales proposals and contracts')
ON CONFLICT (key) DO NOTHING;

INSERT INTO role_permissions(role_id,permission_id)
SELECT r.id,p.id FROM roles r CROSS JOIN permissions p
WHERE r.name='founder_owner' AND p.key IN ('sales.read','sales.create')
ON CONFLICT DO NOTHING;