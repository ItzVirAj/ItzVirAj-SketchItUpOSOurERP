CREATE TABLE events(
 id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
 organization_id uuid NOT NULL REFERENCES organizations(id),
 project_id uuid REFERENCES projects(id) ON DELETE SET NULL,
 created_by_user_id uuid NOT NULL REFERENCES users(id),
 title text NOT NULL,
 description text,
 event_type text NOT NULL DEFAULT 'meeting',
 starts_at timestamptz NOT NULL,
 ends_at timestamptz NOT NULL,
 location text,
 is_all_day boolean NOT NULL DEFAULT false,
 created_at timestamptz NOT NULL DEFAULT now(),
 updated_at timestamptz NOT NULL DEFAULT now(),
 CONSTRAINT events_time_order CHECK (ends_at > starts_at)
);

CREATE INDEX idx_events_org_start ON events(organization_id,starts_at);
CREATE INDEX idx_events_project_start ON events(project_id,starts_at);

ALTER TABLE events ENABLE ROW LEVEL SECURITY;

INSERT INTO permissions(key,description) VALUES
 ('calendar.read','View calendar events'),
 ('calendar.create','Create, update, and delete calendar events')
ON CONFLICT (key) DO NOTHING;

INSERT INTO role_permissions(role_id,permission_id)
SELECT r.id,p.id
FROM roles r CROSS JOIN permissions p
WHERE r.name='founder_owner'
  AND p.key IN ('calendar.read','calendar.create')
ON CONFLICT DO NOTHING;
