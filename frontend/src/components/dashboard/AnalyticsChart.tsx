'use client'

import { useQuery } from 'react-query'
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts'
import { fetchAnalyticsTrends } from '@/lib/api'
import { format, parseISO } from 'date-fns'

export default function AnalyticsChart() {
  const { data: trends, isLoading } = useQuery(
    'analyticsTrends',
    () => fetchAnalyticsTrends()
  )

  const formatDate = (dateStr: string) => {
    return format(parseISO(dateStr), 'MMM dd')
  }

  if (isLoading) {
    return (
      <div className="card p-6">
        <h3 className="text-lg font-semibold text-gray-900 mb-4">Analytics Trends</h3>
        <div className="h-80 bg-gray-100 rounded animate-pulse"></div>
      </div>
    )
  }

  const chartData = trends?.map((item: any) => ({
    date: formatDate(item.date),
    revenue: item.revenue,
    views: item.views,
    conversions: item.conversions,
  })) || []

  return (
    <div className="card p-6">
      <h3 className="text-lg font-semibold text-gray-900 mb-4">Analytics Trends</h3>
      
      <div className="h-80">
        <ResponsiveContainer width="100%" height="100%">
          <LineChart data={chartData}>
            <CartesianGrid strokeDasharray="3 3" />
            <XAxis 
              dataKey="date" 
              tick={{ fontSize: 12 }}
            />
            <YAxis tick={{ fontSize: 12 }} />
            <Tooltip />
            <Legend />
            <Line 
              type="monotone" 
              dataKey="revenue" 
              stroke="#3b82f6" 
              strokeWidth={2}
              name="Revenue ($)"
            />
            <Line 
              type="monotone" 
              dataKey="views" 
              stroke="#10b981" 
              strokeWidth={2}
              name="Views"
            />
            <Line 
              type="monotone" 
              dataKey="conversions" 
              stroke="#f59e0b" 
              strokeWidth={2}
              name="Conversions"
            />
          </LineChart>
        </ResponsiveContainer>
      </div>
    </div>
  )
}