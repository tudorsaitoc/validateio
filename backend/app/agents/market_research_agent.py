"""
Market Research Agent for ValidateIO.

This agent performs comprehensive market research for business ideas including:
- Competitor analysis
- Market sizing (TAM/SAM/SOM)
- Customer pain point identification
- Market trends analysis
"""

import json
import logging
import re
from typing import Any, Dict, List, Optional

from langchain.agents import AgentExecutor, create_openai_functions_agent
from langchain.output_parsers import PydanticOutputParser
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.schema import SystemMessage
try:
    from langchain_community.utilities import GoogleSerperAPIWrapper
except ImportError:
    # Fallback if not available
    GoogleSerperAPIWrapper = None
try:
    from langchain_community.utilities import GoogleSearchAPIWrapper
except ImportError:
    GoogleSearchAPIWrapper = None
from langchain_core.tools import Tool
from langchain_openai import ChatOpenAI
from pydantic import BaseModel, Field

from app.core.config import settings
from app.schemas.validation import MarketResearchResult

logger = logging.getLogger(__name__)


class Competitor(BaseModel):
    """Competitor information model."""
    name: str = Field(description="Company name")
    description: str = Field(description="Brief description of the company")
    strengths: List[str] = Field(description="Key strengths")
    weaknesses: List[str] = Field(description="Key weaknesses")
    market_share: Optional[float] = Field(None, description="Estimated market share percentage")
    funding: Optional[str] = Field(None, description="Funding information if available")


class MarketSize(BaseModel):
    """Market size information model."""
    tam: float = Field(description="Total Addressable Market in USD")
    sam: float = Field(description="Serviceable Addressable Market in USD")
    som: float = Field(description="Serviceable Obtainable Market in USD")
    growth_rate: float = Field(description="Annual market growth rate percentage")
    source: str = Field(description="Source of market size data")


class StructuredMarketResearch(BaseModel):
    """Structured output for market research."""
    competitors: List[Competitor] = Field(description="Top 5 competitors analysis")
    market_size: MarketSize = Field(description="Market size breakdown")
    customer_pain_points: List[str] = Field(description="Key customer pain points")
    unique_value_proposition: str = Field(description="Unique value proposition")
    market_trends: List[str] = Field(description="Current market trends")
    confidence_score: float = Field(description="Confidence score 0-1")
    sources: List[str] = Field(description="Sources used for research")


class MarketResearchAgent:
    """Agent for conducting market research on business ideas."""
    
    def __init__(self):
        """Initialize the market research agent."""
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
        self.output_parser = PydanticOutputParser(pydantic_object=StructuredMarketResearch)
    
    def _create_tools(self) -> List[Tool]:
        """Create tools for the agent."""
        tools = []
        
        # Web search tool
        if settings.SERPER_API_KEY:
            search = GoogleSerperAPIWrapper(serper_api_key=settings.SERPER_API_KEY)
            tools.append(
                Tool(
                    name="web_search",
                    description="Search the web for current information about markets, competitors, and trends",
                    func=search.run,
                )
            )
        
        # Add more tools as needed (e.g., industry databases, patent search, etc.)
        
        return tools
    
    def _create_agent(self) -> AgentExecutor:
        """Create the agent executor."""
        system_message = SystemMessage(
            content="""You are a market research expert specializing in business validation.
            
Your goal is to provide comprehensive market research for business ideas. You must:

1. **Identify and analyze top 5 competitors**
   - Company name, description, strengths, weaknesses
   - Market share and funding information if available

2. **Estimate market size**
   - TAM (Total Addressable Market) in USD
   - SAM (Serviceable Addressable Market) in USD  
   - SOM (Serviceable Obtainable Market) in USD
   - Annual growth rate percentage
   - Cite the source of your market data

3. **Identify 5-7 key customer pain points**
   - Specific problems customers face
   - Why existing solutions fall short

4. **Analyze 5-7 current market trends**
   - Emerging opportunities
   - Shifts in customer behavior
   - Technology or regulatory changes

5. **Provide a unique value proposition**
   - One clear sentence on how this idea uniquely solves customer problems

Always search for recent, credible data. Track all sources used.
Focus on actionable insights backed by data.
Be realistic in your assessments - don't overestimate market potential.
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
    
    def _parse_structured_output(self, raw_output: str) -> StructuredMarketResearch:
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
                """Given the following market research output, structure it according to the format instructions.
                
Market Research Output:
{raw_output}

{format_instructions}

Provide realistic estimates based on the research. If specific numbers aren't available, 
make educated estimates based on similar markets and clearly note they are estimates.
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
            return StructuredMarketResearch(
                competitors=[],
                market_size=MarketSize(
                    tam=0,
                    sam=0,
                    som=0,
                    growth_rate=0,
                    source="Unable to determine"
                ),
                customer_pain_points=["Unable to extract pain points from research"],
                unique_value_proposition="Unable to determine from research",
                market_trends=["Unable to extract trends from research"],
                confidence_score=0.1,
                sources=["Research parsing failed"]
            )
    
    def _convert_to_schema_format(self, structured_data: StructuredMarketResearch) -> MarketResearchResult:
        """Convert structured data to the schema format."""
        competitors = []
        for comp in structured_data.competitors:
            competitors.append({
                "name": comp.name,
                "description": comp.description,
                "strengths": comp.strengths,
                "weaknesses": comp.weaknesses,
                "market_share": comp.market_share,
                "funding": comp.funding
            })
        
        market_size = {
            "tam": structured_data.market_size.tam,
            "sam": structured_data.market_size.sam,
            "som": structured_data.market_size.som,
            "growth_rate": structured_data.market_size.growth_rate,
            "source": structured_data.market_size.source
        }
        
        return MarketResearchResult(
            competitors=competitors,
            market_size=market_size,
            customer_pain_points=structured_data.customer_pain_points,
            unique_value_proposition=structured_data.unique_value_proposition,
            market_trends=structured_data.market_trends,
            confidence_score=structured_data.confidence_score
        )
    
    async def research(
        self,
        business_idea: str,
        target_market: str = None,
        industry: str = None,
    ) -> Dict[str, Any]:
        """
        Conduct market research for a business idea.
        
        Args:
            business_idea: The business idea to research
            target_market: Optional target market specification
            industry: Optional industry specification
            
        Returns:
            Market research results
        """
        try:
            # Construct research query
            query = f"Conduct comprehensive market research for: {business_idea}"
            if target_market:
                query += f"\nTarget Market: {target_market}"
            if industry:
                query += f"\nIndustry: {industry}"
            
            query += "\n\nProvide specific numbers, company names, and actionable insights."
            
            # Run the agent
            logger.info(f"Starting market research for: {business_idea}")
            result = await self.agent.ainvoke({"input": query})
            raw_output = result.get("output", "")
            
            # Parse and structure the results
            structured_data = self._parse_structured_output(raw_output)
            
            # Convert to schema format
            market_research_result = self._convert_to_schema_format(structured_data)
            
            # Return as dict for API response
            return {
                "raw_output": raw_output,
                "competitors": market_research_result.competitors,
                "market_size": market_research_result.market_size,
                "customer_pain_points": market_research_result.customer_pain_points,
                "unique_value_proposition": market_research_result.unique_value_proposition,
                "market_trends": market_research_result.market_trends,
                "confidence_score": market_research_result.confidence_score,
                "sources": structured_data.sources
            }
            
        except Exception as e:
            logger.error(f"Market research failed: {str(e)}")
            raise