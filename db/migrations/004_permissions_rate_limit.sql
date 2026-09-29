CREATE TABLE permissions(
 id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
 key text NOT NULL UNIQUE,
 description text
);
CREATE TABLE role_permissions(
 role_id uuid NOT NULL REFERENCES roles(id) ON DELETE CASCADE,
 permission_id uuid NOT NULL REFERENCES permissions(id) ON DELETE CASCADE,
 PRIMARY KEY(role_id,permission_id)
);
CREATE TABLE login_attempts(
 id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
 identifier text NOT NULL,
 attempted_at timestamptz NOT NULL DEFAULT now(),
 success boolean NOT NULL DEFAULT false
);
CREATE INDEX idx_role_permissions_permission ON role_permissions(permission_id);
CREATE INDEX idx_login_attempts_identifier_time ON login_attempts(identifier,attempted_at DESC);
ALTER TABLE permissions ENABLE ROW LEVEL SECURITY;
ALTER TABLE role_permissions ENABLE ROW LEVEL SECURITY;
ALTER TABLE login_attempts ENABLE ROW LEVEL SECURITY;
INSERT INTO roles(name,description) VALUES
 ('founder_owner','Founder / Owner'),('admin_operations','Admin / Operations'),('project_manager','Project Manager / Tech Lead'),('developer','Developer'),('designer_qa','Designer / QA'),('business_development','Business Development / Sales'),('marketing_executive','Marketing Executive'),('finance_accounts','Finance / Accounts'),('freelancer_contractor','Freelancer / Contractor'),('client','Client portal user')
ON CONFLICT(name) DO NOTHING;
INSERT INTO permissions(key,description) VALUES
 ('users.read','View organization users'),('users.create','Create organization users'),('roles.read','View roles and permissions'),('audit.read','View organization audit logs'),('projects.read','View projects'),('projects.create','Create projects'),('tasks.read','View tasks'),('tasks.create','Create tasks'),('crm.read','View CRM records'),('crm.create','Create CRM records'),('finance.read','View finance records'),('finance.create','Create finance records')
ON CONFLICT(key) DO NOTHING;
INSERT INTO role_permissions(role_id,permission_id)
SELECT r.id,p.id FROM roles r CROSS JOIN permissions p
WHERE r.name='founder_owner'
ON CONFLICT DO NOTHING;