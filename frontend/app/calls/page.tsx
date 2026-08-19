export default function CallsPage() {
  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-3xl font-bold">Call History</h1>
        <p className="text-muted mt-2">Review and analyze incoming and outgoing calls</p>
      </div>

      {/* Stats */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
        <div className="bg-card rounded-lg p-4 border border-border">
          <p className="text-muted text-sm">Total Calls</p>
          <p className="text-2xl font-bold">156</p>
        </div>
        <div className="bg-card rounded-lg p-4 border border-border">
          <p className="text-muted text-sm">This Month</p>
          <p className="text-2xl font-bold">45</p>
        </div>
        <div className="bg-card rounded-lg p-4 border border-border">
          <p className="text-muted text-sm">Avg Duration</p>
          <p className="text-2xl font-bold">5m 23s</p>
        </div>
        <div className="bg-card rounded-lg p-4 border border-border">
          <p className="text-muted text-sm">Sentiment</p>
          <p className="text-2xl font-bold">88%</p>
        </div>
      </div>

      {/* Filter */}
      <div className="flex gap-4">
        <input
          type="text"
          placeholder="Search by phone number or customer..."
          className="flex-1 px-4 py-2 rounded-lg bg-card border border-border text-foreground placeholder-muted"
        />
        <select className="px-4 py-2 rounded-lg bg-card border border-border text-foreground">
          <option>All Calls</option>
          <option>Incoming</option>
          <option>Outgoing</option>
        </select>
      </div>

      {/* Calls Table */}
      <div className="bg-card rounded-lg border border-border overflow-hidden">
        <table className="w-full">
          <thead>
            <tr className="border-b border-border bg-card-foreground/5">
              <th className="px-6 py-3 text-left text-sm font-semibold">Phone Number</th>
              <th className="px-6 py-3 text-left text-sm font-semibold">Date & Time</th>
              <th className="px-6 py-3 text-left text-sm font-semibold">Duration</th>
              <th className="px-6 py-3 text-left text-sm font-semibold">Intent</th>
              <th className="px-6 py-3 text-left text-sm font-semibold">Sentiment</th>
              <th className="px-6 py-3 text-left text-sm font-semibold">Actions</th>
            </tr>
          </thead>
          <tbody>
            {[1, 2, 3, 4, 5, 6].map((i) => (
              <tr key={i} className="border-b border-border hover:bg-card-foreground/5 transition">
                <td className="px-6 py-4 text-sm">+1 (555) 123-4567</td>
                <td className="px-6 py-4 text-sm">Today at 10:30 AM</td>
                <td className="px-6 py-4 text-sm">3m 45s</td>
                <td className="px-6 py-4 text-sm">
                  <span className="px-2 py-1 rounded-full bg-blue-500/20 text-blue-400 text-xs">Booking</span>
                </td>
                <td className="px-6 py-4 text-sm">
                  <span className="px-2 py-1 rounded-full bg-success/20 text-success text-xs">Positive</span>
                </td>
                <td className="px-6 py-4 text-sm">
                  <button className="text-primary hover:text-primary/80 mr-3">Listen</button>
                  <button className="text-primary hover:text-primary/80">Details</button>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}
