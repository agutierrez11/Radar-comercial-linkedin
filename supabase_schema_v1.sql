-- Radar Comercial v1
-- Aplicar mediante una migración controlada.
-- Este esquema es privacy-first: RLS aísla cada bóveda por auth.uid().
-- Para zero-knowledge estricto, cifrar el payload privado antes del INSERT.

create extension if not exists pgcrypto;

create table if not exists public.vaults (
  id uuid primary key default gen_random_uuid(),
  owner_id uuid not null references auth.users(id) on delete cascade,
  display_name text not null default 'Bóveda personal',
  created_at timestamptz not null default now(),
  updated_at timestamptz not null default now(),
  unique (owner_id)
);

create table if not exists public.vault_snapshots (
  id uuid primary key default gen_random_uuid(),
  vault_id uuid not null references public.vaults(id) on delete cascade,
  owner_id uuid not null references auth.users(id) on delete cascade,
  source_filename text not null,
  source_hash text not null,
  captured_at timestamptz,
  processed_at timestamptz,
  status text not null default 'processing'
    check (status in ('processing', 'ready', 'failed', 'archived')),
  created_at timestamptz not null default now(),
  unique (owner_id, source_hash)
);

create table if not exists public.vault_files (
  id uuid primary key default gen_random_uuid(),
  snapshot_id uuid not null references public.vault_snapshots(id) on delete cascade,
  vault_id uuid not null references public.vaults(id) on delete cascade,
  owner_id uuid not null references auth.users(id) on delete cascade,
  kind text not null
    check (kind in ('original_zip', 'connections', 'positions', 'messages', 'profile', 'derived')),
  storage_path text not null,
  encrypted boolean not null default false,
  byte_size bigint,
  sha256 text,
  created_at timestamptz not null default now(),
  unique (owner_id, storage_path)
);

create table if not exists public.company_entities (
  id uuid primary key default gen_random_uuid(),
  owner_id uuid not null references auth.users(id) on delete cascade,
  canonical_name text not null,
  linkedin_url text,
  domain text,
  country text,
  industry text,
  confidence numeric(5,2) not null default 0,
  source text,
  observed_at timestamptz not null default now()
);

create table if not exists public.contact_identities (
  id uuid primary key default gen_random_uuid(),
  owner_id uuid not null references auth.users(id) on delete cascade,
  canonical_linkedin_url text,
  identity_key text not null,
  first_seen_at timestamptz,
  last_seen_at timestamptz,
  created_at timestamptz not null default now(),
  unique (owner_id, identity_key)
);

create table if not exists public.contact_versions (
  id uuid primary key default gen_random_uuid(),
  identity_id uuid not null references public.contact_identities(id) on delete cascade,
  snapshot_id uuid not null references public.vault_snapshots(id) on delete cascade,
  owner_id uuid not null references auth.users(id) on delete cascade,
  company_entity_id uuid references public.company_entities(id) on delete set null,
  name text,
  company_name text,
  position text,
  country text,
  city text,
  connected_on date,
  present_in_snapshot boolean not null default true,
  current_status text not null default 'observed'
    check (current_status in ('observed', 'missing_from_latest_snapshot', 'reactivated', 'deleted_by_owner')),
  source text,
  confidence numeric(5,2) not null default 0,
  encrypted_payload text,
  created_at timestamptz not null default now(),
  unique (owner_id, identity_id, snapshot_id)
);

create table if not exists public.conversation_threads (
  id uuid primary key default gen_random_uuid(),
  owner_id uuid not null references auth.users(id) on delete cascade,
  contact_identity_id uuid references public.contact_identities(id) on delete cascade,
  conversation_key text not null,
  first_message_at timestamptz,
  last_message_at timestamptz,
  message_count integer not null default 0,
  campaign text,
  topic text,
  commercial_direction text
    check (commercial_direction in ('sent', 'received', 'bidirectional', 'unknown')),
  outcome text,
  archived boolean not null default false,
  created_at timestamptz not null default now(),
  unique (owner_id, conversation_key)
);

create table if not exists public.conversation_messages (
  id uuid primary key default gen_random_uuid(),
  owner_id uuid not null references auth.users(id) on delete cascade,
  thread_id uuid not null references public.conversation_threads(id) on delete cascade,
  message_key text not null,
  message_at timestamptz,
  sender_type text not null default 'unknown'
    check (sender_type in ('owner', 'contact', 'unknown')),
  content text,
  encrypted_content text,
  content_hash text,
  first_seen_snapshot_id uuid references public.vault_snapshots(id) on delete set null,
  last_seen_snapshot_id uuid references public.vault_snapshots(id) on delete set null,
  deleted_at timestamptz,
  created_at timestamptz not null default now(),
  unique (owner_id, message_key)
);

