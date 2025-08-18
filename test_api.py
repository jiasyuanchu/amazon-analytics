#!/usr/bin/env python3
import os
import sys
import asyncio
sys.path.append('./backend')

# Load environment variables
from dotenv import load_dotenv
load_dotenv()

from backend.app.services.amazon_service import amazon_service

async def test_api():
    print('Testing Amazon API connection...')
    print(f'API Key configured: {amazon_service.api_key[:10]}...' if amazon_service.api_key else 'No API key')
    print(f'Marketplace: {amazon_service.marketplace}')
    
    # Test search functionality
    print('\nTesting product search...')
    results = await amazon_service.search_products('laptop', 1)
    print(f'Found {len(results)} products')
    
    if results:
        product = results[0]
        print(f'\nFirst product:')
        print(f'- Title: {product.get("title", "N/A")[:50]}...')
        print(f'- ASIN: {product.get("asin", "N/A")}')
        print(f'- Price: ${product.get("price", 0)}')
        print(f'- Rating: {product.get("rating", 0)}/5')
        print(f'- Review Count: {product.get("review_count", 0)}')
        
        # Test detailed product info
        asin = product.get('asin')
        if asin:
            print(f'\nTesting product details for ASIN: {asin}')
            details = await amazon_service.get_product_details(asin)
            if details:
                print('✅ Product details retrieved successfully')
                print(f'- Description length: {len(details.get("description", ""))} chars')
                print(f'- Features: {len(details.get("features", []))} items')
            else:
                print('❌ Failed to get product details')
                
            # Test reviews
            print(f'\nTesting product reviews for ASIN: {asin}')
            review_data = await amazon_service.get_product_reviews(asin)
            print(f'- Total reviews: {review_data.get("total_reviews", 0)}')
            print(f'- Average rating: {review_data.get("average_rating", 0)}/5')
            print(f'- Sample reviews: {len(review_data.get("reviews", []))}')
    else:
        print('❌ No products found in search')

if __name__ == "__main__":
    asyncio.run(test_api())