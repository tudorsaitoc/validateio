"""
Experiment Generator Agent for ValidateIO.

This agent generates experiments for business validation including:
- Landing page variations
- A/B test configurations
- Copy variations
- Target audience definitions
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
from app.schemas.validation import ExperimentResult

logger = logging.getLogger(__name__)


class LandingPageVariation(BaseModel):
    """Landing page variation model."""
    variant_id: str = Field(description="Unique identifier for the variant (e.g., 'A', 'B', 'C')")
    headline: str = Field(description="Main headline for the landing page")
    subheadline: str = Field(description="Supporting subheadline")
    cta_text: str = Field(description="Call-to-action button text")
    value_proposition: str = Field(description="Primary value proposition")
    features: List[str] = Field(description="Key features to highlight (3-5 items)")
    social_proof: str = Field(description="Social proof element (testimonial, stat, etc.)")
    design_style: str = Field(description="Design approach (minimal, bold, professional, etc.)")
    color_scheme: str = Field(description="Primary color scheme recommendation")


class ABTest(BaseModel):
    """A/B test configuration model."""
    test_name: str = Field(description="Name of the A/B test")
    hypothesis: str = Field(description="Test hypothesis")
    control_variant: str = Field(description="Control variant identifier")
    test_variant: str = Field(description="Test variant identifier")
    primary_metric: str = Field(description="Primary metric to measure")
    secondary_metrics: List[str] = Field(description="Secondary metrics to track")
    minimum_sample_size: int = Field(description="Minimum sample size per variant")
    expected_improvement: float = Field(description="Expected improvement percentage")


class CopyVariation(BaseModel):
    """Copy variation model."""
    variant_id: str = Field(description="Unique identifier for the variant")
    tone: str = Field(description="Copy tone (professional, casual, urgent, etc.)")
    headline: str = Field(description="Main headline copy")
    body_copy: str = Field(description="Main body copy (2-3 sentences)")
    cta_copy: str = Field(description="Call-to-action copy")
    pain_point_focus: str = Field(description="Primary pain point addressed")
    benefit_focus: str = Field(description="Primary benefit highlighted")


class TargetAudience(BaseModel):
    """Target audience definition model."""
    segment_name: str = Field(description="Name of the audience segment")
    demographics: Dict[str, Any] = Field(description="Age, gender, income, education, etc.")
    psychographics: List[str] = Field(description="Interests, values, lifestyle")
    pain_points: List[str] = Field(description="Specific pain points for this segment")
    channels: List[str] = Field(description="Best channels to reach this audience")
    messaging_approach: str = Field(description="Recommended messaging approach")
    estimated_size: int = Field(description="Estimated audience size")


class StructuredExperiments(BaseModel):
    """Structured output for experiments."""
    landing_pages: List[LandingPageVariation] = Field(description="3-4 landing page variations")
    ab_tests: List[ABTest] = Field(description="3-5 A/B test configurations")
    copy_variations: List[CopyVariation] = Field(description="4-6 copy variations")
    target_audiences: List[TargetAudience] = Field(description="3-4 target audience segments")
    predicted_conversion_rate: float = Field(description="Overall predicted conversion rate (0-100)")
    confidence_score: float = Field(description="Confidence in predictions (0-1)")
    rationale: str = Field(description="Brief rationale for experiment designs")


class ExperimentGeneratorAgent:
    """Agent for generating experiments based on market research."""
    
    def __init__(self):
        """Initialize the experiment generator agent."""
        self.llm = ChatOpenAI(
            model="gpt-4-turbo-preview",
            temperature=0.8,  # Higher temperature for creative variations
            openai_api_key=settings.OPENAI_API_KEY,
        )
        self.structured_llm = ChatOpenAI(
            model="gpt-4-turbo-preview",
            temperature=0.3,  # Lower temperature for structured output
            openai_api_key=settings.OPENAI_API_KEY,
        )
        self.tools = self._create_tools()
        self.agent = self._create_agent()
        self.output_parser = PydanticOutputParser(pydantic_object=StructuredExperiments)
    
    def _create_tools(self) -> List[Tool]:
        """Create tools for the agent."""
        tools = []
        
        # Conversion rate calculator tool
        tools.append(
            Tool(
                name="conversion_rate_estimator",
                description="Estimate conversion rates based on industry benchmarks and value proposition strength",
                func=self._estimate_conversion_rate,
            )
        )
        
        # Audience size estimator tool
        tools.append(
            Tool(
                name="audience_size_estimator",
                description="Estimate target audience size based on demographics and market data",
                func=self._estimate_audience_size,
            )
        )
        
        return tools
    
    def _estimate_conversion_rate(self, query: str) -> str:
        """Estimate conversion rate based on industry and value proposition."""
        # Simple heuristic for demo - in production, this would use real data
        base_rates = {
            "saas": 2.5,
            "ecommerce": 2.0,
            "fintech": 1.5,
            "healthcare": 1.8,
            "education": 3.0,
            "marketplace": 2.2,
            "consumer": 2.8,
            "b2b": 1.2,
        }
        
        # Default conversion rate
        default_rate = 2.0
        
        # Extract industry if mentioned
        industry_rate = default_rate
        for industry, rate in base_rates.items():
            if industry.lower() in query.lower():
                industry_rate = rate
                break
        
        # Adjust based on value proposition strength indicators
        if any(word in query.lower() for word in ["innovative", "unique", "first", "only"]):
            industry_rate *= 1.2
        if any(word in query.lower() for word in ["free", "trial", "demo"]):
            industry_rate *= 1.3
        if any(word in query.lower() for word in ["enterprise", "complex", "technical"]):
            industry_rate *= 0.8
            
        return f"Estimated conversion rate: {industry_rate:.1f}% based on industry benchmarks and value proposition analysis"
    
    def _estimate_audience_size(self, query: str) -> str:
        """Estimate audience size based on demographics."""
        # Simple estimation for demo purposes
        total_population = 300_000_000  # US population estimate
        
        # Apply filters based on query
        filtered_population = total_population
        
        if "millennials" in query.lower():
            filtered_population *= 0.22  # ~22% of population
        elif "gen z" in query.lower():
            filtered_population *= 0.20  # ~20% of population
        elif "professionals" in query.lower():
            filtered_population *= 0.40  # ~40% working professionals
            
        if "urban" in query.lower():
            filtered_population *= 0.82  # ~82% urban population
        elif "suburban" in query.lower():
            filtered_population *= 0.52  # ~52% suburban
            
        if "high income" in query.lower():
            filtered_population *= 0.20  # Top 20% income
        elif "middle income" in query.lower():
            filtered_population *= 0.50  # Middle 50%
            
        return f"Estimated audience size: {int(filtered_population):,} people based on demographic filters"
    
    def _create_agent(self) -> AgentExecutor:
        """Create the agent executor."""
        system_message = SystemMessage(
            content="""You are an expert conversion rate optimizer and experimental marketer.
            
