from typing import List, Optional
from datetime import datetime, timedelta
from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from app.db.database import get_db
from app.models.product import Product, ProductAnalytics
from app.schemas.analytics import AnalyticsResponse, TopProductsResponse

router = APIRouter()


@router.get("/overview")
async def get_analytics_overview(db: AsyncSession = Depends(get_db)):
    """Get analytics overview with key metrics"""
    
    # Total products
    total_products_result = await db.execute(select(func.count(Product.id)))
    total_products = total_products_result.scalar()
    
    # Average price
    avg_price_result = await db.execute(select(func.avg(Product.price)))
    avg_price = avg_price_result.scalar() or 0
    
    # Total revenue (last 30 days)
    thirty_days_ago = datetime.utcnow() - timedelta(days=30)
    revenue_result = await db.execute(
        select(func.sum(ProductAnalytics.revenue))
        .where(ProductAnalytics.date >= thirty_days_ago)
    )
    total_revenue = revenue_result.scalar() or 0
    
    # Average rating
    avg_rating_result = await db.execute(select(func.avg(Product.rating)))
    avg_rating = avg_rating_result.scalar() or 0
    
    return {
        "total_products": total_products,
        "average_price": round(avg_price, 2),
        "total_revenue_30d": round(total_revenue, 2),
        "average_rating": round(avg_rating, 2)
    }


@router.get("/top-products", response_model=List[TopProductsResponse])
async def get_top_products(
    metric: str = Query("revenue", regex="^(revenue|views|conversions)$"),
    limit: int = Query(10, ge=1, le=50),
    days: int = Query(30, ge=1, le=365),
    db: AsyncSession = Depends(get_db)
):
    """Get top products by specified metric"""
    
    date_filter = datetime.utcnow() - timedelta(days=days)
    
    if metric == "revenue":
        order_by = func.sum(ProductAnalytics.revenue).desc()
        metric_sum = func.sum(ProductAnalytics.revenue)
    elif metric == "views":
        order_by = func.sum(ProductAnalytics.views).desc()
        metric_sum = func.sum(ProductAnalytics.views)
    else:  # conversions
        order_by = func.sum(ProductAnalytics.conversions).desc()
        metric_sum = func.sum(ProductAnalytics.conversions)
    
    query = (
        select(
            Product.asin,
            Product.title,
            Product.price,
            Product.rating,
            metric_sum.label("metric_value")
        )
        .join(ProductAnalytics, Product.asin == ProductAnalytics.asin)
        .where(ProductAnalytics.date >= date_filter)
        .group_by(Product.asin, Product.title, Product.price, Product.rating)
        .order_by(order_by)
        .limit(limit)
    )
    
    result = await db.execute(query)
    top_products = result.all()
    
    return [
        {
            "asin": row.asin,
            "title": row.title,
            "price": row.price,
            "rating": row.rating,
            "metric_value": row.metric_value or 0
        }
        for row in top_products
    ]


@router.get("/trends")
async def get_analytics_trends(
    days: int = Query(30, ge=7, le=365),
    db: AsyncSession = Depends(get_db)
):
    """Get analytics trends over time"""
    
    date_filter = datetime.utcnow() - timedelta(days=days)
    
    query = (
        select(
            func.date(ProductAnalytics.date).label("date"),
            func.sum(ProductAnalytics.revenue).label("revenue"),
            func.sum(ProductAnalytics.views).label("views"),
            func.sum(ProductAnalytics.conversions).label("conversions")
        )
        .where(ProductAnalytics.date >= date_filter)
        .group_by(func.date(ProductAnalytics.date))
        .order_by(func.date(ProductAnalytics.date))
    )
    
    result = await db.execute(query)
    trends = result.all()
    
    return [
        {
            "date": row.date,
            "revenue": row.revenue or 0,
            "views": row.views or 0,
            "conversions": row.conversions or 0
        }
        for row in trends
    ]