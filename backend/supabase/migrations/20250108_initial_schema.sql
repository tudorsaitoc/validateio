-- ValidateIO Initial Schema for Supabase
-- This migration sets up the database schema for ValidateIO

-- Enable required extensions
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "pgcrypto";

-- Create enum types
CREATE TYPE validation_status AS ENUM ('PENDING', 'PROCESSING', 'COMPLETED', 'FAILED', 'CANCELLED');

-- Create users table (extends Supabase auth.users)
-- This table stores additional user profile information
CREATE TABLE IF NOT EXISTS public.user_profiles (
    id UUID PRIMARY KEY REFERENCES auth.users(id) ON DELETE CASCADE,
    username VARCHAR(255) UNIQUE NOT NULL,
    full_name VARCHAR(255),
    is_active BOOLEAN NOT NULL DEFAULT true,
    is_superuser BOOLEAN NOT NULL DEFAULT false,
    is_verified BOOLEAN NOT NULL DEFAULT false,
    created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW()
);

-- Create validations table
CREATE TABLE IF NOT EXISTS public.validations (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID NOT NULL REFERENCES auth.users(id) ON DELETE CASCADE,
    business_idea TEXT NOT NULL,
    target_market VARCHAR(255),
    industry VARCHAR(255),
    status validation_status NOT NULL DEFAULT 'PENDING',
    task_id VARCHAR(255),
    market_research JSONB,
    experiments JSONB,
    marketing_campaigns JSONB,
    total_cost DECIMAL(10, 2),
    execution_time_seconds DECIMAL(10, 2),
    completed_at TIMESTAMP WITH TIME ZONE,
    created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW()
);

-- Create indexes
CREATE INDEX idx_validations_user_id ON public.validations(user_id);
CREATE INDEX idx_validations_status ON public.validations(status);
CREATE INDEX idx_validations_created_at ON public.validations(created_at DESC);

-- Create function to update updated_at timestamp
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ language 'plpgsql';

-- Create triggers for updated_at
CREATE TRIGGER update_user_profiles_updated_at BEFORE UPDATE ON public.user_profiles
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_validations_updated_at BEFORE UPDATE ON public.validations
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- Create function to handle new user signups
-- This automatically creates a user profile when a new user signs up
CREATE OR REPLACE FUNCTION handle_new_user()
RETURNS TRIGGER AS $$
BEGIN
    INSERT INTO public.user_profiles (id, username, full_name, created_at, updated_at)
    VALUES (
        NEW.id,
        COALESCE(NEW.raw_user_meta_data->>'username', split_part(NEW.email, '@', 1)),
        NEW.raw_user_meta_data->>'full_name',
        NOW(),
        NOW()
    );
    RETURN NEW;
END;
$$ language 'plpgsql';

-- Create trigger for new user signups
CREATE TRIGGER on_auth_user_created
    AFTER INSERT ON auth.users
    FOR EACH ROW EXECUTE FUNCTION handle_new_user();

-- Row Level Security (RLS) Policies

-- Enable RLS on tables
ALTER TABLE public.user_profiles ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.validations ENABLE ROW LEVEL SECURITY;

-- User profiles policies
-- Users can view their own profile
CREATE POLICY "Users can view own profile" ON public.user_profiles
    FOR SELECT USING (auth.uid() = id);

-- Users can update their own profile
CREATE POLICY "Users can update own profile" ON public.user_profiles
    FOR UPDATE USING (auth.uid() = id);

-- Superusers can view all profiles
CREATE POLICY "Superusers can view all profiles" ON public.user_profiles
    FOR SELECT USING (
        EXISTS (
            SELECT 1 FROM public.user_profiles
            WHERE id = auth.uid() AND is_superuser = true
        )
    );

-- Validations policies
-- Users can view their own validations
CREATE POLICY "Users can view own validations" ON public.validations
    FOR SELECT USING (auth.uid() = user_id);

-- Users can create their own validations
CREATE POLICY "Users can create own validations" ON public.validations
    FOR INSERT WITH CHECK (auth.uid() = user_id);

-- Users can update their own validations
CREATE POLICY "Users can update own validations" ON public.validations
    FOR UPDATE USING (auth.uid() = user_id);

-- Users can delete their own validations
CREATE POLICY "Users can delete own validations" ON public.validations
    FOR DELETE USING (auth.uid() = user_id);

-- Superusers can view all validations
CREATE POLICY "Superusers can view all validations" ON public.validations
    FOR SELECT USING (
        EXISTS (
            SELECT 1 FROM public.user_profiles
            WHERE id = auth.uid() AND is_superuser = true
        )
    );

-- Create realtime subscriptions for validations
-- This enables real-time updates for validation status changes
ALTER PUBLICATION supabase_realtime ADD TABLE public.validations;

-- Grant necessary permissions
GRANT USAGE ON SCHEMA public TO anon, authenticated;
GRANT ALL ON public.user_profiles TO anon, authenticated;
GRANT ALL ON public.validations TO anon, authenticated;
GRANT USAGE ON SEQUENCE public.validations_id_seq TO anon, authenticated;

-- Create views for easier querying
CREATE OR REPLACE VIEW public.validation_summaries AS
SELECT 
    v.id,
    v.user_id,
    v.business_idea,
    v.target_market,
    v.industry,
    v.status,
    v.total_cost,
    v.execution_time_seconds,
    v.created_at,
    v.updated_at,
    v.completed_at,
    up.username,
    up.full_name AS user_full_name
FROM public.validations v
JOIN public.user_profiles up ON v.user_id = up.id;

-- Grant permissions on view
GRANT SELECT ON public.validation_summaries TO anon, authenticated;

-- Add RLS policy for view
CREATE POLICY "Users can view own validation summaries" ON public.validations
    FOR SELECT USING (
        auth.uid() = user_id OR
        EXISTS (
            SELECT 1 FROM public.user_profiles
            WHERE id = auth.uid() AND is_superuser = true
        )
    );