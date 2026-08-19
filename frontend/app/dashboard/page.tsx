export default function DashboardPage() {
  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-3xl font-bold">Dashboard</h1>
        <p className="text-muted mt-2">Overview of your business performance</p>
      </div>

      {/* Stats Grid */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
        <div className="bg-card rounded-lg p-6 border border-border">
          <p className="text-muted text-sm mb-2">Total Calls (Today)</p>
          <p className="text-3xl font-bold">24</p>
          <p className="text-xs text-success mt-2">↑ 12% from yesterday</p>
        </div>
        <div className="bg-card rounded-lg p-6 border border-border">
          <p className="text-muted text-sm mb-2">Avg. Call Duration</p>
          <p className="text-3xl font-bold">3m 45s</p>
          <p className="text-xs text-muted mt-2">Average</p>
        </div>
        <div className="bg-card rounded-lg p-6 border border-border">
          <p className="text-muted text-sm mb-2">Appointments Booked</p>
          <p className="text-3xl font-bold">12</p>
          <p className="text-xs text-success mt-2">From calls today</p>
        </div>
        <div className="bg-card rounded-lg p-6 border border-border">
          <p className="text-muted text-sm mb-2">Customer Sentiment</p>
          <p className="text-3xl font-bold">92%</p>
          <p className="text-xs text-success mt-2">Positive feedback</p>
        </div>
      </div>

      {/* Charts and Details */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-4">
        <div className="bg-card rounded-lg p-6 border border-border">
          <h3 className="text-lg font-semibold mb-4">Call Distribution</h3>
          <div className="h-64 flex items-center justify-center text-muted">
            [Chart will be displayed here]
          </div>
        </div>
        <div className="bg-card rounded-lg p-6 border border-border">
          <h3 className="text-lg font-semibold mb-4">Busiest Hours</h3>
          <div className="h-64 flex items-center justify-center text-muted">
            [Chart will be displayed here]
          </div>
        </div>
      </div>
    </div>
  );
}
