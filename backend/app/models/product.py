from sqlalchemy import Column, Integer, String, Float, DateTime, Text, Boolean, JSON
from sqlalchemy.sql import func
from app.db.database import Base


class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    asin = Column(String(20), unique=True, index=True, nullable=False)
    title = Column(Text, nullable=False)
    price = Column(Float)
    currency = Column(String(3), default="USD")
    rating = Column(Float)
    review_count = Column(Integer, default=0)
    category = Column(String(255))
    brand = Column(String(255))
    availability = Column(Boolean, default=True)
    image_url = Column(Text)
    product_url = Column(Text)
    description = Column(Text)
    features = Column(JSON)
    dimensions = Column(JSON)
    weight = Column(Float)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())


class PriceHistory(Base):
    __tablename__ = "price_history"

    id = Column(Integer, primary_key=True, index=True)
    asin = Column(String(20), index=True, nullable=False)
    price = Column(Float, nullable=False)
    currency = Column(String(3), default="USD")
    timestamp = Column(DateTime(timezone=True), server_default=func.now(), index=True)


class ProductAnalytics(Base):
    __tablename__ = "product_analytics"

    id = Column(Integer, primary_key=True, index=True)
    asin = Column(String(20), index=True, nullable=False)
    views = Column(Integer, default=0)
    conversions = Column(Integer, default=0)
    revenue = Column(Float, default=0.0)
    bounce_rate = Column(Float, default=0.0)
    avg_session_duration = Column(Float, default=0.0)
    date = Column(DateTime(timezone=True), server_default=func.now(), index=True)