# ValidateIO Deployment Guide

This guide covers the complete CI/CD setup for deploying ValidateIO to Google Cloud Run.

## Prerequisites

1. Google Cloud Project with billing enabled
2. GitHub repository with the ValidateIO code
3. Required APIs enabled in GCP:
   - Cloud Run API
   - Container Registry API
   - Cloud Build API

## GitHub Secrets Setup

Add these secrets to your GitHub repository (Settings → Secrets → Actions):

### Required Secrets

1. **GCP_PROJECT_ID**: Your Google Cloud project ID
2. **GCP_PROJECT_NUMBER**: Your Google Cloud project number
3. **GCP_SA_KEY**: Service account key (JSON) with these roles:
   - Cloud Run Admin
   - Storage Admin
   - Service Account User

### Backend Environment Secrets

4. **SUPABASE_URL**: Your Supabase project URL
5. **SUPABASE_ANON_KEY**: Supabase anonymous key
6. **SUPABASE_SERVICE_KEY**: Supabase service key
7. **OPENAI_API_KEY**: OpenAI API key
8. **GOOGLE_API_KEY**: Google API key (optional)
9. **SERPER_API_KEY**: Serper API key (optional)
10. **LANGCHAIN_API_KEY**: LangChain API key (optional)
11. **LANGCHAIN_TRACING_V2**: Set to "true" if using LangChain tracing
12. **LANGCHAIN_PROJECT**: LangChain project name
13. **JWT_SECRET**: Random secret for JWT signing
14. **FRONTEND_URL**: Production frontend URL (e.g., https://validateio-frontend-XXX.run.app)

## Deployment Workflows

### Automatic Deployments

The CI/CD pipeline automatically deploys:

1. **Frontend**: When changes are pushed to `frontend/**` on main branch
2. **Backend**: When changes are pushed to `backend/**` on main branch
3. **CI Tests**: Run on all pull requests

### Manual Deployment

To manually trigger a deployment:

1. Go to Actions tab in GitHub
2. Select "Deploy Frontend" or "Deploy Backend"
3. Click "Run workflow"
4. Select main branch
5. Click "Run workflow" button

## Local Testing

### Frontend
```bash
cd frontend
npm install
npm run dev
```

### Backend
```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
uvicorn main:app --reload
```

## Environment Variables

### Frontend (.env.local)
```env
NEXT_PUBLIC_API_URL=http://localhost:8000
```

### Backend (.env)
```env
ENVIRONMENT=development
SUPABASE_URL=your-supabase-url
SUPABASE_ANON_KEY=your-anon-key
SUPABASE_SERVICE_KEY=your-service-key
OPENAI_API_KEY=your-openai-key
JWT_SECRET=your-jwt-secret
FRONTEND_URL=http://localhost:3000
```

## Monitoring

### Cloud Run Console
- Frontend: https://console.cloud.google.com/run/detail/us-central1/validateio-frontend
- Backend: https://console.cloud.google.com/run/detail/us-central1/validateio-backend

### Logs
```bash
# Frontend logs
gcloud logging read "resource.type=cloud_run_revision AND resource.labels.service_name=validateio-frontend" --limit 50

# Backend logs
gcloud logging read "resource.type=cloud_run_revision AND resource.labels.service_name=validateio-backend" --limit 50
```

## Troubleshooting

### Common Issues

1. **403 Forbidden**: Ensure Cloud Run service is set to allow unauthenticated access
2. **Build failures**: Check GitHub Actions logs for detailed error messages
3. **CORS errors**: Verify FRONTEND_URL is correctly set in backend environment
4. **API connection issues**: Ensure NEXT_PUBLIC_API_URL doesn't have trailing slash

### Rolling Back

To rollback to a previous version:

```bash
# List all revisions
gcloud run revisions list --service=validateio-backend --region=us-central1

# Route traffic to specific revision
gcloud run services update-traffic validateio-backend --to-revisions=validateio-backend-00008-abc=100 --region=us-central1
```

## Cost Optimization

1. Set minimum instances to 0 for both services
2. Use Cloud Run's automatic scaling
3. Monitor usage in GCP Console
4. Consider using Cloud CDN for frontend assets

## Security Best Practices

1. Never commit secrets to the repository
2. Use least-privilege service accounts
3. Enable Cloud Run Binary Authorization
4. Set up VPC Service Controls if needed
5. Regularly rotate API keys and secrets

## Next Steps

1. Set up custom domain
2. Configure Cloud CDN
3. Set up monitoring alerts
4. Implement backup strategy
5. Configure rate limiting