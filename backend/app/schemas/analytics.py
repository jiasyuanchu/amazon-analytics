from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class AnalyticsBase(BaseModel):
    asin: str
    views: int = 0
    conversions: int = 0
    revenue: float = 0.0
    bounce_rate: float = 0.0
    avg_session_duration: float = 0.0


class AnalyticsResponse(AnalyticsBase):
    id: int
    date: datetime

    class Config:
        from_attributes = True


class TopProductsResponse(BaseModel):
    asin: str
    title: str
    price: Optional[float]
    rating: Optional[float]
    metric_value: float

    class Config:
        from_attributes = True