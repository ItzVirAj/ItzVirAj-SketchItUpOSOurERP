-- 013 Documents foundation
CREATE TABLE IF NOT EXISTS document_folders (
 id uuid PRIMARY KEY DEFAULT gen_random_uuid(), organization_id uuid NOT NULL REFERENCES organizations(id) ON DELETE CASCADE,
 parent_folder_id uuid REFERENCES document_folders(id) ON DELETE CASCADE, name varchar(240) NOT NULL, description text,
 created_by_user_id uuid NOT NULL REFERENCES users(id), created_at timestamptz NOT NULL DEFAULT now(), updated_at timestamptz NOT NULL DEFAULT now()
);
CREATE TABLE IF NOT EXISTS documents (
 id uuid PRIMARY KEY DEFAULT gen_random_uuid(), organization_id uuid NOT NULL REFERENCES organizations(id) ON DELETE CASCADE,
 folder_id uuid REFERENCES document_folders(id) ON DELETE SET NULL, name varchar(240) NOT NULL, description text,
 storage_key text NOT NULL, mime_type varchar(120), size_bytes bigint, checksum varchar(128),
 client_id uuid REFERENCES clients(id) ON DELETE SET NULL, project_id uuid REFERENCES projects(id) ON DELETE SET NULL,
 uploaded_by_user_id uuid NOT NULL REFERENCES users(id), created_at timestamptz NOT NULL DEFAULT now(), updated_at timestamptz NOT NULL DEFAULT now()
);
CREATE TABLE IF NOT EXISTS document_versions (
 id uuid PRIMARY KEY DEFAULT gen_random_uuid(), organization_id uuid NOT NULL REFERENCES organizations(id) ON DELETE CASCADE,
 document_id uuid NOT NULL REFERENCES documents(id) ON DELETE CASCADE, version_number integer NOT NULL,
 storage_key text NOT NULL, mime_type varchar(120), size_bytes bigint, checksum varchar(128),
 uploaded_by_user_id uuid NOT NULL REFERENCES users(id), created_at timestamptz NOT NULL DEFAULT now(),
 UNIQUE(document_id,version_number)
);
CREATE INDEX IF NOT EXISTS idx_document_folders_org_parent ON document_folders(organization_id,parent_folder_id);
CREATE INDEX IF NOT EXISTS idx_documents_org_updated ON documents(organization_id,updated_at DESC);
CREATE INDEX IF NOT EXISTS idx_documents_org_folder ON documents(organization_id,folder_id);
CREATE INDEX IF NOT EXISTS idx_documents_org_client ON documents(organization_id,client_id);
CREATE INDEX IF NOT EXISTS idx_documents_org_project ON documents(organization_id,project_id);
CREATE INDEX IF NOT EXISTS idx_document_versions_document ON document_versions(document_id,version_number DESC);
ALTER TABLE document_folders ENABLE ROW LEVEL SECURITY;
ALTER TABLE documents ENABLE ROW LEVEL SECURITY;
ALTER TABLE document_versions ENABLE ROW LEVEL SECURITY;
INSERT INTO permissions(key,description) VALUES ('documents.read','Read documents'),('documents.create','Create documents') ON CONFLICT(key) DO NOTHING;
INSERT INTO role_permissions(role_id,permission_id) SELECT r.id,p.id FROM roles r CROSS JOIN permissions p WHERE r.name='founder_owner' AND p.key IN ('documents.read','documents.create') ON CONFLICT DO NOTHING;