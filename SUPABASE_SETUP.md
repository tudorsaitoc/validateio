# Supabase Setup Guide for ValidateIO

This guide will help you set up Supabase for ValidateIO, replacing the local Docker PostgreSQL database and custom JWT authentication with Supabase's managed services.

## Prerequisites

- A Supabase account (sign up at https://supabase.com)
- Node.js and Python installed locally

## Step 1: Create a Supabase Project

1. Go to [Supabase Dashboard](https://app.supabase.com)
2. Click "New Project"
3. Fill in the project details:
   - Project name: `validateio` (or your preferred name)
   - Database password: Choose a strong password (save this!)
   - Region: Choose the closest region to your users
4. Click "Create Project" and wait for it to be ready

## Step 2: Configure Environment Variables

1. Once your project is ready, go to Settings > API
2. Copy the following values:
   - `Project URL` → `SUPABASE_URL`
   - `anon public` key → `SUPABASE_ANON_KEY`
   - `service_role` key → `SUPABASE_SERVICE_KEY` (⚠️ Keep this secret!)

3. Go to Settings > Database
4. Copy the connection string and replace `[YOUR-PASSWORD]` with your database password:
   - Connection string → `DATABASE_URL`

5. Go to Settings > Auth
6. Copy the JWT secret:
   - `JWT Secret` → `SUPABASE_JWT_SECRET`

7. Update your `.env` file with these values:

```env
# Database (Supabase)
DATABASE_URL=postgresql://postgres:[YOUR-PASSWORD]@db.[YOUR-PROJECT-REF].supabase.co:5432/postgres
SUPABASE_URL=https://[YOUR-PROJECT-REF].supabase.co
SUPABASE_ANON_KEY=your_anon_key_here
SUPABASE_SERVICE_KEY=your_service_key_here
SUPABASE_JWT_SECRET=your_jwt_secret_here
USE_SUPABASE_AUTH=true
```

## Step 3: Run Database Migrations

1. Go to your Supabase Dashboard
2. Navigate to SQL Editor
3. Create a new query
4. Copy and paste the contents of `backend/supabase/migrations/20250108_initial_schema.sql`
5. Click "Run" to execute the migration

This will create:
- User profiles table (extends Supabase auth)
- Validations table
- Row Level Security policies
- Real-time subscriptions
- Database triggers and functions

## Step 4: Configure Authentication (Optional)

1. Go to Authentication > Providers in your Supabase Dashboard
2. Enable email authentication (enabled by default)
3. Optional: Configure additional providers (Google, GitHub, etc.)
4. Configure email templates if needed

## Step 5: Update Backend Dependencies

Add the Supabase Python client to your requirements:

```bash
cd backend
pip install supabase
```

Or add to `requirements.txt`:
```
supabase>=2.0.0
```

## Step 6: Test the Connection

Run the backend with Supabase:

```bash
cd backend
python main.py
```

The application should now:
- Connect to your Supabase PostgreSQL database
- Use Supabase authentication instead of custom JWT
- Support real-time updates for validations

## Features Enabled by Supabase

### 1. **Managed PostgreSQL Database**
- No need for local Docker PostgreSQL
- Automatic backups
- Connection pooling
- SSL connections

### 2. **Authentication**
- Replace custom JWT implementation with Supabase Auth
- Built-in user management
- Social login support
- Email verification
- Password reset flows

### 3. **Real-time Subscriptions**
- Live updates when validation status changes
- No need for WebSocket implementation
- Automatic reconnection handling

### 4. **Row Level Security (RLS)**
- Database-level security policies
- Users can only access their own data
- Superuser support for admin access

### 5. **Storage (Future Enhancement)**
- Can be used for storing validation results
- File uploads for business documents
- Image storage for marketing materials

## Troubleshooting

### Connection Issues
- Verify all environment variables are set correctly
- Check if your IP is allowed in Supabase (Settings > Database > Connection Pooling)
- Ensure you're using the correct connection string format

### Authentication Issues
- Verify `SUPABASE_JWT_SECRET` matches your project's JWT secret
- Check if `USE_SUPABASE_AUTH` is set to `true`
- Ensure the anon key and service key are correct

### Migration Issues
- Make sure to run migrations in order
- Check SQL Editor output for any errors
- Verify all extensions are enabled

## Next Steps

1. Update frontend to use Supabase client
2. Implement real-time validation status updates
3. Add social authentication providers
4. Configure email templates for better UX
5. Set up database backups and monitoring

## Security Best Practices

1. **Never expose your service key** - Use it only on the backend
2. **Enable RLS** on all tables (already done in migration)
3. **Use environment variables** - Never commit secrets
4. **Restrict CORS origins** in production
5. **Enable 2FA** on your Supabase account

## Resources

- [Supabase Documentation](https://supabase.com/docs)
- [Supabase Python Client](https://github.com/supabase-community/supabase-py)
- [Row Level Security Guide](https://supabase.com/docs/guides/auth/row-level-security)
- [Real-time Subscriptions](https://supabase.com/docs/guides/realtime)