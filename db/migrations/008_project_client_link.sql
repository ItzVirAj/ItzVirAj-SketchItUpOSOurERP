ALTER TABLE projects ADD COLUMN client_id uuid REFERENCES clients(id) ON DELETE SET NULL;
CREATE INDEX idx_projects_org_client ON projects(organization_id,client_id);