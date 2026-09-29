CREATE TABLE projects(
 id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
 organization_id uuid NOT NULL REFERENCES organizations(id),
 client_name text,
 name text NOT NULL,
 description text,
 status text NOT NULL DEFAULT 'planned',
 owner_user_id uuid REFERENCES users(id),
 start_date timestamptz,
 due_date timestamptz,
 created_at timestamptz NOT NULL DEFAULT now(),
 updated_at timestamptz NOT NULL DEFAULT now()
);
CREATE TABLE tasks(
 id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
 organization_id uuid NOT NULL REFERENCES organizations(id),
 project_id uuid NOT NULL REFERENCES projects(id) ON DELETE CASCADE,
 title text NOT NULL,
 description text,
 status text NOT NULL DEFAULT 'todo',
 priority text NOT NULL DEFAULT 'medium',
 assignee_user_id uuid REFERENCES users(id),
 due_date timestamptz,
 created_at timestamptz NOT NULL DEFAULT now(),
 updated_at timestamptz NOT NULL DEFAULT now()
);
CREATE INDEX idx_projects_org_created ON projects(organization_id,created_at DESC);
CREATE INDEX idx_tasks_project_created ON tasks(project_id,created_at DESC);
CREATE INDEX idx_tasks_org_status ON tasks(organization_id,status);
ALTER TABLE projects ENABLE ROW LEVEL SECURITY;
ALTER TABLE tasks ENABLE ROW LEVEL SECURITY;