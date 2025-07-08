# Experiment Generator Agent

The Experiment Generator Agent is part of ValidateIO's validation pipeline. It takes market research results as input and generates comprehensive experiments for business validation.

## Features

### 1. Landing Page Variations
- Generates 3-4 unique landing page designs
- Each variation includes:
  - Headlines and subheadlines
  - Call-to-action text
  - Value propositions
  - Feature lists
  - Social proof elements
  - Design style recommendations
  - Color scheme suggestions

### 2. A/B Test Configurations
- Creates 3-5 specific A/B tests
- Each test includes:
  - Clear hypothesis
  - Control and test variants
  - Primary and secondary metrics
  - Sample size calculations
  - Expected improvement ranges

### 3. Copy Variations
- Produces 4-6 different copy approaches
- Variations include:
  - Different tones (professional, casual, urgent)
  - Multiple headlines
  - Body copy options
  - CTA variations
  - Pain point and benefit focus

### 4. Target Audience Segments
- Defines 3-4 distinct audience segments
- Each segment includes:
  - Demographics and psychographics
  - Specific pain points
  - Recommended channels
  - Messaging approaches
  - Audience size estimates

## Usage

```python
from app.agents import ExperimentGeneratorAgent

# Initialize the agent
agent = ExperimentGeneratorAgent()

# Generate experiments
results = await agent.generate_experiments(
    business_idea="Your business idea",
    market_research=market_research_results,  # From MarketResearchAgent
    target_market="Optional target market",
    industry="Optional industry"
)
```

## Output Structure

The agent returns results matching the `ExperimentResult` schema:

```python
{
    "landing_pages": [...],      # List of landing page variations
    "ab_tests": [...],          # List of A/B test configurations
    "copy_variations": [...],   # List of copy variations
    "target_audiences": [...],  # List of target audience segments
    "predicted_conversion_rate": 2.5,  # Predicted conversion rate percentage
    "confidence_score": 0.85,   # Confidence in predictions (0-1)
    "rationale": "..."          # Explanation of experiment design choices
}
```

## Tools

The agent includes two built-in tools:

1. **Conversion Rate Estimator**: Estimates conversion rates based on industry benchmarks
2. **Audience Size Estimator**: Calculates potential audience sizes based on demographics

## Configuration

The agent uses the following settings from `app.core.config`:
- `OPENAI_API_KEY`: Required for LLM functionality
- `AGENT_TIMEOUT_SECONDS`: Maximum execution time (default: 30 seconds)

## Integration

The agent is designed to work seamlessly with:
- `MarketResearchAgent`: Takes market research results as input
- `MarketingCampaignAgent`: Experiments inform campaign creation (future)

See `example_integration.py` for a complete workflow example.