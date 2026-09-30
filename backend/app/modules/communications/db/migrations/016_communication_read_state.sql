CREATE TABLE communication_channel_read_states (
 channel_id uuid NOT NULL REFERENCES communication_channels(id) ON DELETE CASCADE,
 user_id uuid NOT NULL REFERENCES users(id) ON DELETE CASCADE,
 last_read_at timestamptz NOT NULL DEFAULT now(),
 PRIMARY KEY (channel_id,user_id)
);

CREATE INDEX idx_comm_read_states_user ON communication_channel_read_states(user_id,channel_id);
CREATE INDEX idx_comm_messages_channel_created_sender ON communication_messages(channel_id,created_at DESC,sender_user_id);