Your goal is to design comprehensive experiments for validating business ideas. You must:

1. **Create 3-4 landing page variations**
   - Each with unique headline, value prop, and design approach
   - Different angles to test market response
   - Include specific copy and visual recommendations

2. **Design 3-5 A/B tests**
   - Clear hypotheses based on market research
   - Specific metrics to measure
   - Realistic sample size calculations
   - Expected improvement ranges

3. **Generate 4-6 copy variations**
   - Different tones and approaches
   - Focus on different pain points and benefits
   - Vary urgency and social proof elements

4. **Define 3-4 target audience segments**
   - Specific demographics and psychographics
   - Unique pain points per segment
   - Channel and messaging recommendations
   - Realistic audience size estimates

5. **Predict overall conversion rates**
   - Based on industry benchmarks
   - Adjusted for value proposition strength
   - Consider market competition

Focus on creating diverse, testable variations that will provide clear validation signals.
Be specific and actionable in all recommendations.
Base predictions on realistic industry standards.
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
    
    def _parse_structured_output(self, raw_output: str) -> StructuredExperiments:
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
                """Given the following experiment design output, structure it according to the format instructions.
                
Experiment Design Output:
{raw_output}

{format_instructions}

Create diverse, specific variations that can be tested. Ensure all copy is compelling and targeted.
Make realistic predictions based on industry standards.
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
            # Return a default structure with the raw output
            return StructuredExperiments(
                landing_pages=[],
                ab_tests=[],
                copy_variations=[],
                target_audiences=[],
                predicted_conversion_rate=2.0,
                confidence_score=0.1,
                rationale="Unable to parse experiment designs"
            )
    
    def _convert_to_schema_format(self, structured_data: StructuredExperiments) -> ExperimentResult:
        """Convert structured data to the schema format."""
        landing_pages = []
        for lp in structured_data.landing_pages:
            landing_pages.append({
                "variant_id": lp.variant_id,
                "headline": lp.headline,
                "subheadline": lp.subheadline,
                "cta_text": lp.cta_text,
                "value_proposition": lp.value_proposition,
                "features": lp.features,
                "social_proof": lp.social_proof,
                "design_style": lp.design_style,
                "color_scheme": lp.color_scheme
            })
        
        ab_tests = []
        for test in structured_data.ab_tests:
            ab_tests.append({
                "test_name": test.test_name,
                "hypothesis": test.hypothesis,
                "control_variant": test.control_variant,
                "test_variant": test.test_variant,
                "primary_metric": test.primary_metric,
                "secondary_metrics": test.secondary_metrics,
                "minimum_sample_size": test.minimum_sample_size,
                "expected_improvement": test.expected_improvement
            })
        
        copy_variations = []
        for copy in structured_data.copy_variations:
            copy_variations.append({
                "variant_id": copy.variant_id,
                "tone": copy.tone,
                "headline": copy.headline,
                "body_copy": copy.body_copy,
                "cta_copy": copy.cta_copy,
                "pain_point_focus": copy.pain_point_focus,
                "benefit_focus": copy.benefit_focus
            })
        
        target_audiences = []
        for audience in structured_data.target_audiences:
            target_audiences.append({
                "segment_name": audience.segment_name,
                "demographics": audience.demographics,
                "psychographics": audience.psychographics,
                "pain_points": audience.pain_points,
                "channels": audience.channels,
                "messaging_approach": audience.messaging_approach,
                "estimated_size": audience.estimated_size
            })
        
        return ExperimentResult(
            landing_pages=landing_pages,
            ab_tests=ab_tests,
            copy_variations=copy_variations,
            target_audiences=target_audiences,
            predicted_conversion_rate=structured_data.predicted_conversion_rate
        )
    
    async def generate_experiments(
        self,
        business_idea: str,
        market_research: Dict[str, Any],
        target_market: str = None,
        industry: str = None,
    ) -> Dict[str, Any]:
        """
        Generate experiments based on business idea and market research.
        
        Args:
            business_idea: The business idea to create experiments for
            market_research: Market research results to inform experiments
            target_market: Optional target market specification
            industry: Optional industry specification
            
        Returns:
            Experiment generation results
        """
        try:
            # Extract key insights from market research
            competitors = market_research.get("competitors", [])
            pain_points = market_research.get("customer_pain_points", [])
            value_prop = market_research.get("unique_value_proposition", "")
            market_trends = market_research.get("market_trends", [])
            
            # Construct experiment generation query
            query = f"""Design comprehensive experiments for: {business_idea}

