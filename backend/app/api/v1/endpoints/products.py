from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from datetime import datetime
from app.db.database import get_db
from app.models.product import Product, PriceHistory
from app.schemas.product import ProductResponse, ProductCreate, PriceHistoryResponse
from app.services.amazon_service import amazon_service

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


@router.get("/search/amazon")
async def search_amazon_products(
    query: str = Query(..., description="Search term for Amazon products"),
    pages: int = Query(1, ge=1, le=3, description="Number of pages to search")
):
    """Search for products on Amazon using Rainforest API"""
    try:
        products = await amazon_service.search_products(query, pages)
        return {
            "query": query,
            "total_results": len(products),
            "products": products
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to search Amazon: {str(e)}")


@router.post("/sync/{asin}", response_model=ProductResponse)
async def sync_product_from_amazon(asin: str, db: AsyncSession = Depends(get_db)):
    """Sync a product from Amazon and save to local database"""
    try:
        # Get product details from Amazon
        amazon_data = await amazon_service.get_product_details(asin)
        if not amazon_data:
            raise HTTPException(status_code=404, detail="Product not found on Amazon")
        
        # Check if product already exists in our database
        result = await db.execute(select(Product).where(Product.asin == asin))
        existing_product = result.scalar_one_or_none()
        
        if existing_product:
            # Update existing product
            for key, value in amazon_data.items():
                if hasattr(existing_product, key) and value is not None:
                    setattr(existing_product, key, value)
            existing_product.updated_at = datetime.utcnow()
            
            # Add price history entry
            if amazon_data.get('price', 0) > 0:
                price_entry = PriceHistory(
                    asin=asin,
                    price=amazon_data['price'],
                    currency=amazon_data.get('currency', 'USD'),
                    timestamp=datetime.utcnow()
                )
                db.add(price_entry)
            
            await db.commit()
            await db.refresh(existing_product)
            return existing_product
        else:
            # Create new product
            new_product = Product(**amazon_data)
            new_product.created_at = datetime.utcnow()
            new_product.updated_at = datetime.utcnow()
            db.add(new_product)
            
            # Add initial price history entry
            if amazon_data.get('price', 0) > 0:
                price_entry = PriceHistory(
                    asin=asin,
                    price=amazon_data['price'],
                    currency=amazon_data.get('currency', 'USD'),
                    timestamp=datetime.utcnow()
                )
                db.add(price_entry)
            
            await db.commit()
            await db.refresh(new_product)
            return new_product
            
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to sync product: {str(e)}")


@router.get("/{asin}/with-amazon-fallback", response_model=ProductResponse)
async def get_product_with_amazon_fallback(asin: str, db: AsyncSession = Depends(get_db)):
    """Get product from local database, fallback to Amazon if not found"""
    # First try to get from local database
    result = await db.execute(select(Product).where(Product.asin == asin))
    product = result.scalar_one_or_none()
    
    if product:
        return product
    
    # If not found locally, try to fetch from Amazon and sync
    try:
        amazon_data = await amazon_service.get_product_details(asin)
        if not amazon_data:
            raise HTTPException(status_code=404, detail="Product not found locally or on Amazon")
        
        # Create new product from Amazon data
        new_product = Product(**amazon_data)
        new_product.created_at = datetime.utcnow()
        new_product.updated_at = datetime.utcnow()
        db.add(new_product)
        
        # Add initial price history entry
        if amazon_data.get('price', 0) > 0:
            price_entry = PriceHistory(
                asin=asin,
                price=amazon_data['price'],
                currency=amazon_data.get('currency', 'USD'),
                timestamp=datetime.utcnow()
            )
            db.add(price_entry)
        
        await db.commit()
        await db.refresh(new_product)
        return new_product
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch product: {str(e)}")


@router.get("/{asin}/reviews")
async def get_product_reviews(asin: str):
    """Get product reviews from Amazon"""
    try:
        reviews = await amazon_service.get_product_reviews(asin)
        return reviews
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch reviews: {str(e)}")