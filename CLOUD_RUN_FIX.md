# 🔧 Fixing Cloud Run 403 Forbidden Error

## Quick Fix via Cloud Console

Since you're getting a 403 Forbidden error on your health endpoint, here's how to fix it:

### Option 1: Use Google Cloud Console (Web UI)

1. Go to: https://console.cloud.google.com/run
2. Click on your service: `validateio-backend`
3. Click the "EDIT & DEPLOY NEW REVISION" button
4. Scroll to the "Authentication" section
5. Select: **"Allow unauthenticated invocations"**
6. Click "DEPLOY"

### Option 2: Use Cloud Shell

1. Open Cloud Shell: https://console.cloud.google.com/
2. Click the terminal icon (>_) in the top right
3. Run these commands:

```bash
# Make the service public
gcloud run services add-iam-policy-binding validateio-backend \
  --member="allUsers" \
  --role="roles/run.invoker" \
  --region=us-central1

# Or update the service
gcloud run services update validateio-backend \
  --allow-unauthenticated \
  --region=us-central1
```

### Option 3: Trigger New Deployment

Since your GitHub Actions already has `--allow-unauthenticated`, you can:

1. Make a small change (like adding a comment to main.py)
2. Commit and push to main branch
3. This will trigger a new deployment with the correct settings

```bash
cd /Users/tudorsaitoc/dev/validateio
echo "# Trigger deployment" >> backend/main.py
git add backend/main.py
git commit -m "fix: trigger deployment with public access"
git push origin main
```

## Verify the Fix

Once done, test your health endpoint:

```bash
curl https://validateio-backend-[YOUR-PROJECT-ID].run.app/health
```

You should see:
```json
{
  "status": "healthy",
  "service": "validateio-api",
  "version": "0.1.0"
}
```

## Why This Happened

Cloud Run services are private by default. Even though your CD workflow includes `--allow-unauthenticated`, it might not have applied if:
- The initial deployment was manual
- There was a partial deployment failure
- The service was created before adding the flag

## Next Steps

After fixing authentication:
1. ✅ Test the health endpoint
2. ✅ Test the detailed health endpoint: `/health/detailed`
3. ✅ Check your API documentation: `/docs`
4. ✅ Verify Supabase connection in detailed health