Key Market Insights:
- Value Proposition: {value_prop}
- Top Customer Pain Points: {', '.join(pain_points[:3]) if pain_points else 'Not specified'}
- Key Market Trends: {', '.join(market_trends[:3]) if market_trends else 'Not specified'}
- Main Competitors: {', '.join([c.get('name', '') for c in competitors[:3]]) if competitors else 'Not specified'}
"""
            
            if target_market:
                query += f"\nTarget Market: {target_market}"
            if industry:
                query += f"\nIndustry: {industry}"
            
            query += """

Create diverse variations that test different value propositions, messaging angles, and audience segments.
Design experiments that will provide clear validation signals within 2-4 weeks.
Base all predictions on realistic industry benchmarks."""
            
            # Run the agent
            logger.info(f"Generating experiments for: {business_idea}")
            result = await self.agent.ainvoke({"input": query})
            raw_output = result.get("output", "")
            
            # Parse and structure the results
            structured_data = self._parse_structured_output(raw_output)
            
            # Convert to schema format
            experiment_result = self._convert_to_schema_format(structured_data)
            
            # Return as dict for API response
            return {
                "raw_output": raw_output,
                "landing_pages": experiment_result.landing_pages,
                "ab_tests": experiment_result.ab_tests,
                "copy_variations": experiment_result.copy_variations,
                "target_audiences": experiment_result.target_audiences,
                "predicted_conversion_rate": experiment_result.predicted_conversion_rate,
                "confidence_score": structured_data.confidence_score,
                "rationale": structured_data.rationale
            }
            
        except Exception as e:
            logger.error(f"Experiment generation failed: {str(e)}")
            raise