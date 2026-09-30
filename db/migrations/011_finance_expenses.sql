CREATE TABLE expenses(
 id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
 organization_id uuid NOT NULL REFERENCES organizations(id),
 project_id uuid REFERENCES projects(id) ON DELETE SET NULL,
 category varchar(80) NOT NULL,
 description text NOT NULL,
 amount numeric(14,2) NOT NULL CHECK(amount>0),
 currency varchar(3) NOT NULL DEFAULT 'INR',
 incurred_at timestamptz NOT NULL,
 status varchar(30) NOT NULL DEFAULT 'recorded',
 created_by_user_id uuid NOT NULL REFERENCES users(id),
 created_at timestamptz NOT NULL DEFAULT now()
);
CREATE INDEX idx_expenses_org_date ON expenses(organization_id,incurred_at DESC);
CREATE INDEX idx_expenses_project_date ON expenses(project_id,incurred_at DESC);
ALTER TABLE expenses ENABLE ROW LEVEL SECURITY;
INSERT INTO permissions(key,description) VALUES
 ('finance.expenses.read','View expenses'),
 ('finance.expenses.create','Create expenses')
ON CONFLICT (key) DO NOTHING;
INSERT INTO role_permissions(role_id,permission_id)
SELECT r.id,p.id FROM roles r CROSS JOIN permissions p
WHERE r.name='founder_owner' AND p.key IN ('finance.expenses.read','finance.expenses.create')
ON CONFLICT DO NOTHING;