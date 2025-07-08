"""
Marketing Autopilot Agent for ValidateIO.

This agent generates marketing campaigns based on market research and experiments including:
- Ad campaign strategies
- Content marketing plans
- Channel recommendations
- Budget allocation
- ROI predictions
"""

import json
import logging
import re
from typing import Any, Dict, List, Optional

from langchain.agents import AgentExecutor, create_openai_functions_agent
from langchain.output_parsers import PydanticOutputParser
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.schema import SystemMessage
from langchain_core.tools import Tool
from langchain_openai import ChatOpenAI
from pydantic import BaseModel, Field

from app.core.config import settings
from app.schemas.validation import MarketingCampaignResult

logger = logging.getLogger(__name__)


class AdCampaign(BaseModel):
    """Ad campaign model."""
    campaign_name: str = Field(description="Campaign name")
    platform: str = Field(description="Advertising platform (Google Ads, Facebook, LinkedIn, etc.)")
    campaign_type: str = Field(description="Campaign type (search, display, video, social)")
    target_audience: str = Field(description="Target audience for this campaign")
    budget_allocation: float = Field(description="Budget allocation percentage for this campaign")
    key_message: str = Field(description="Primary message/hook")
    ad_copy: str = Field(description="Main ad copy (2-3 sentences)")
    cta: str = Field(description="Call-to-action")
    expected_cpc: float = Field(description="Expected cost per click in USD")
    expected_ctr: float = Field(description="Expected click-through rate percentage")
    expected_conversion_rate: float = Field(description="Expected conversion rate percentage")


class ContentPiece(BaseModel):
    """Content piece model."""
    content_type: str = Field(description="Type of content (blog, video, infographic, etc.)")
    title: str = Field(description="Content title")
    topic: str = Field(description="Main topic/theme")
    target_keywords: List[str] = Field(description="Target keywords for SEO")
    content_goal: str = Field(description="Primary goal (awareness, education, conversion)")
    distribution_channels: List[str] = Field(description="Where to distribute this content")


class ContentStrategy(BaseModel):
    """Content strategy model."""
    content_pillars: List[str] = Field(description="Main content themes/pillars")
    content_calendar: List[ContentPiece] = Field(description="First month's content calendar")
    publishing_frequency: str = Field(description="How often to publish (e.g., 2x per week)")
    primary_formats: List[str] = Field(description="Main content formats to focus on")


class ChannelRecommendation(BaseModel):
    """Marketing channel recommendation model."""
    channel: str = Field(description="Marketing channel name")
    priority: str = Field(description="Priority level (high, medium, low)")
    reasoning: str = Field(description="Why this channel is recommended")
    estimated_reach: int = Field(description="Estimated monthly reach")
    estimated_cost: float = Field(description="Estimated monthly cost in USD")
    expected_roi: float = Field(description="Expected ROI percentage")


class StructuredMarketingCampaigns(BaseModel):
    """Structured output for marketing campaigns."""
    ad_campaigns: List[AdCampaign] = Field(description="4-6 ad campaign configurations")
    content_strategy: ContentStrategy = Field(description="Content marketing strategy")
    channel_recommendations: List[ChannelRecommendation] = Field(description="5-7 marketing channel recommendations")
    total_monthly_budget: float = Field(description="Recommended total monthly budget in USD")
    budget_allocation: Dict[str, float] = Field(description="Budget allocation by channel/category")
    expected_monthly_leads: int = Field(description="Expected monthly leads")
    expected_cac: float = Field(description="Expected customer acquisition cost in USD")
    expected_roi: float = Field(description="Expected overall ROI percentage")
    confidence_score: float = Field(description="Confidence in predictions (0-1)")
    rationale: str = Field(description="Strategic rationale for the marketing plan")


