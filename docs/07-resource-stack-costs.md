# Resource Stack & Cost Tracking

## Technology Stack Overview

### Core Stack (90% Open Source)

#### Backend Stack
```yaml
Framework:
  - FastAPI (Python web framework)
  - Celery (Task queue)
  - SQLAlchemy (ORM)
  - Pydantic (Data validation)

Database:
  - Supabase (Postgres + Auth)
  - Redis (Caching & queue broker)
  - ChromaDB/Qdrant (Vector store)

AI/ML:
  - LangChain (Agent orchestration)
  - Instructor (Structured LLM outputs)
  - OpenAI SDK (GPT models)
  - Anthropic SDK (Claude models)

Testing:
  - Pytest (Unit/integration tests)
  - Locust (Load testing)
  - Black/Ruff (Code formatting)
```

#### Frontend Stack
```yaml
Framework:
  - Next.js 14 (React framework)
  - TypeScript (Type safety)
  - Tailwind CSS (Styling)
  - shadcn/ui (Component library)

State & Data:
  - Zustand (State management)
  - React Query (Data fetching)
  - React Hook Form (Forms)

Build Tools:
  - Vite (Build tool)
  - ESLint (Linting)
  - Prettier (Formatting)

Analytics:
  - PostHog (Product analytics)
  - Sentry (Error tracking)
```

#### Infrastructure
```yaml
Hosting:
  - Google Cloud Run (Backend)
  - Vercel (Frontend)
  - Google Cloud Storage (Files)

DevOps:
  - GitHub Actions (CI/CD)
  - Docker (Containerization)
  - Cloud Build (Image building)

Monitoring:
  - Google Cloud Monitoring
  - Uptime monitoring
  - Custom dashboards
```

### Paid APIs & Services (10%)

```yaml
AI Services:
  - OpenAI API (GPT-4, GPT-3.5)
  - Anthropic API (Claude)
  - Serper.dev (Web search)

Infrastructure:
  - Google Cloud Platform
  - Vercel Pro (optional)
  - GitHub Team (optional)

Marketing:
  - Resend (Email)
  - PostHog (Analytics)
  - Intercom (optional)
```

## Cost Breakdown

### Monthly Cost Projections

#### Phase 1: Development (Months 1-3)
| Service | Free Tier | Estimated Usage | Monthly Cost |
|---------|-----------|-----------------|--------------|
| Google Cloud | $300 credit | Light usage | $0 |
| OpenAI | $20 credit | Development | $50 |
| Anthropic | Pay as you go | Testing | $30 |
| Supabase | Free tier | <500MB | $0 |
| Vercel | Free tier | <100GB | $0 |
| GitHub | Free | Public repo | $0 |
| **Total** | | | **$80/month** |

#### Phase 2: MVP Launch (Months 4-6)
| Service | Usage | Unit Cost | Monthly Cost |
|---------|-------|-----------|--------------|
| Google Cloud Run | 100K requests | $0.40/million | $40 |
| Cloud Storage | 50GB | $0.02/GB | $1 |
| OpenAI GPT-4 | 2M tokens | $0.03/1K | $60 |
| OpenAI GPT-3.5 | 10M tokens | $0.002/1K | $20 |
| Anthropic Claude | 1M tokens | $0.015/1K | $15 |
| Serper API | 1K searches | $0.05/search | $50 |
| Supabase | Free tier | - | $0 |
| Vercel | Free tier | - | $0 |
| PostHog | <1M events | Free | $0 |
| Resend | <3K emails | Free | $0 |
| **Total** | | | **$186/month** |

#### Phase 3: Growth (Months 7-12)
| Service | Usage | Unit Cost | Monthly Cost |
|---------|-------|-----------|--------------|
| Google Cloud Run | 1M requests | $0.40/million | $400 |
| Cloud Storage | 200GB | $0.02/GB | $4 |
| OpenAI GPT-4 | 10M tokens | $0.03/1K | $300 |
| OpenAI GPT-3.5 | 50M tokens | $0.002/1K | $100 |
| Anthropic Claude | 5M tokens | $0.015/1K | $75 |
| Serper API | 5K searches | $0.05/search | $250 |
| Supabase | Pro tier | Fixed | $25 |
| Vercel | Pro tier | Fixed | $20 |
| PostHog | 2M events | - | $0 |
| Resend | 10K emails | - | $20 |
| **Total** | | | **$1,194/month** |

## Cost Optimization Strategies

### LLM Cost Optimization

```python
# Tiered LLM usage based on task complexity
llm_routing = {
    "simple_tasks": {
        "model": "gpt-3.5-turbo",
        "cost": "$0.002/1K tokens",
        "use_cases": ["basic extraction", "formatting"]
    },
    "complex_tasks": {
        "model": "gpt-4",
        "cost": "$0.03/1K tokens",
        "use_cases": ["analysis", "reasoning"]
    },
    "creative_tasks": {
        "model": "claude-3",
        "cost": "$0.015/1K tokens",
        "use_cases": ["copywriting", "ideation"]
    }
}

# Caching strategy
cache_config = {
    "ttl": 86400,  # 24 hours
    "max_size": "1GB",
    "cache_rate": 0.3  # 30% cache hit target
}
```

