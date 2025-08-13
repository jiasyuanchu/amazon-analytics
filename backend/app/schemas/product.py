from pydantic import BaseModel
from typing import Optional, Dict, Any
from datetime import datetime


class ProductBase(BaseModel):
    asin: str
    title: str
    price: Optional[float] = None
    currency: str = "USD"
    rating: Optional[float] = None
    review_count: int = 0
    category: Optional[str] = None
    brand: Optional[str] = None
    availability: bool = True
    image_url: Optional[str] = None
    product_url: Optional[str] = None
    description: Optional[str] = None
    features: Optional[Dict[str, Any]] = None
    dimensions: Optional[Dict[str, Any]] = None
    weight: Optional[float] = None


class ProductCreate(ProductBase):
    pass


class ProductResponse(ProductBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class PriceHistoryBase(BaseModel):
    asin: str
    price: float
    currency: str = "USD"


class PriceHistoryResponse(PriceHistoryBase):
    id: int
    timestamp: datetime

    class Config:
        from_attributes = True