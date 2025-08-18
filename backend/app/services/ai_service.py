import json
from typing import Dict, Any, Optional
import httpx
from app.core.config import settings


class AIService:
    def __init__(self):
        # Only consider valid API keys (not placeholder values)
        self.openai_api_key = (
            settings.OPENAI_API_KEY 
            if settings.OPENAI_API_KEY and settings.OPENAI_API_KEY.strip() and not settings.OPENAI_API_KEY.startswith('your_')
            else None
        )
        self.anthropic_api_key = (
            settings.ANTHROPIC_API_KEY 
            if settings.ANTHROPIC_API_KEY and settings.ANTHROPIC_API_KEY.strip() and not settings.ANTHROPIC_API_KEY.startswith('your_')
            else None
        )

    async def analyze_product(self, asin: str, analysis_type: str = "comprehensive") -> str:
        """Analyze a product using AI"""
        
        prompt = self._get_analysis_prompt(asin, analysis_type)
        
        if self.openai_api_key:
            return await self._call_openai(prompt)
        elif self.anthropic_api_key:
            return await self._call_anthropic(prompt)
        else:
            return "AI analysis not available - please configure OpenAI or Anthropic API key"

    async def generate_insights(self, data: Dict[str, Any], insight_type: str = "trends") -> str:
        """Generate insights from analytics data"""
        
        prompt = self._get_insights_prompt(data, insight_type)
        
        if self.openai_api_key:
            return await self._call_openai(prompt)
        elif self.anthropic_api_key:
            return await self._call_anthropic(prompt)
        else:
            return "AI insights not available - please configure OpenAI or Anthropic API key"

    def _get_analysis_prompt(self, asin: str, analysis_type: str) -> str:
        """Generate analysis prompt"""
        prompts = {
            "comprehensive": f"Provide a comprehensive analysis of Amazon product {asin}, including market position, pricing strategy, customer sentiment, and competitive landscape.",
            "price": f"Analyze the pricing strategy and price competitiveness of Amazon product {asin}.",
            "reviews": f"Analyze customer reviews and sentiment for Amazon product {asin}.",
            "competition": f"Analyze the competitive landscape for Amazon product {asin}."
        }
        return prompts.get(analysis_type, prompts["comprehensive"])

    def _get_insights_prompt(self, data: Dict[str, Any], insight_type: str) -> str:
        """Generate insights prompt"""
        data_str = json.dumps(data, indent=2)
        prompts = {
            "trends": f"Analyze the following analytics data and provide insights on trends:\n{data_str}",
            "recommendations": f"Based on the following data, provide actionable recommendations:\n{data_str}",
            "predictions": f"Based on the following data, provide predictions for future performance:\n{data_str}"
        }
        return prompts.get(insight_type, prompts["trends"])

    async def _call_openai(self, prompt: str) -> str:
        """Call OpenAI API"""
        # TODO: Implement actual OpenAI API integration
        # For now, return placeholder message
        return "OpenAI integration not implemented yet. Please configure the actual OpenAI client."

    async def _call_anthropic(self, prompt: str) -> str:
        """Call Anthropic API"""
        # TODO: Implement actual Anthropic API integration  
        # For now, return placeholder message
        return "Anthropic integration not implemented yet. Please configure the actual Anthropic client."

