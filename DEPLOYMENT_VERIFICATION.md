# ValidateIO Deployment Verification Guide

This guide provides step-by-step instructions for verifying that your ValidateIO deployment is working correctly with Supabase and GitHub Actions.

## Prerequisites

- Python 3.11+ installed
- Node.js 18+ installed
- Supabase project created
- GitHub repository configured
- Environment variables set up

## 1. Local Verification

### 1.1 Test Supabase Connection

First, ensure your local environment can connect to Supabase:

```bash
# Navigate to project root
cd /Users/tudorsaitoc/dev/validateio

# Make the script executable
chmod +x scripts/test_supabase_connection.py

# Run the Supabase connection test
python scripts/test_supabase_connection.py
```

Expected output:
- ✅ Environment variables are set
- ✅ Supabase client connection works
- ✅ Direct database connection works
- ✅ Authentication is configured

If any tests fail:
1. Check your `.env` file contains all required variables
2. Verify your Supabase project is active
3. Ensure your database URL is correct

### 1.2 Test Local API

Start the backend locally and test:

```bash
# Start the backend
cd backend
uvicorn main:app --reload --port 8000

# In another terminal, test the API
curl http://localhost:8000/health
```

Expected response:
```json
{
  "status": "healthy",
  "version": "0.1.0",
  "timestamp": "2025-01-08T12:00:00.000Z"
}
```

## 2. Deployment Verification

### 2.1 Deploy to Your Platform

Deploy your application using your chosen platform (Vercel, Railway, Render, etc.)

### 2.2 Test Deployed API Endpoints

Once deployed, test your API endpoints:

```bash
# Make the script executable
chmod +x scripts/test_deployed_api.py

# Test your deployed API (replace with your actual URL)
python scripts/test_deployed_api.py https://your-api-url.com

# With API key (if configured)
python scripts/test_deployed_api.py https://your-api-url.com --api-key YOUR_API_KEY

# Skip certain tests if needed
python scripts/test_deployed_api.py https://your-api-url.com --skip-auth --skip-performance
```

The script will test:
- Health check endpoints
- API documentation availability
- Authentication endpoints
- Validation endpoints
- API performance

### 2.3 Verify Database Migrations

Check that your database migrations have run successfully:

```bash
# Connect to your Supabase SQL editor or use psql
# Run this query to check migration history
SELECT * FROM alembic_version;

# Check that all tables exist
SELECT table_name 
FROM information_schema.tables 
WHERE table_schema = 'public'
ORDER BY table_name;
```

Expected tables:
- `users`
- `validations`
- `validation_results`
- `alembic_version`

## 3. GitHub Actions Verification

### 3.1 Check Workflow Status

1. Go to your GitHub repository
2. Click on the "Actions" tab
3. Check the status of recent workflows

### 3.2 Required Secrets

Ensure these secrets are set in your GitHub repository settings:

- `SUPABASE_URL`
- `SUPABASE_ANON_KEY`
- `SUPABASE_SERVICE_KEY`
- `DATABASE_URL`
- `OPENAI_API_KEY` (if using OpenAI)
- `ANTHROPIC_API_KEY` (if using Anthropic)

### 3.3 Test Automated Deployment

Make a small change and push to trigger deployment:

```bash
# Make a small change (e.g., update version in backend/app/core/config.py)
git add .
git commit -m "test: verify automated deployment"
git push origin main
```

Monitor the GitHub Actions tab to ensure:
1. Tests pass
2. Build succeeds
3. Deployment completes

## 4. Monitoring and Logs

### 4.1 Check Application Logs

Depending on your deployment platform:

**Vercel:**
```bash
vercel logs
```

**Railway:**
Check logs in the Railway dashboard

**Render:**
Check logs in the Render dashboard

### 4.2 Monitor Supabase

1. Go to your Supabase dashboard
2. Check the "Database" tab for query logs
3. Check the "Auth" tab for authentication logs
4. Monitor the "Storage" tab if using file storage

## 5. Common Issues and Solutions

### Issue: Database Connection Timeout

**Solution:**
- Check if your deployment platform IP is whitelisted in Supabase
- Verify the DATABASE_URL uses the correct connection pooling mode
- Ensure SSL mode is configured correctly

### Issue: CORS Errors

**Solution:**
- Update `BACKEND_CORS_ORIGINS` in your environment variables
- Ensure your frontend URL is included in the allowed origins

### Issue: Authentication Not Working

**Solution:**
- Verify `SUPABASE_JWT_SECRET` matches your Supabase project
- Check that `USE_SUPABASE_AUTH` is set to `true`
- Ensure Supabase Auth is properly configured

### Issue: API Endpoints Return 404

**Solution:**
- Verify the API is deployed at the expected URL
- Check that the `/api/v1` prefix is being used
- Ensure all routes are properly registered

## 6. Performance Benchmarks

After deployment, your API should meet these benchmarks:

- Health check: < 200ms
- Authentication: < 500ms
- Validation creation: < 2s
- List operations: < 1s

Use the performance test in the API testing script to verify.

## 7. Next Steps

Once verification is complete:

1. Set up monitoring (e.g., Sentry, LogRocket)
2. Configure alerts for errors and downtime
3. Set up automated backups for your database
4. Review and update security settings
5. Plan for scaling as usage grows

## Support

If you encounter issues:

1. Check the logs for detailed error messages
2. Verify all environment variables are set correctly
3. Ensure your Supabase project is active and not paused
4. Review the deployment platform's documentation

---

Remember to keep your API keys and secrets secure. Never commit them to version control!