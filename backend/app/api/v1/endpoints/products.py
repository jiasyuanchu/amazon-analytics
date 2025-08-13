from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.db.database import get_db
from app.models.product import Product, PriceHistory
from app.schemas.product import ProductResponse, ProductCreate, PriceHistoryResponse

router = APIRouter()


@router.get("/", response_model=List[ProductResponse])
async def get_products(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    category: Optional[str] = None,
    db: AsyncSession = Depends(get_db)
):
    """Get all products with optional filtering"""
    query = select(Product)
    
    if category:
        query = query.where(Product.category == category)
    
    query = query.offset(skip).limit(limit)
    result = await db.execute(query)
    products = result.scalars().all()
    
    return products


@router.get("/{asin}", response_model=ProductResponse)
async def get_product(asin: str, db: AsyncSession = Depends(get_db)):
    """Get a specific product by ASIN"""
    result = await db.execute(select(Product).where(Product.asin == asin))
    product = result.scalar_one_or_none()
    
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    
    return product


@router.post("/", response_model=ProductResponse)
async def create_product(product: ProductCreate, db: AsyncSession = Depends(get_db)):
    """Create a new product"""
    db_product = Product(**product.model_dump())
    db.add(db_product)
    await db.commit()
    await db.refresh(db_product)
    return db_product


@router.get("/{asin}/price-history", response_model=List[PriceHistoryResponse])
async def get_price_history(asin: str, db: AsyncSession = Depends(get_db)):
    """Get price history for a product"""
    result = await db.execute(
        select(PriceHistory)
        .where(PriceHistory.asin == asin)
        .order_by(PriceHistory.timestamp.desc())
        .limit(100)
    )
    price_history = result.scalars().all()
    
    return price_history