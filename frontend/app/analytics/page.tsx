export default function AnalyticsPage() {
  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-3xl font-bold">Analytics</h1>
        <p className="text-muted mt-2">Performance metrics and insights</p>
      </div>

      {/* Date Range Selector */}
      <div className="flex gap-4">
        <select className="px-4 py-2 rounded-lg bg-card border border-border text-foreground">
          <option>Last 7 days</option>
          <option>Last 30 days</option>
          <option>Last 90 days</option>
          <option>Last year</option>
        </select>
      </div>

      {/* KPI Cards */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
        <div className="bg-card rounded-lg p-6 border border-border">
          <p className="text-muted text-sm mb-2">Total Calls</p>
          <p className="text-3xl font-bold">256</p>
          <p className="text-xs text-success mt-2">↑ 15% vs last period</p>
        </div>
        <div className="bg-card rounded-lg p-6 border border-border">
          <p className="text-muted text-sm mb-2">Appointments Booked</p>
          <p className="text-3xl font-bold">87</p>
          <p className="text-xs text-success mt-2">34% conversion rate</p>
        </div>
        <div className="bg-card rounded-lg p-6 border border-border">
          <p className="text-muted text-sm mb-2">Avg Call Duration</p>
          <p className="text-3xl font-bold">4m 12s</p>
          <p className="text-xs text-muted mt-2">Professional</p>
        </div>
        <div className="bg-card rounded-lg p-6 border border-border">
          <p className="text-muted text-sm mb-2">Customer Satisfaction</p>
          <p className="text-3xl font-bold">9.2/10</p>
          <p className="text-xs text-success mt-2">Based on 156 responses</p>
        </div>
      </div>

      {/* Charts */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-4">
        <div className="bg-card rounded-lg p-6 border border-border">
          <h3 className="text-lg font-semibold mb-4">Calls by Day</h3>
          <div className="h-64 flex items-center justify-center text-muted">
            [Line chart showing call trends]
          </div>
        </div>
        <div className="bg-card rounded-lg p-6 border border-border">
          <h3 className="text-lg font-semibold mb-4">Call Intent Distribution</h3>
          <div className="h-64 flex items-center justify-center text-muted">
            [Pie chart showing booking vs inquiries]
          </div>
        </div>
      </div>

      {/* More charts */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-4">
        <div className="bg-card rounded-lg p-6 border border-border">
          <h3 className="text-lg font-semibold mb-4">Sentiment Analysis</h3>
          <div className="space-y-4">
            <div>
              <div className="flex justify-between mb-2">
                <span className="text-sm">Positive</span>
                <span className="text-sm font-semibold">88%</span>
              </div>
              <div className="w-full bg-card-foreground/10 rounded-full h-2">
                <div className="bg-success h-2 rounded-full" style={{width: '88%'}}></div>
              </div>
            </div>
            <div>
              <div className="flex justify-between mb-2">
                <span className="text-sm">Neutral</span>
                <span className="text-sm font-semibold">10%</span>
              </div>
              <div className="w-full bg-card-foreground/10 rounded-full h-2">
                <div className="bg-warning h-2 rounded-full" style={{width: '10%'}}></div>
              </div>
            </div>
            <div>
              <div className="flex justify-between mb-2">
                <span className="text-sm">Negative</span>
                <span className="text-sm font-semibold">2%</span>
              </div>
              <div className="w-full bg-card-foreground/10 rounded-full h-2">
                <div className="bg-destructive h-2 rounded-full" style={{width: '2%'}}></div>
              </div>
            </div>
          </div>
        </div>
        <div className="bg-card rounded-lg p-6 border border-border">
          <h3 className="text-lg font-semibold mb-4">Peak Hours</h3>
          <div className="space-y-3">
            <p className="text-sm">
              <span className="font-semibold">Busiest Time:</span> <span className="text-muted">10:00 AM - 11:00 AM</span>
            </p>
            <p className="text-sm">
              <span className="font-semibold">Quietest Time:</span> <span className="text-muted">6:00 PM - 7:00 PM</span>
            </p>
            <p className="text-sm">
              <span className="font-semibold">Avg Calls/Hour:</span> <span className="text-muted">12</span>
            </p>
            <p className="text-sm">
              <span className="font-semibold">Peak Time Calls:</span> <span className="text-muted">34</span>
            </p>
          </div>
        </div>
      </div>
    </div>
  );
}
