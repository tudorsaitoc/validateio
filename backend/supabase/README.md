# Supabase Migrations

This directory contains SQL migrations for setting up the ValidateIO database schema in Supabase.

## Migration Files

- `20250108_initial_schema.sql` - Initial database schema including:
  - User profiles table (extends Supabase auth.users)
  - Validations table
  - Row Level Security (RLS) policies
  - Database triggers and functions
  - Real-time subscriptions setup

## How to Apply Migrations

1. Go to your [Supabase Dashboard](https://app.supabase.com)
2. Select your project
3. Navigate to the SQL Editor
4. Create a new query
5. Copy and paste the contents of the migration file
6. Click "Run" to execute

## Migration Order

Always apply migrations in chronological order based on their timestamps.

## Creating New Migrations

When creating new migrations:
1. Use the naming format: `YYYYMMDD_description.sql`
2. Include both UP (create) and DOWN (rollback) operations when possible
3. Test migrations in a development environment first
4. Document any breaking changes

## Row Level Security

All tables have RLS enabled by default. Users can only access their own data unless they have superuser privileges.

## Real-time Subscriptions

The validations table is configured for real-time updates. This allows the frontend to receive live updates when validation status changes.