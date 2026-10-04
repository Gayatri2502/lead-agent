'use client';

import { StatCard } from '@/components/ui/patterns/StatCard';
import { ChartWrapper, LineChart, BarChart } from '@/components/ui/charts';
import { Card, CardContent } from '@/components/ui/composite/Card';
import { useAnalyticsOverview } from '@/services/queries';
import { Phone, Calendar, Users, Smile, Clock, TrendingUp } from 'lucide-react';

export default function DashboardPage() {
  const { data: analytics, isLoading } = useAnalyticsOverview(1);

  const stats = [
    {
      label: 'Total Calls (Today)',
      value: analytics?.calls_today || 0,
      change: { value: 12, label: 'from yesterday', trend: 'up' as const },
      icon: <Phone className="h-5 w-5" />,
      iconBg: 'primary' as const,
    },
    {
      label: 'Avg. Call Duration',
      value: analytics?.avg_duration ? `${Math.floor(analytics.avg_duration / 60)}m ${analytics.avg_duration % 60}s` : '0m 0s',
      icon: <Clock className="h-5 w-5" />,
      iconBg: 'success' as const,
    },
    {
      label: 'Appointments Booked',
      value: analytics?.appointments_booked || 0,
      change: { value: 8, label: 'from calls today', trend: 'up' as const },
      icon: <Calendar className="h-5 w-5" />,
      iconBg: 'warning' as const,
    },
    {
      label: 'Customer Sentiment',
      value: analytics?.sentiment_score ? `${analytics.sentiment_score}%` : '0%',
      change: { value: 3, label: 'positive feedback', trend: 'up' as const },
      icon: <Smile className="h-5 w-5" />,
      iconBg: 'success' as const,
    },
  ];

  // Mock chart data for demo
  const callDistributionData = [
    { x: 0, y: 45 },
    { x: 1, y: 52 },
    { x: 2, y: 38 },
    { x: 3, y: 61 },
    { x: 4, y: 55 },
    { x: 5, y: 22 },
    { x: 6, y: 18 },
  ];

  const busiestHoursData = [
    { x: 9, y: 12 },
    { x: 10, y: 28 },
    { x: 11, y: 35 },
    { x: 12, y: 22 },
    { x: 13, y: 18 },
    { x: 14, y: 31 },
    { x: 15, y: 25 },
    { x: 16, y: 19 },
    { x: 17, y: 14 },
  ];

  return (
    <div className="space-y-6 animate-in fade-in-0 zoom-in-95">
      <div>
        <h1 className="text-h2 font-semibold tracking-tight">Dashboard</h1>
        <p className="text-muted-foreground mt-1">Overview of your business performance</p>
      </div>

      {/* Stats Grid */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
        {stats.map((stat, index) => (
          <StatCard key={index} {...stat} loading={isLoading} />
        ))}
      </div>

      {/* Charts */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-4">
        <ChartWrapper title="Call Distribution" description="Calls per day this week" height={300}>
          <LineChart data={callDistributionData} color="primary" height={300} showGrid />
        </ChartWrapper>
        <ChartWrapper title="Busiest Hours" description="Call volume by hour" height={300}>
          <BarChart data={busiestHoursData} color="success" height={300} showGrid />
        </ChartWrapper>
      </div>

      {/* Quick Stats Cards */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
        <Card>
          <CardContent className="p-6">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-label text-muted-foreground">Missed Calls</p>
                <p className="text-data-lg font-semibold">{analytics?.missed_calls || 0}</p>
              </div>
              <div className="w-12 h-12 rounded-lg bg-destructive/20 flex items-center justify-center">
                <Phone className="h-6 w-6 text-destructive" />
              </div>
            </div>
          </CardContent>
        </Card>
        <Card>
          <CardContent className="p-6">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-label text-muted-foreground">Conversion Rate</p>
                <p className="text-data-lg font-semibold">{analytics?.conversion_rate || 0}%</p>
              </div>
              <div className="w-12 h-12 rounded-lg bg-primary/20 flex items-center justify-center">
                <TrendingUp className="h-6 w-6 text-primary" />
              </div>
            </div>
          </CardContent>
        </Card>
        <Card>
          <CardContent className="p-6">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-label text-muted-foreground">Peak Hour</p>
                <p className="text-data-lg font-semibold">2 PM</p>
              </div>
              <div className="w-12 h-12 rounded-lg bg-warning/20 flex items-center justify-center">
                <Clock className="h-6 w-6 text-warning" />
              </div>
            </div>
          </CardContent>
        </Card>
        <Card>
          <CardContent className="p-6">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-label text-muted-foreground">Active Users</p>
                <p className="text-data-lg font-semibold">12</p>
              </div>
              <div className="w-12 h-12 rounded-lg bg-success/20 flex items-center justify-center">
                <Users className="h-6 w-6 text-success" />
              </div>
            </div>
          </CardContent>
        </Card>
      </div>
    </div>
  );
}