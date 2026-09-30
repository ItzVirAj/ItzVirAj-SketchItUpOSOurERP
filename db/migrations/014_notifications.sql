-- 014 Notifications foundation
CREATE TABLE IF NOT EXISTS notifications (
 id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
 organization_id uuid NOT NULL REFERENCES organizations(id) ON DELETE CASCADE,
 user_id uuid NOT NULL REFERENCES users(id) ON DELETE CASCADE,
 type varchar(60) NOT NULL,
 title varchar(240) NOT NULL,
 body text,
 entity_type varchar(80),
 entity_id uuid,
 action_url text,
 is_read boolean NOT NULL DEFAULT false,
 read_at timestamptz,
 created_at timestamptz NOT NULL DEFAULT now()
);
CREATE INDEX IF NOT EXISTS idx_notifications_user_unread ON notifications(organization_id,user_id,is_read,created_at DESC);
CREATE INDEX IF NOT EXISTS idx_notifications_user_created ON notifications(organization_id,user_id,created_at DESC);
ALTER TABLE notifications ENABLE ROW LEVEL SECURITY;
INSERT INTO permissions(key,description) VALUES ('notifications.read','Read notifications'),('notifications.create','Create notifications') ON CONFLICT(key) DO NOTHING;
INSERT INTO role_permissions(role_id,permission_id)
SELECT r.id,p.id FROM roles r CROSS JOIN permissions p
WHERE r.name='founder_owner' AND p.key IN ('notifications.read','notifications.create')
ON CONFLICT DO NOTHING;