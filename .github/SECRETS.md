# GitHub Secrets Configuration

This document lists all the GitHub secrets required for the CI/CD pipelines to work correctly.

## Required Secrets

### Google Cloud Platform (Backend Deployment)

- **`GCP_PROJECT_ID`**: Your Google Cloud Project ID
  - Example: `validateio-prod-123456`
  
- **`GCP_REGION`**: The GCP region for Cloud Run deployment
  - Example: `us-central1`
  
- **`GCP_SA_KEY`**: Service Account JSON key with permissions for:
  - Cloud Run Admin
  - Artifact Registry Writer
  - Storage Admin
  - To create: Go to GCP Console → IAM & Admin → Service Accounts → Create Service Account → Add roles → Create Key (JSON)

### Vercel (Frontend Deployment)

- **`VERCEL_TOKEN`**: Your Vercel API token
  - Get it from: https://vercel.com/account/tokens
  
- **`VERCEL_ORG_ID`**: Your Vercel organization ID
  - Find in: https://vercel.com/account
  
- **`VERCEL_PROJECT_ID`**: Your Vercel project ID
  - Find in: Project Settings → General

### Database

- **`DATABASE_URL`**: PostgreSQL connection string for production
  - Format: `postgresql://[user]:[password]@[host]:[port]/[database]?sslmode=require`
  
- **`SUPABASE_URL`**: Your Supabase project URL
  - Example: `https://xyzxyzxyz.supabase.co`
  
- **`SUPABASE_ANON_KEY`**: Supabase anonymous/public key
  - Find in: Supabase Dashboard → Settings → API

### API Keys

- **`OPENAI_API_KEY`**: OpenAI API key for GPT models
  - Get from: https://platform.openai.com/api-keys
  
- **`ANTHROPIC_API_KEY`**: Anthropic API key for Claude models
  - Get from: https://console.anthropic.com/account/keys
  
- **`RESEND_API_KEY`**: Resend API key for email services
  - Get from: https://resend.com/api-keys

### Application Configuration

- **`JWT_SECRET_KEY`**: Secret key for JWT token signing
  - Generate with: `openssl rand -hex 32`
  
- **`REDIS_URL`**: Redis connection URL for caching/queues
  - Format: `redis://:[password]@[host]:[port]/[db]`

### Frontend Environment

- **`NEXT_PUBLIC_API_URL`**: Backend API URL for frontend
  - Example: `https://validateio-backend-xyzxyz.a.run.app`

### Monitoring (Optional)

- **`SENTRY_DSN`**: Sentry DSN for error tracking
  - Get from: Sentry Project → Settings → Client Keys
  
- **`SLACK_WEBHOOK_URL`**: Slack webhook for deployment notifications
  - Create at: https://api.slack.com/apps → Incoming Webhooks

### Staging Environment

- **`STAGING_DATABASE_URL`**: PostgreSQL connection string for staging
  - Format: Same as DATABASE_URL but for staging database
  
- **`STAGING_SUPABASE_URL`**: Staging Supabase project URL
  
- **`STAGING_SUPABASE_ANON_KEY`**: Staging Supabase anonymous key
  
- **`STAGING_REDIS_URL`**: Redis connection URL for staging
  
- **`STAGING_API_URL`**: Backend API URL for staging frontend
  - Example: `https://validateio-backend-staging-xyzxyz.a.run.app`
  
- **`STAGING_URL`**: Frontend staging URL for E2E tests
  - Example: `https://validateio-staging.vercel.app`

### Testing

- **`TEST_USER_EMAIL`**: Email for E2E test user
  
- **`TEST_USER_PASSWORD`**: Password for E2E test user

### Maintenance

- **`MAINTENANCE_API_KEY`**: API key for maintenance endpoints
  - Generate with: `openssl rand -hex 32`
  
- **`SUPABASE_SERVICE_KEY`**: Supabase service role key (for backups)
  - Find in: Supabase Dashboard → Settings → API → Service Role Key

## Setting Secrets

### Via GitHub UI

1. Go to your repository on GitHub
2. Click on **Settings** → **Secrets and variables** → **Actions**
3. Click **New repository secret**
4. Add each secret with its name and value

### Via GitHub CLI

```bash
# Install GitHub CLI if not already installed
# brew install gh (macOS)
# or visit: https://cli.github.com/

# Authenticate
gh auth login

# Set secrets
gh secret set GCP_PROJECT_ID --body "your-project-id"
gh secret set GCP_REGION --body "us-central1"
gh secret set GCP_SA_KEY < path/to/service-account-key.json
gh secret set DATABASE_URL --body "postgresql://..."
# ... repeat for all secrets
```

## Security Best Practices

1. **Rotate secrets regularly** - At least every 90 days
2. **Use least privilege** - Grant only necessary permissions
3. **Separate environments** - Use different secrets for dev/staging/prod
4. **Audit access** - Regularly review who has access to secrets
5. **Never commit secrets** - Always use GitHub Secrets, never hardcode

## Troubleshooting

### Common Issues

1. **"Unauthorized" errors in GCP deployment**
   - Check that GCP_SA_KEY has all required permissions
   - Verify the service account is active

2. **"Invalid token" errors in Vercel deployment**
   - Regenerate your Vercel token
   - Ensure the token has deployment permissions

3. **Database connection failures**
   - Verify DATABASE_URL includes SSL parameters
   - Check IP allowlisting in database settings

4. **Missing environment variables in deployed app**
   - Ensure all NEXT_PUBLIC_* vars are set during build
   - Check Cloud Run service configuration for backend vars