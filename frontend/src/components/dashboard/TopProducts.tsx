'use client'

import { useQuery } from 'react-query'
import { fetchTopProducts } from '@/lib/api'
import { StarIcon } from '@heroicons/react/24/solid'

export default function TopProducts() {
  const { data: topProducts, isLoading } = useQuery(
    'topProducts',
    () => fetchTopProducts('revenue', 10)
  )

  if (isLoading) {
    return (
      <div className="card p-6">
        <h3 className="text-lg font-semibold text-gray-900 mb-4">Top Products</h3>
        <div className="space-y-4">
          {[...Array(5)].map((_, i) => (
            <div key={i} className="flex items-center space-x-3 animate-pulse">
              <div className="w-12 h-12 bg-gray-200 rounded"></div>
              <div className="flex-1">
                <div className="h-4 bg-gray-200 rounded w-3/4 mb-1"></div>
                <div className="h-3 bg-gray-200 rounded w-1/2"></div>
              </div>
              <div className="h-6 bg-gray-200 rounded w-16"></div>
            </div>
          ))}
        </div>
      </div>
    )
  }

  return (
    <div className="card p-6">
      <div className="flex items-center justify-between mb-4">
        <h3 className="text-lg font-semibold text-gray-900">Top Products</h3>
        <select className="text-sm border border-gray-300 rounded-md px-2 py-1">
          <option value="revenue">By Revenue</option>
          <option value="views">By Views</option>
          <option value="conversions">By Conversions</option>
        </select>
      </div>
      
      <div className="space-y-4">
        {topProducts?.map((product: any, index: number) => (
          <div key={product.asin} className="flex items-center space-x-3">
            <div className="flex-shrink-0 w-8 h-8 bg-primary-100 rounded-full flex items-center justify-center">
              <span className="text-sm font-medium text-primary-600">
                {index + 1}
              </span>
            </div>
            
            <div className="flex-1 min-w-0">
              <p className="text-sm font-medium text-gray-900 truncate">
                {product.title}
              </p>
              <div className="flex items-center space-x-2">
                <span className="text-sm text-gray-500">
                  ${product.price}
                </span>
                {product.rating && (
                  <div className="flex items-center">
                    <StarIcon className="h-4 w-4 text-yellow-400" />
                    <span className="text-sm text-gray-600 ml-1">
                      {product.rating}
                    </span>
                  </div>
                )}
              </div>
            </div>
            
            <div className="flex-shrink-0">
              <span className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-green-100 text-green-800">
                ${product.metric_value?.toLocaleString()}
              </span>
            </div>
          </div>
        ))}
      </div>
    </div>
  )
}