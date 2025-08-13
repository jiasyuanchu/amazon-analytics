export interface Product {
  id: number
  asin: string
  title: string
  price?: number
  currency: string
  rating?: number
  review_count: number
  category?: string
  brand?: string
  availability: boolean
  image_url?: string
  product_url?: string
  description?: string
  features?: Record<string, any>
  dimensions?: Record<string, any>
  weight?: number
  created_at: string
  updated_at?: string
}

export interface PriceHistory {
  id: number
  asin: string
  price: number
  currency: string
  timestamp: string
}

export interface ProductAnalytics {
  id: number
  asin: string
  views: number
  conversions: number
  revenue: number
  bounce_rate: number
  avg_session_duration: number
  date: string
}

export interface AnalyticsOverview {
  total_products: number
  average_price: number
  total_revenue_30d: number
  average_rating: number
}

export interface AnalyticsTrend {
  date: string
  revenue: number
  views: number
  conversions: number
}

export interface TopProduct {
  asin: string
  title: string
  price?: number
  rating?: number
  metric_value: number
}

export interface AIAnalysis {
  analysis: string
}

export interface AIInsight {
  insights: string
}

export interface AIHealth {
  openai_available: boolean
  anthropic_available: boolean
  service_ready: boolean
}