### Infrastructure Optimization

```yaml
# Cloud Run autoscaling
scaling:
  min_instances: 0  # Scale to zero
  max_instances: 10
  target_cpu: 60
  target_memory: 70

# Storage lifecycle
lifecycle:
  - action: "Delete"
    condition:
      age: 30  # Delete after 30 days
      type: "temp_files"
  - action: "Archive"
    condition:
      age: 90
      type: "user_data"
```

## Budget Allocation

### Monthly Budget Distribution
```python
budget_allocation = {
    "infrastructure": 0.20,  # 20% - Hosting, storage
    "ai_services": 0.50,     # 50% - LLMs, embeddings
    "tools_apis": 0.20,      # 20% - Search, monitoring
    "buffer": 0.10           # 10% - Unexpected costs
}

# Phase-based budgets
monthly_budgets = {
    "phase_1": 100,   # Development
    "phase_2": 300,   # MVP
    "phase_3": 1500   # Growth
}
```

## Cost Tracking Dashboard

### Metrics to Track
```sql
-- Daily cost query
SELECT 
    date,
    SUM(openai_cost) as openai,
    SUM(anthropic_cost) as anthropic,
    SUM(gcp_cost) as infrastructure,
    SUM(other_costs) as other,
    SUM(total_cost) as total
FROM daily_costs
WHERE date >= CURRENT_DATE - INTERVAL '30 days'
GROUP BY date
ORDER BY date DESC;

-- Cost per user
SELECT 
    COUNT(DISTINCT user_id) as users,
    SUM(total_cost) as total_cost,
    SUM(total_cost) / COUNT(DISTINCT user_id) as cost_per_user
FROM user_costs
WHERE month = CURRENT_MONTH;
```

### Alert Thresholds
```python
cost_alerts = {
    "daily": {
        "warning": 10,    # $10/day
        "critical": 20    # $20/day
    },
    "weekly": {
        "warning": 50,    # $50/week
        "critical": 100   # $100/week
    },
    "monthly": {
        "warning": 0.8,   # 80% of budget
        "critical": 1.0   # 100% of budget
    }
}
```

## Free Tier Maximization

### Service Limits & Optimization

| Service | Free Tier Limit | Optimization Strategy |
|---------|----------------|----------------------|
| Supabase | 500MB DB, 2GB storage | Archive old data, compress files |
| Vercel | 100GB bandwidth | CDN for static assets, optimize images |
| PostHog | 1M events/month | Sample events, batch updates |
| GitHub Actions | 2,000 min/month | Optimize workflows, use caching |
| Resend | 3,000 emails/month | Segment users, prioritize engaged |
| Google Cloud | $300 credit | Spread over 3 months |

## Resource Planning

### Scaling Triggers

```python
scaling_triggers = {
    "upgrade_supabase": {
        "condition": "database_size > 400MB",
        "action": "Move to Pro tier ($25/mo)",
        "impact": "+$25/month"
    },
    "upgrade_vercel": {
        "condition": "bandwidth > 90GB",
        "action": "Move to Pro tier ($20/mo)",
        "impact": "+$20/month"
    },
    "add_redis_cluster": {
        "condition": "concurrent_users > 1000",
        "action": "Deploy Redis cluster",
        "impact": "+$100/month"
    }
}
```

### Cost Reduction Checklist

```markdown
Weekly Review:
[ ] Review API usage reports
[ ] Check for unused resources
[ ] Optimize database queries
[ ] Review caching effectiveness
[ ] Audit third-party services

If over budget:
[ ] Enable aggressive caching
[ ] Reduce LLM token usage
[ ] Optimize prompt engineering
[ ] Defer non-critical features
[ ] Negotiate volume discounts
```

## ROI Calculations

### Unit Economics
```python
unit_economics = {
    "revenue_per_user": 50,      # Monthly subscription
    "cost_per_user": 15,         # All-in costs
    "gross_margin": 0.70,        # 70%
    "break_even_users": 20,      # Fixed costs / margin
    "target_ltv_cac": 3.0        # 3:1 ratio minimum
}
```

### Payback Period
- Customer Acquisition Cost: $50
- Monthly Revenue per User: $50
- Payback Period: 1 month
- 12-month LTV: $600
- LTV:CAC Ratio: 12:1

## Financial Projections

### 6-Month Forecast
| Month | Users | Revenue | Costs | Profit |
|-------|-------|---------|-------|--------|
| 1 | 0 | $0 | $100 | -$100 |
| 2 | 0 | $0 | $100 | -$100 |
| 3 | 10 | $100 | $200 | -$100 |
| 4 | 50 | $500 | $300 | $200 |
| 5 | 150 | $1,500 | $500 | $1,000 |
| 6 | 300 | $3,000 | $800 | $2,200 |

### Break-even Analysis
- Fixed Costs: $200/month (infrastructure base)
- Variable Cost per User: $10
- Price per User: $50
- Break-even: 5 paying users
- Target: 20 paying users by Month 4