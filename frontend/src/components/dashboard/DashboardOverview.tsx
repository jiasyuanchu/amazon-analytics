'use client'

import { useQuery } from 'react-query'
import { fetchAnalyticsOverview } from '@/lib/api'
import { 
  ShoppingBagIcon, 
  CurrencyDollarIcon, 
  ChartBarIcon,
  StarIcon 
} from '@heroicons/react/24/outline'

export default function DashboardOverview() {
  const { data: overview, isLoading } = useQuery(
    'analyticsOverview',
    fetchAnalyticsOverview
  )

  const stats = [
    {
      name: 'Total Products',
      value: overview?.total_products || 0,
      icon: ShoppingBagIcon,
      change: '+12%',
      changeType: 'positive',
    },
    {
      name: 'Average Price',
      value: `$${overview?.average_price || 0}`,
      icon: CurrencyDollarIcon,
      change: '+4.3%',
      changeType: 'positive',
    },
    {
      name: 'Revenue (30d)',
      value: `$${overview?.total_revenue_30d?.toLocaleString() || 0}`,
      icon: ChartBarIcon,
      change: '+8.2%',
      changeType: 'positive',
    },
    {
      name: 'Avg. Rating',
      value: overview?.average_rating?.toFixed(1) || '0.0',
      icon: StarIcon,
      change: '+0.1',
      changeType: 'positive',
    },
  ]

  if (isLoading) {
    return (
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        {[...Array(4)].map((_, i) => (
          <div key={i} className="card p-6 animate-pulse">
            <div className="h-4 bg-gray-200 rounded w-3/4 mb-2"></div>
            <div className="h-8 bg-gray-200 rounded w-1/2 mb-1"></div>
            <div className="h-3 bg-gray-200 rounded w-1/4"></div>
          </div>
        ))}
      </div>
    )
  }

  return (
    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
      {stats.map((stat) => {
        const IconComponent = stat.icon
        return (
          <div key={stat.name} className="card p-6">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm font-medium text-gray-600">{stat.name}</p>
                <p className="text-2xl font-bold text-gray-900">{stat.value}</p>
              </div>
              <div className="p-3 bg-primary-100 rounded-lg">
                <IconComponent className="h-6 w-6 text-primary-600" />
              </div>
            </div>
            <div className="mt-4 flex items-center">
              <span className="text-sm font-medium text-green-600">
                {stat.change}
              </span>
              <span className="text-sm text-gray-500 ml-2">from last month</span>
            </div>
          </div>
        )
      })}
    </div>
  )
}