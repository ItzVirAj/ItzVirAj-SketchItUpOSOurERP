INSERT INTO permissions(key,description) VALUES ('dashboard.read','View organization dashboard and KPI summaries') ON CONFLICT (key) DO NOTHING;
INSERT INTO role_permissions(role_id,permission_id)
SELECT r.id,p.id FROM roles r CROSS JOIN permissions p
WHERE r.name='founder_owner' AND p.key='dashboard.read'
ON CONFLICT DO NOTHING;