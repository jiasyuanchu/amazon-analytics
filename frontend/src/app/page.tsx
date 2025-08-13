import DashboardOverview from '@/components/dashboard/DashboardOverview'
import TopProducts from '@/components/dashboard/TopProducts'
import AnalyticsChart from '@/components/dashboard/AnalyticsChart'

export default function Home() {
  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-3xl font-bold text-gray-900">Dashboard</h1>
        <p className="text-gray-600 mt-1">
          Welcome to your Amazon Analytics Dashboard
        </p>
      </div>
      
      <DashboardOverview />
      
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <AnalyticsChart />
        <TopProducts />
      </div>
    </div>
  )
}