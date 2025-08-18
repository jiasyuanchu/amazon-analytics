import json
import asyncio
from typing import Dict, Any, Optional, List
import requests
from datetime import datetime
from app.core.config import settings


class AmazonDataService:
    """Service for fetching real Amazon product data using Rainforest API"""
    
    def __init__(self):
        # Only consider valid API keys (not placeholder values)
        self.api_key = (
            settings.RAINFOREST_API_KEY 
            if settings.RAINFOREST_API_KEY and settings.RAINFOREST_API_KEY.strip() and not settings.RAINFOREST_API_KEY.startswith('your_')
            else None
        )
        self.base_url = "https://api.rainforestapi.com/request"
        self.marketplace = settings.AMAZON_MARKETPLACE
        
    async def search_products(self, query: str, pages: int = 1) -> List[Dict[str, Any]]:
        """Search for products on Amazon"""
        if not self.api_key:
            return []
        
        try:
            params = {
                'api_key': self.api_key,
                'type': 'search',
                'amazon_domain': f'amazon.{"com" if self.marketplace == "US" else "co.uk"}',
                'search_term': query,
                'page': '1'
            }
            
            response = requests.get(self.base_url, params=params, timeout=30)
            response.raise_for_status()
            
            data = response.json()
            search_results = data.get('search_results', [])
            
            # Convert to our format
            products = []
            for item in search_results[:10]:  # Limit to first 10 results
                product = self._convert_search_result_to_product(item)
                if product:
                    products.append(product)
            
            return products
            
        except Exception as e:
            print(f"Error fetching search results: {e}")
            return []
    
    async def get_product_details(self, asin: str) -> Optional[Dict[str, Any]]:
        """Get detailed product information by ASIN"""
        if not self.api_key:
            return None
        
        try:
            params = {
                'api_key': self.api_key,
                'type': 'product',
                'amazon_domain': f'amazon.{"com" if self.marketplace == "US" else "co.uk"}',
                'asin': asin
            }
            
            response = requests.get(self.base_url, params=params, timeout=30)
            response.raise_for_status()
            
            data = response.json()
            product_data = data.get('product', {})
            
            if not product_data:
                return None
                
            return self._convert_product_data_to_our_format(product_data)
            
        except Exception as e:
            print(f"Error fetching product details for {asin}: {e}")
            return None
    
    async def get_product_reviews(self, asin: str, pages: int = 1) -> Dict[str, Any]:
        """Get product reviews and ratings"""
        if not self.api_key:
            return {
                'total_reviews': 0,
                'average_rating': 0.0,
                'reviews': []
            }
        
        try:
            params = {
                'api_key': self.api_key,
                'type': 'reviews',
                'amazon_domain': f'amazon.{"com" if self.marketplace == "US" else "co.uk"}',
                'asin': asin,
                'page': '1'
            }
            
            response = requests.get(self.base_url, params=params, timeout=30)
            response.raise_for_status()
            
            data = response.json()
            reviews = data.get('reviews', [])
            
            # Process reviews
            total_reviews = len(reviews)
            avg_rating = sum([r.get('rating', 0) for r in reviews]) / max(total_reviews, 1)
            
            return {
                'total_reviews': total_reviews,
                'average_rating': round(avg_rating, 1),
                'reviews': reviews[:5]  # Return first 5 reviews
            }
            
        except Exception as e:
            print(f"Error fetching reviews for {asin}: {e}")
            return {
                'total_reviews': 0,
                'average_rating': 0.0,
                'reviews': []
            }
    
    def _convert_search_result_to_product(self, item: Dict) -> Optional[Dict[str, Any]]:
        """Convert Rainforest API search result to our product format"""
        try:
            price = 0.0
            price_str = item.get('price', {}).get('value')
            if price_str:
                # Remove currency symbols and convert to float
                price_clean = ''.join(filter(lambda x: x.isdigit() or x == '.', str(price_str)))
                price = float(price_clean) if price_clean else 0.0
            
            return {
                'asin': item.get('asin', ''),
                'title': item.get('title', ''),
                'price': price,
                'currency': 'USD',
                'rating': float(item.get('rating', 0)),
                'review_count': int(item.get('ratings_total', 0)),
                'category': item.get('department', ''),
                'brand': item.get('brand', ''),
                'availability': item.get('is_prime', True),
                'image_url': item.get('image', ''),
                'product_url': item.get('link', ''),
                'description': item.get('title', '')[:500],  # Use title as short description
                'features': None,
                'dimensions': None,
                'weight': None
            }
        except Exception as e:
            print(f"Error converting search result: {e}")
            return None
    
    def _convert_product_data_to_our_format(self, product: Dict) -> Dict[str, Any]:
        """Convert Rainforest API product data to our format"""
        try:
            price = 0.0
            price_data = product.get('buybox_winner', {}).get('price', {})
            if price_data and 'value' in price_data:
                price_str = str(price_data['value'])
                price_clean = ''.join(filter(lambda x: x.isdigit() or x == '.', price_str))
                price = float(price_clean) if price_clean else 0.0
            
            # Extract numeric weight from weight string
            weight = 0.0
            weight_str = product.get('weight', '')
            if weight_str:
                weight_numbers = ''.join(filter(lambda x: x.isdigit() or x == '.', str(weight_str)))
                weight = float(weight_numbers) if weight_numbers else 0.0
            
            return {
                'asin': product.get('asin', ''),
                'title': product.get('title', ''),
                'price': price,
                'currency': 'USD',
                'rating': float(product.get('rating', 0)),
                'review_count': int(product.get('ratings_total', 0)),
                'category': product.get('category', {}).get('name', ''),
                'brand': product.get('brand', ''),
                'availability': product.get('availability', {}).get('raw', '') != 'Currently unavailable',
                'image_url': product.get('main_image', {}).get('link', ''),
                'product_url': product.get('link', ''),
                'description': product.get('description', '')[:1000] if product.get('description') else '',
                'features': product.get('feature_bullets', []),
                'dimensions': product.get('dimensions', {}),
                'weight': weight
            }
        except Exception as e:
            print(f"Error converting product data: {e}")
            return {}
    


# Create a singleton instance
amazon_service = AmazonDataService()