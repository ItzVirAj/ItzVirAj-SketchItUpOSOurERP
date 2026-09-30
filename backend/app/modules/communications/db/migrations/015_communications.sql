CREATE TABLE communication_channels (
 id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
 organization_id uuid NOT NULL REFERENCES organizations(id) ON DELETE CASCADE,
 name varchar(120) NOT NULL,
 description text,
 channel_type varchar(20) NOT NULL DEFAULT 'public',
 created_by_user_id uuid NOT NULL REFERENCES users(id),
 created_at timestamptz NOT NULL DEFAULT now(),
 updated_at timestamptz NOT NULL DEFAULT now(),
 CONSTRAINT communication_channels_type_chk CHECK (channel_type IN ('public','private')),
 CONSTRAINT communication_channels_org_name_uniq UNIQUE (organization_id,name)
);

CREATE TABLE communication_channel_members (
 channel_id uuid NOT NULL REFERENCES communication_channels(id) ON DELETE CASCADE,
 user_id uuid NOT NULL REFERENCES users(id) ON DELETE CASCADE,
 joined_at timestamptz NOT NULL DEFAULT now(),
 PRIMARY KEY (channel_id,user_id)
);

CREATE TABLE communication_messages (
 id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
 organization_id uuid NOT NULL REFERENCES organizations(id) ON DELETE CASCADE,
 channel_id uuid NOT NULL REFERENCES communication_channels(id) ON DELETE CASCADE,
 sender_user_id uuid NOT NULL REFERENCES users(id),
 body text NOT NULL,
 is_edited boolean NOT NULL DEFAULT false,
 created_at timestamptz NOT NULL DEFAULT now(),
 updated_at timestamptz NOT NULL DEFAULT now()
);

CREATE INDEX idx_comm_channels_org_updated ON communication_channels(organization_id,updated_at DESC);
CREATE INDEX idx_comm_members_user ON communication_channel_members(user_id,channel_id);
CREATE INDEX idx_comm_messages_channel_created ON communication_messages(channel_id,created_at DESC);
CREATE INDEX idx_comm_messages_org_created ON communication_messages(organization_id,created_at DESC);

ALTER TABLE communication_channels ENABLE ROW LEVEL SECURITY;
ALTER TABLE communication_channel_members ENABLE ROW LEVEL SECURITY;
ALTER TABLE communication_messages ENABLE ROW LEVEL SECURITY;

INSERT INTO permissions (id,key,description) VALUES
 (gen_random_uuid(),'communications.read','Read internal communication channels and messages'),
 (gen_random_uuid(),'communications.create','Create channels and send internal messages')
ON CONFLICT (key) DO NOTHING;

INSERT INTO role_permissions(role_id,permission_id)
SELECT r.id,p.id FROM roles r CROSS JOIN permissions p
WHERE r.name='founder_owner' AND p.key IN ('communications.read','communications.create')
ON CONFLICT DO NOTHING;
