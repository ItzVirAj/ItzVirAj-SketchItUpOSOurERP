ALTER TABLE communication_channels ADD COLUMN archived_at timestamptz;

CREATE INDEX idx_comm_channels_org_archived_updated
ON communication_channels(organization_id, archived_at, updated_at DESC);