class MarketingAutopilotAgent:
    """Agent for generating marketing campaigns based on market research and experiments."""
    
    def __init__(self):
        """Initialize the marketing autopilot agent."""
        self.llm = ChatOpenAI(
            model="gpt-4-turbo-preview",
            temperature=0.7,
            openai_api_key=settings.OPENAI_API_KEY,
        )
        self.structured_llm = ChatOpenAI(
            model="gpt-4-turbo-preview",
            temperature=0.3,  # Lower temperature for structured output
            openai_api_key=settings.OPENAI_API_KEY,
        )
        self.tools = self._create_tools()
        self.agent = self._create_agent()
        self.output_parser = PydanticOutputParser(pydantic_object=StructuredMarketingCampaigns)
    
    def _create_tools(self) -> List[Tool]:
        """Create tools for the agent."""
        tools = []
        
        # ROI calculator tool
        tools.append(
            Tool(
                name="roi_calculator",
                description="Calculate expected ROI based on channel, budget, and conversion rates",
                func=self._calculate_roi,
            )
        )
        
        # Budget optimizer tool
        tools.append(
            Tool(
                name="budget_optimizer",
                description="Optimize budget allocation across channels based on expected performance",
                func=self._optimize_budget,
            )
        )
        
        # CAC estimator tool
        tools.append(
            Tool(
                name="cac_estimator",
                description="Estimate customer acquisition cost based on channel mix and conversion rates",
                func=self._estimate_cac,
            )
        )
        
        return tools
    
    def _calculate_roi(self, query: str) -> str:
        """Calculate ROI based on channel and metrics."""
        # Industry benchmark data for different channels
        channel_benchmarks = {
            "google_ads": {"cpc": 2.5, "ctr": 3.5, "conv_rate": 2.5},
            "facebook": {"cpc": 1.8, "ctr": 1.9, "conv_rate": 2.0},
            "linkedin": {"cpc": 5.5, "ctr": 0.9, "conv_rate": 1.5},
            "content_marketing": {"cpc": 0.5, "ctr": 5.0, "conv_rate": 3.0},
            "email": {"cpc": 0.1, "ctr": 20.0, "conv_rate": 4.0},
            "seo": {"cpc": 0.3, "ctr": 4.0, "conv_rate": 2.8},
        }
        
        # Extract budget if mentioned (default $5000)
        budget = 5000
        if "$" in query:
            try:
                budget_match = re.search(r'\$(\d+(?:,\d+)?)', query)
                if budget_match:
                    budget = float(budget_match.group(1).replace(',', ''))
            except:
                pass
        
        # Calculate weighted average ROI
        total_roi = 0
        channel_count = 0
        
        for channel, metrics in channel_benchmarks.items():
            if channel.replace('_', ' ').lower() in query.lower():
                clicks = budget / metrics["cpc"]
                conversions = clicks * (metrics["conv_rate"] / 100)
                revenue = conversions * 150  # Assume $150 LTV
                roi = ((revenue - budget) / budget) * 100
                total_roi += roi
                channel_count += 1
        
        if channel_count == 0:
            # Default ROI calculation
            avg_roi = 125  # Industry average
        else:
            avg_roi = total_roi / channel_count
        
        return f"Expected ROI: {avg_roi:.1f}% based on channel mix and ${'%.2f' % budget} budget"
    
    def _optimize_budget(self, query: str) -> str:
        """Optimize budget allocation across channels."""
        # Extract total budget
        total_budget = 10000  # Default
        if "$" in query:
            try:
                budget_match = re.search(r'\$(\d+(?:,\d+)?)', query)
                if budget_match:
                    total_budget = float(budget_match.group(1).replace(',', ''))
            except:
                pass
        
        # Recommended allocation based on business type
        if "b2b" in query.lower():
            allocation = {
                "LinkedIn Ads": 30,
                "Google Ads": 25,
                "Content Marketing": 20,
                "Email Marketing": 15,
                "SEO": 10
            }
        elif "ecommerce" in query.lower():
            allocation = {
                "Google Ads": 35,
                "Facebook/Instagram": 30,
                "Email Marketing": 15,
                "Content Marketing": 10,
                "Influencer Marketing": 10
            }
        else:  # Default SaaS/Tech
            allocation = {
                "Google Ads": 30,
                "Content Marketing": 25,
                "Facebook Ads": 20,
                "SEO": 15,
                "Email Marketing": 10
            }
        
        breakdown = []
        for channel, percent in allocation.items():
            amount = total_budget * (percent / 100)
            breakdown.append(f"{channel}: ${amount:.0f} ({percent}%)")
        
        return f"Optimized budget allocation for ${total_budget:.0f}:\n" + "\n".join(breakdown)
    
    def _estimate_cac(self, query: str) -> str:
        """Estimate customer acquisition cost."""
        # Base CAC by industry
        industry_cac = {
            "saas": 395,
            "ecommerce": 70,
            "fintech": 450,
            "healthcare": 550,
            "education": 250,
            "marketplace": 300,
            "consumer": 120,
            "b2b": 475,
        }
        
        # Default CAC
        base_cac = 300
        
        # Find industry match
        for industry, cac in industry_cac.items():
            if industry.lower() in query.lower():
                base_cac = cac
                break
        
        # Adjust based on targeting
        if "enterprise" in query.lower():
            base_cac *= 1.5
        elif "smb" in query.lower() or "small business" in query.lower():
            base_cac *= 0.7
        
        # Adjust based on channels
        if "organic" in query.lower() or "content" in query.lower():
            base_cac *= 0.6
        elif "paid" in query.lower():
            base_cac *= 1.2
        
        return f"Estimated Customer Acquisition Cost: ${base_cac:.0f} based on industry benchmarks and channel mix"
    
    def _create_agent(self) -> AgentExecutor:
        """Create the agent executor."""
        system_message = SystemMessage(
            content="""You are a marketing strategy expert and growth hacker.
            
Your goal is to create comprehensive marketing campaigns based on market research and experiment results. You must:

1. **Design 4-6 ad campaigns**
   - Different platforms (Google, Facebook, LinkedIn, etc.)
   - Specific targeting and messaging
   - Budget allocation per campaign
   - Expected metrics (CPC, CTR, conversion rate)

2. **Create content marketing strategy**
   - Content pillars aligned with customer pain points
   - First month's content calendar with specific pieces
   - Distribution strategy across channels
   - SEO-focused approach

3. **Recommend 5-7 marketing channels**
   - Priority ranking based on target audience
   - Expected reach and cost per channel
   - ROI projections for each
   - Clear reasoning for recommendations

4. **Allocate budget strategically**
   - Total monthly budget recommendation
   - Percentage allocation by channel/campaign
   - Expected CAC and ROI calculations
   - Performance tracking metrics

5. **Project results**
   - Expected monthly leads
   - Customer acquisition cost
   - Overall ROI percentage
   - Key success metrics

Base all recommendations on:
- Market research insights (competitors, pain points, trends)
- Experiment results (best performing messages, audiences)
- Industry benchmarks and best practices
- Realistic budget constraints for startups

Be specific, actionable, and data-driven in all recommendations.
Focus on channels and strategies that can show results within 30-60 days.
"""
        )
        
        prompt = ChatPromptTemplate.from_messages([
            system_message,
            MessagesPlaceholder(variable_name="chat_history", optional=True),
            ("human", "{input}"),
            MessagesPlaceholder(variable_name="agent_scratchpad"),
        ])
        
        agent = create_openai_functions_agent(
            llm=self.llm,
            tools=self.tools,
            prompt=prompt,
        )
        
        return AgentExecutor(
            agent=agent,
            tools=self.tools,
            verbose=True,
            max_iterations=5,
            max_execution_time=settings.AGENT_TIMEOUT_SECONDS,
            handle_parsing_errors=True,
        )
    
    def _parse_structured_output(self, raw_output: str) -> StructuredMarketingCampaigns:
        """Parse the agent's output into structured format."""
        try:
            # First try to extract JSON from the output
            json_match = re.search(r'\{[\s\S]*\}', raw_output)
            if json_match:
                json_str = json_match.group()
                return self.output_parser.parse(json_str)
        except Exception as e:
            logger.warning(f"Failed to parse JSON from output: {e}")
        
        # Fallback: Use LLM to structure the output
        try:
            format_instructions = self.output_parser.get_format_instructions()
            prompt = ChatPromptTemplate.from_template(
                """Given the following marketing campaign output, structure it according to the format instructions.
                
Marketing Campaign Output:
{raw_output}

{format_instructions}

Create specific, actionable campaigns with realistic metrics based on industry standards.
Ensure all recommendations are data-driven and achievable within typical startup budgets.
"""
            )
            
            messages = prompt.format_messages(
                raw_output=raw_output,
                format_instructions=format_instructions
            )
            
            response = self.structured_llm.invoke(messages)
            return self.output_parser.parse(response.content)
            
        except Exception as e:
            logger.error(f"Failed to structure output: {e}")
            # Return a default structure
            return StructuredMarketingCampaigns(
                ad_campaigns=[],
                content_strategy=ContentStrategy(
                    content_pillars=[],
                    content_calendar=[],
                    publishing_frequency="2x per week",
                    primary_formats=[]
                ),
                channel_recommendations=[],
                total_monthly_budget=5000,
                budget_allocation={},
                expected_monthly_leads=50,
                expected_cac=200,
                expected_roi=100,
                confidence_score=0.1,
                rationale="Unable to parse marketing campaigns"
            )
    
    def _convert_to_schema_format(self, structured_data: StructuredMarketingCampaigns) -> MarketingCampaignResult:
        """Convert structured data to the schema format."""
        ad_campaigns = []
        for campaign in structured_data.ad_campaigns:
            ad_campaigns.append({
                "campaign_name": campaign.campaign_name,
                "platform": campaign.platform,
                "campaign_type": campaign.campaign_type,
                "target_audience": campaign.target_audience,
                "budget_allocation": campaign.budget_allocation,
                "key_message": campaign.key_message,
                "ad_copy": campaign.ad_copy,
                "cta": campaign.cta,
                "expected_cpc": campaign.expected_cpc,
                "expected_ctr": campaign.expected_ctr,
                "expected_conversion_rate": campaign.expected_conversion_rate
            })
        
        content_strategy = {
            "content_pillars": structured_data.content_strategy.content_pillars,
            "content_calendar": [
                {
                    "content_type": piece.content_type,
                    "title": piece.title,
                    "topic": piece.topic,
                    "target_keywords": piece.target_keywords,
                    "content_goal": piece.content_goal,
                    "distribution_channels": piece.distribution_channels
                }
                for piece in structured_data.content_strategy.content_calendar
            ],
            "publishing_frequency": structured_data.content_strategy.publishing_frequency,
            "primary_formats": structured_data.content_strategy.primary_formats
        }
        
        channel_recommendations = [
            rec.channel for rec in structured_data.channel_recommendations
        ]
        
        return MarketingCampaignResult(
            ad_campaigns=ad_campaigns,
            content_strategy=content_strategy,
            channel_recommendations=channel_recommendations,
            budget_allocation=structured_data.budget_allocation,
            expected_roi=structured_data.expected_roi
        )
    
    async def generate_campaigns(
        self,
        business_idea: str,
        market_research: Dict[str, Any],
        experiment_results: Dict[str, Any],
        target_market: str = None,
        industry: str = None,
        monthly_budget: float = None,
    ) -> Dict[str, Any]:
        """
        Generate marketing campaigns based on market research and experiment results.
        
        Args:
            business_idea: The business idea to create campaigns for
            market_research: Market research results
            experiment_results: Experiment results with winning variations
            target_market: Optional target market specification
            industry: Optional industry specification
            monthly_budget: Optional monthly budget constraint
            
        Returns:
            Marketing campaign results
        """
        try:
            # Extract key insights
            competitors = market_research.get("competitors", [])
            pain_points = market_research.get("customer_pain_points", [])
            value_prop = market_research.get("unique_value_proposition", "")
            market_trends = market_research.get("market_trends", [])
            
            # Extract winning experiments
            landing_pages = experiment_results.get("landing_pages", [])
            best_copy = experiment_results.get("copy_variations", [])
            target_audiences = experiment_results.get("target_audiences", [])
            predicted_conversion = experiment_results.get("predicted_conversion_rate", 2.0)
            
            # Construct campaign generation query
            query = f"""Create comprehensive marketing campaigns for: {business_idea}

Market Research Insights:
- Value Proposition: {value_prop}
- Top Pain Points: {', '.join(pain_points[:3]) if pain_points else 'Not specified'}
- Market Trends: {', '.join(market_trends[:3]) if market_trends else 'Not specified'}
- Key Competitors: {', '.join([c.get('name', '') for c in competitors[:3]]) if competitors else 'Not specified'}

Winning Experiment Results:
- Best Headlines: {', '.join([lp.get('headline', '') for lp in landing_pages[:2]]) if landing_pages else 'Not specified'}
- Top Performing Copy Tone: {best_copy[0].get('tone', 'Not specified') if best_copy else 'Not specified'}
- Primary Target Audiences: {', '.join([ta.get('segment_name', '') for ta in target_audiences[:2]]) if target_audiences else 'Not specified'}
- Predicted Conversion Rate: {predicted_conversion}%
"""
            
            if target_market:
                query += f"\nTarget Market: {target_market}"
            if industry:
                query += f"\nIndustry: {industry}"
            if monthly_budget:
                query += f"\nMonthly Budget Constraint: ${monthly_budget}"
            else:
                query += "\nMonthly Budget: Recommend optimal budget for a startup"
            
            query += """

Design campaigns that:
1. Leverage the winning messages and audiences from experiments
2. Focus on channels where our target audience is most active
3. Maximize ROI within budget constraints
4. Can show measurable results within 30-60 days
5. Build on competitor weaknesses and market opportunities

Provide specific, actionable recommendations with realistic metrics."""
            
            # Run the agent
            logger.info(f"Generating marketing campaigns for: {business_idea}")
            result = await self.agent.ainvoke({"input": query})
            raw_output = result.get("output", "")
            
            # Parse and structure the results
            structured_data = self._parse_structured_output(raw_output)
            
            # Convert to schema format
            campaign_result = self._convert_to_schema_format(structured_data)
            
            # Return as dict for API response
            return {
                "raw_output": raw_output,
                "ad_campaigns": campaign_result.ad_campaigns,
                "content_strategy": campaign_result.content_strategy,
                "channel_recommendations": campaign_result.channel_recommendations,
                "budget_allocation": campaign_result.budget_allocation,
                "expected_roi": campaign_result.expected_roi,
                "total_monthly_budget": structured_data.total_monthly_budget,
                "expected_monthly_leads": structured_data.expected_monthly_leads,
                "expected_cac": structured_data.expected_cac,
                "confidence_score": structured_data.confidence_score,
                "rationale": structured_data.rationale,
                # Additional detailed recommendations from structured data
                "channel_details": [
                    {
                        "channel": rec.channel,
                        "priority": rec.priority,
                        "reasoning": rec.reasoning,
                        "estimated_reach": rec.estimated_reach,
                        "estimated_cost": rec.estimated_cost,
                        "expected_roi": rec.expected_roi
                    }
                    for rec in structured_data.channel_recommendations
                ]
            }
            
        except Exception as e:
            logger.error(f"Marketing campaign generation failed: {str(e)}")
            raise