from typing import Dict, Any
from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from app.services.ai_service import AIService
from app.core.config import settings

router = APIRouter()


class AnalysisRequest(BaseModel):
    asin: str
    analysis_type: str = "comprehensive"  # comprehensive, price, reviews, competition


class InsightRequest(BaseModel):
    data: Dict[str, Any]
    insight_type: str = "trends"  # trends, recommendations, predictions


@router.post("/analyze-product")
async def analyze_product(request: AnalysisRequest):
    """Analyze a product using AI"""
    if not settings.OPENAI_API_KEY and not settings.ANTHROPIC_API_KEY:
        raise HTTPException(
            status_code=503, 
            detail="AI service not configured. Please set API keys."
        )
    
    ai_service = AIService()
    try:
        analysis = await ai_service.analyze_product(
            request.asin, 
            request.analysis_type
        )
        return {"analysis": analysis}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Analysis failed: {str(e)}")


@router.post("/generate-insights")
async def generate_insights(request: InsightRequest):
    """Generate insights from analytics data using AI"""
    if not settings.OPENAI_API_KEY and not settings.ANTHROPIC_API_KEY:
        raise HTTPException(
            status_code=503, 
            detail="AI service not configured. Please set API keys."
        )
    
    ai_service = AIService()
    try:
        insights = await ai_service.generate_insights(
            request.data, 
            request.insight_type
        )
        return {"insights": insights}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Insight generation failed: {str(e)}")


@router.get("/health")
async def ai_health_check():
    """Check AI service availability"""
    has_openai = bool(settings.OPENAI_API_KEY and settings.OPENAI_API_KEY.strip() and not settings.OPENAI_API_KEY.startswith('your_'))
    has_anthropic = bool(settings.ANTHROPIC_API_KEY and settings.ANTHROPIC_API_KEY.strip() and not settings.ANTHROPIC_API_KEY.startswith('your_'))
    
    return {
        "openai_available": has_openai,
        "anthropic_available": has_anthropic,
        "service_ready": has_openai or has_anthropic
    }