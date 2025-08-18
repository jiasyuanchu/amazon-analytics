// API client for Amazon Analytics backend

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

export interface Product {
  id: number;
  asin: string;
  title: string;
  price: number;
  currency: string;
  rating: number;
  review_count: number;
  category: string;
  brand: string;
  availability: boolean;
  image_url?: string;
  product_url?: string;
  description: string;
  features?: any;
  dimensions?: any;
  weight?: number;
  created_at: string;
  updated_at?: string;
}

export interface AnalyticsOverview {
  total_products: number;
  average_price: number;
  total_revenue_30d: number;
  average_rating: number;
}

export interface TrendData {
  date: string;
  value: number;
  metric: string;
}

// Analytics API functions
export async function fetchAnalyticsOverview(): Promise<AnalyticsOverview> {
  const response = await fetch(`${API_BASE_URL}/api/v1/analytics/overview`);
  if (!response.ok) {
    throw new Error('Failed to fetch analytics overview');
  }
  return response.json();
}

export async function fetchAnalyticsTrends(): Promise<TrendData[]> {
  const response = await fetch(`${API_BASE_URL}/api/v1/analytics/trends`);
  if (!response.ok) {
    throw new Error('Failed to fetch analytics trends');
  }
  return response.json();
}

export async function fetchTopProducts(): Promise<Product[]> {
  const response = await fetch(`${API_BASE_URL}/api/v1/analytics/top-products`);
  if (!response.ok) {
    throw new Error('Failed to fetch top products');
  }
  return response.json();
}

// Products API functions
export async function fetchProducts(): Promise<Product[]> {
  const response = await fetch(`${API_BASE_URL}/api/v1/products/`);
  if (!response.ok) {
    throw new Error('Failed to fetch products');
  }
  return response.json();
}

export async function fetchProduct(asin: string): Promise<Product> {
  const response = await fetch(`${API_BASE_URL}/api/v1/products/${asin}`);
  if (!response.ok) {
    throw new Error('Failed to fetch product');
  }
  return response.json();
}

export async function createProduct(product: Partial<Product>): Promise<Product> {
  const response = await fetch(`${API_BASE_URL}/api/v1/products/`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(product),
  });
  if (!response.ok) {
    throw new Error('Failed to create product');
  }
  return response.json();
}

export async function fetchPriceHistory(asin: string): Promise<any[]> {
  const response = await fetch(`${API_BASE_URL}/api/v1/products/${asin}/price-history`);
  if (!response.ok) {
    throw new Error('Failed to fetch price history');
  }
  return response.json();
}

// AI API functions
export async function analyzeProduct(asin: string, analysisType: string = 'comprehensive'): Promise<{ analysis: string }> {
  const response = await fetch(`${API_BASE_URL}/api/v1/ai/analyze-product`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({
      asin,
      analysis_type: analysisType,
    }),
  });
  if (!response.ok) {
    throw new Error('Failed to analyze product');
  }
  return response.json();
}

export async function generateInsights(data: any, insightType: string = 'trends'): Promise<{ insights: string }> {
  const response = await fetch(`${API_BASE_URL}/api/v1/ai/generate-insights`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({
      data,
      insight_type: insightType,
    }),
  });
  if (!response.ok) {
    throw new Error('Failed to generate insights');
  }
  return response.json();
}

export async function checkAIHealth(): Promise<{ openai_available: boolean; anthropic_available: boolean; service_ready: boolean }> {
  const response = await fetch(`${API_BASE_URL}/api/v1/ai/health`);
  if (!response.ok) {
    throw new Error('Failed to check AI health');
  }
  return response.json();
}

// Amazon API functions
export async function searchAmazonProducts(query: string): Promise<{ query: string; total_results: number; products: any[] }> {
  const response = await fetch(`${API_BASE_URL}/api/v1/products/search/amazon?query=${encodeURIComponent(query)}`);
  if (!response.ok) {
    throw new Error('Failed to search Amazon products');
  }
  return response.json();
}

export async function syncProductFromAmazon(asin: string): Promise<Product> {
  const response = await fetch(`${API_BASE_URL}/api/v1/products/sync/${asin}`, {
    method: 'POST',
  });
  if (!response.ok) {
    throw new Error('Failed to sync product from Amazon');
  }
  return response.json();
}

export async function getProductWithAmazonFallback(asin: string): Promise<Product> {
  const response = await fetch(`${API_BASE_URL}/api/v1/products/${asin}/with-amazon-fallback`);
  if (!response.ok) {
    throw new Error('Failed to get product');
  }
  return response.json();
}

export async function getProductReviews(asin: string): Promise<{ total_reviews: number; average_rating: number; reviews: any[] }> {
  const response = await fetch(`${API_BASE_URL}/api/v1/products/${asin}/reviews`);
  if (!response.ok) {
    throw new Error('Failed to get product reviews');
  }
  return response.json();
}