create table if not exists public.icp_profiles (
  id uuid primary key default gen_random_uuid(),
  owner_id uuid not null references auth.users(id) on delete cascade,
  name text not null,
  mode text not null default 'manual'
    check (mode in ('professional_context', 'manual', 'historical_campaign')),
  industries jsonb not null default '[]'::jsonb,
  countries jsonb not null default '[]'::jsonb,
  target_titles jsonb not null default '[]'::jsonb,
  keywords jsonb not null default '[]'::jsonb,
  exclusions jsonb not null default '[]'::jsonb,
  weights jsonb not null default '{"industry":30,"title":25,"country":20,"company":15,"relationship":10}'::jsonb,
  created_at timestamptz not null default now(),
  updated_at timestamptz not null default now()
);

create table if not exists public.vault_decisions (
  id uuid primary key default gen_random_uuid(),
  owner_id uuid not null references auth.users(id) on delete cascade,
  entity_type text not null check (entity_type in ('contact', 'conversation', 'message', 'company')),
  entity_id uuid not null,
  decision text not null check (decision in ('keep', 'archive', 'review', 'delete')),
  reason text,
  decided_at timestamptz not null default now()
);

create index if not exists vault_snapshots_owner_idx on public.vault_snapshots(owner_id, created_at desc);
create index if not exists vault_files_owner_idx on public.vault_files(owner_id, kind);
create index if not exists company_entities_owner_idx on public.company_entities(owner_id);
create index if not exists contact_identities_owner_idx on public.contact_identities(owner_id);
create index if not exists contact_versions_owner_idx on public.contact_versions(owner_id, snapshot_id);
create index if not exists conversation_threads_owner_idx on public.conversation_threads(owner_id, last_message_at desc);
create index if not exists conversation_messages_owner_idx on public.conversation_messages(owner_id, message_at desc);
create index if not exists icp_profiles_owner_idx on public.icp_profiles(owner_id);
create index if not exists vault_decisions_owner_idx on public.vault_decisions(owner_id, decided_at desc);

-- No confiar únicamente en filtros del navegador.
-- RLS y grants deben aplicarse a todas las tablas expuestas.

do $$
declare
  table_name text;
begin
  foreach table_name in array array[
    'vaults', 'vault_snapshots', 'vault_files', 'company_entities',
    'contact_identities', 'contact_versions', 'conversation_threads',
    'conversation_messages', 'icp_profiles', 'vault_decisions'
  ] loop
    execute format('alter table public.%I enable row level security', table_name);
    execute format('revoke all on table public.%I from anon', table_name);
    execute format('grant select, insert, update, delete on table public.%I to authenticated', table_name);
  end loop;
end $$;

-- Policies explícitas y separadas por operación.

do $$
declare
  table_name text;
begin
  foreach table_name in array array[
    'vaults', 'vault_snapshots', 'vault_files', 'company_entities',
    'contact_identities', 'contact_versions', 'conversation_threads',
    'conversation_messages', 'icp_profiles', 'vault_decisions'
  ] loop
    execute format('create policy %I on public.%I for select to authenticated using (owner_id = (select auth.uid()))', table_name || '_select_own', table_name);
    execute format('create policy %I on public.%I for insert to authenticated with check (owner_id = (select auth.uid()))', table_name || '_insert_own', table_name);
    execute format('create policy %I on public.%I for update to authenticated using (owner_id = (select auth.uid())) with check (owner_id = (select auth.uid()))', table_name || '_update_own', table_name);
    execute format('create policy %I on public.%I for delete to authenticated using (owner_id = (select auth.uid()))', table_name || '_delete_own', table_name);
  end loop;
exception when duplicate_object then
  null;
end $$;

-- Storage: bucket privado creado en el Dashboard o mediante una migración segura.
-- Las rutas deben seguir: {user_id}/{snapshot_id}/{kind}.zip|csv|json
-- Ejemplo de policies para storage.objects:
--
-- create policy "vault_files_insert_own"
-- on storage.objects for insert to authenticated
-- with check (
--   bucket_id = 'private-vault'
--   and (storage.foldername(name))[1] = (select auth.uid()::text)
-- );
--
-- create policy "vault_files_select_own"
-- on storage.objects for select to authenticated
-- using (
--   bucket_id = 'private-vault'
--   and owner_id = (select auth.uid()::text)
-- );
--
-- create policy "vault_files_delete_own"
-- on storage.objects for delete to authenticated
-- using (
--   bucket_id = 'private-vault'
--   and owner_id = (select auth.uid()::text)
-- );
