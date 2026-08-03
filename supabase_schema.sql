-- 1. Crear tabla de contactos (Cada usuario tiene su propio silo de contactos)
CREATE TABLE public.contacts (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    user_id UUID REFERENCES auth.users(id) ON DELETE CASCADE NOT NULL,
    contact_id TEXT NOT NULL, -- URL de LinkedIn o ID único
    first_name TEXT,
    last_name TEXT,
    company TEXT,
    position TEXT,
    connected_on TEXT,
    email_address TEXT,
    profile_url TEXT,
    msg_count INTEGER DEFAULT 0,
    latest_message TEXT,
    -- Campos CRM
    crm_status TEXT DEFAULT 'Ninguno',
    crm_notes TEXT,
    custom_name TEXT,
    custom_company TEXT,
    custom_position TEXT,
    crm_date TEXT,
    -- Extensibilidad
    raw_data JSONB DEFAULT '{}'::jsonb,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT timezone('utc'::text, now()) NOT NULL,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT timezone('utc'::text, now()) NOT NULL,
    UNIQUE(user_id, contact_id) -- Un usuario no puede tener el mismo contacto duplicado
);

-- 2. Habilitar RLS (Row Level Security) para privacidad estricta
ALTER TABLE public.contacts ENABLE ROW LEVEL SECURITY;

-- 3. Crear políticas de seguridad (Zero-Knowledge)
-- El usuario solo puede ver y editar sus propios contactos
CREATE POLICY "Users can view their own contacts" 
ON public.contacts FOR SELECT 
USING (auth.uid() = user_id);

CREATE POLICY "Users can insert their own contacts" 
ON public.contacts FOR INSERT 
WITH CHECK (auth.uid() = user_id);

CREATE POLICY "Users can update their own contacts" 
ON public.contacts FOR UPDATE 
USING (auth.uid() = user_id)
WITH CHECK (auth.uid() = user_id);

CREATE POLICY "Users can delete their own contacts" 
ON public.contacts FOR DELETE 
USING (auth.uid() = user_id);

-- 4. Crear tabla de configuraciones y caché IA del usuario
CREATE TABLE public.user_settings (
    user_id UUID REFERENCES auth.users(id) ON DELETE CASCADE PRIMARY KEY,
    owner_name TEXT,
    positions JSONB DEFAULT '[]'::jsonb,
    ai_provider TEXT DEFAULT 'claude',
    ai_key TEXT, -- Almacenado del lado del servidor de forma más segura
    ai_cache JSONB DEFAULT '{}'::jsonb,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT timezone('utc'::text, now()) NOT NULL,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT timezone('utc'::text, now()) NOT NULL
);

-- 5. Habilitar RLS en configuraciones
ALTER TABLE public.user_settings ENABLE ROW LEVEL SECURITY;

CREATE POLICY "Users can view their own settings" 
ON public.user_settings FOR SELECT 
USING (auth.uid() = user_id);

CREATE POLICY "Users can insert their own settings" 
ON public.user_settings FOR INSERT 
WITH CHECK (auth.uid() = user_id);

CREATE POLICY "Users can update their own settings" 
ON public.user_settings FOR UPDATE 
USING (auth.uid() = user_id)
WITH CHECK (auth.uid() = user_id);

-- 6. Opcional: Función para auto-crear configuraciones al registrarse
CREATE OR REPLACE FUNCTION public.handle_new_user() 
RETURNS trigger AS $$
BEGIN
  INSERT INTO public.user_settings (user_id)
  VALUES (new.id);
  RETURN new;
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;

CREATE TRIGGER on_auth_user_created
  AFTER INSERT ON auth.users
  FOR EACH ROW EXECUTE PROCEDURE public.handle_new_user();
