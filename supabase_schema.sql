-- Habilitar extensión pgvector para embeddings
create extension if not exists vector;

-- Tabla de Comerciales (Sellers)
create table public.sellers (
    id uuid primary key default gen_random_uuid(),
    name text not null,
    email text unique not null,
    created_at timestamp with time zone default timezone('utc'::text, now()) not null
);

-- Tabla de Conexiones de LinkedIn (BYOD)
create table public.connections (
    id uuid primary key default gen_random_uuid(),
    seller_id uuid references public.sellers(id) on delete cascade not null,
    first_name text,
    last_name text,
    current_company text,
    current_position text,
    linkedin_url text,
    normalized_company text, -- Para busqueda exacta sin acentos/mayusculas
    embedding vector(768), -- Asumiendo Gemini embeddings (768 dimensiones).
    created_at timestamp with time zone default timezone('utc'::text, now()) not null
);

-- Index de similitud HNSW para optimizar consultas de vectores
create index on public.connections using hnsw (embedding vector_cosine_ops);

-- Tabla de Cuentas Objetivo (Target Accounts)
create table public.target_accounts (
    id uuid primary key default gen_random_uuid(),
    name text not null,
    domain text,
    industry text,
    created_at timestamp with time zone default timezone('utc'::text, now()) not null
);

-- Tabla de Introducciones y Bounties (Warm Intros)
create table public.warm_intros (
    id uuid primary key default gen_random_uuid(),
    target_account_id uuid references public.target_accounts(id),
    connection_id uuid references public.connections(id) not null,
    requesting_seller_id uuid references public.sellers(id) not null,
    providing_seller_id uuid references public.sellers(id) not null,
    status text check (status in ('requested', 'approved', 'rejected', 'successful')) default 'requested',
    bounty_amount numeric default 150.00,
    created_at timestamp with time zone default timezone('utc'::text, now()) not null,
    updated_at timestamp with time zone default timezone('utc'::text, now()) not null
);

-- RLS: Seguridad a nivel de fila para Connections (Privacidad del vendedor)
alter table public.connections enable row level security;

-- En producción (con Supabase Auth), esto aseguraría que cada quien ve lo suyo
-- create policy "Sellers can manage their own connections" 
-- on public.connections for all using (seller_id = auth.uid());
-- NOTA: Por ahora, dado que interactuaremos desde el Backend con Service Role, 
-- la Service Role Key bypassea RLS automáticamente.

-- RPC Semáforo: Buscar coincidencias por empresa (Zero-Knowledge: sin revelar nombre)
create or replace function get_warm_semaphore(search_company text)
returns table (
    company_matched text,
    contact_count bigint,
    seller_id uuid
) 
language sql
security definer
as $$
    select 
        c.current_company as company_matched,
        count(c.id) as contact_count,
        c.seller_id
    from public.connections c
    where c.normalized_company ilike '%' || search_company || '%'
    group by c.current_company, c.seller_id;
$$;
