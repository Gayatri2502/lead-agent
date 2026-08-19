export default function Home() {
  return (
    <div className="space-y-8">
      {/* Welcome Banner */}
      <div className="bg-gradient-to-r from-primary to-blue-600 rounded-lg p-8 text-white">
        <h1 className="text-3xl font-bold mb-2">Welcome to AI Voice Receptionist</h1>
        <p className="text-lg opacity-90">
          Manage appointments, track calls, and analyze customer interactions with AI-powered insights
        </p>
      </div>

      {/* Dashboard Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
        {/* Card: Total Calls */}
        <div className="bg-card rounded-lg p-6 border border-border">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-muted text-sm mb-1">Today's Calls</p>
              <p className="text-3xl font-bold">24</p>
            </div>
            <div className="w-12 h-12 rounded-lg bg-primary/20 flex items-center justify-center">
              <span className="text-2xl">📞</span>
            </div>
          </div>
        </div>

        {/* Card: Appointments */}
        <div className="bg-card rounded-lg p-6 border border-border">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-muted text-sm mb-1">Appointments</p>
              <p className="text-3xl font-bold">12</p>
            </div>
            <div className="w-12 h-12 rounded-lg bg-success/20 flex items-center justify-center">
              <span className="text-2xl">📅</span>
            </div>
          </div>
        </div>

        {/* Card: Customers */}
        <div className="bg-card rounded-lg p-6 border border-border">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-muted text-sm mb-1">New Customers</p>
              <p className="text-3xl font-bold">5</p>
            </div>
            <div className="w-12 h-12 rounded-lg bg-warning/20 flex items-center justify-center">
              <span className="text-2xl">👥</span>
            </div>
          </div>
        </div>

        {/* Card: Satisfaction */}
        <div className="bg-card rounded-lg p-6 border border-border">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-muted text-sm mb-1">Satisfaction</p>
              <p className="text-3xl font-bold">94%</p>
            </div>
            <div className="w-12 h-12 rounded-lg bg-destructive/20 flex items-center justify-center">
              <span className="text-2xl">😊</span>
            </div>
          </div>
        </div>
      </div>

      {/* Recent Activity */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-4">
        {/* Recent Calls */}
        <div className="lg:col-span-2 bg-card rounded-lg p-6 border border-border">
          <h3 className="text-lg font-semibold mb-4">Recent Calls</h3>
          <div className="space-y-3">
            {[1, 2, 3, 4, 5].map((i) => (
              <div key={i} className="flex items-center justify-between py-3 border-b border-border last:border-b-0">
                <div className="flex items-center gap-3">
                  <div className="w-10 h-10 rounded-full bg-primary/20 flex items-center justify-center">
                    <span className="text-sm">📞</span>
                  </div>
                  <div>
                    <p className="font-medium">Customer {i}</p>
                    <p className="text-sm text-muted">2 hours ago</p>
                  </div>
                </div>
                <div className="text-right">
                  <p className="text-sm font-medium">Booking</p>
                  <p className="text-xs text-success">Completed</p>
                </div>
              </div>
            ))}
          </div>
        </div>

        {/* Quick Actions */}
        <div className="bg-card rounded-lg p-6 border border-border">
          <h3 className="text-lg font-semibold mb-4">Quick Actions</h3>
          <div className="space-y-3">
            <button className="w-full px-4 py-3 rounded-lg bg-primary/10 text-primary hover:bg-primary/20 transition text-sm font-medium">
              Schedule Appointment
            </button>
            <button className="w-full px-4 py-3 rounded-lg border border-border hover:bg-card-foreground/5 transition text-sm font-medium">
              View Call Recordings
            </button>
            <button className="w-full px-4 py-3 rounded-lg border border-border hover:bg-card-foreground/5 transition text-sm font-medium">
              Export Analytics
            </button>
            <button className="w-full px-4 py-3 rounded-lg border border-border hover:bg-card-foreground/5 transition text-sm font-medium">
              Manage Team
            </button>
          </div>
        </div>
      </div>
    </div>
  );
}
