export default function BookingsPage() {
  return (
    <div className="space-y-6">
      <div className="flex justify-between items-center">
        <div>
          <h1 className="text-3xl font-bold">Appointments</h1>
          <p className="text-muted mt-2">Manage and schedule appointments</p>
        </div>
        <button className="px-4 py-2 rounded-lg bg-primary text-white hover:bg-primary/90 transition">
          + New Appointment
        </button>
      </div>

      {/* Filter and Search */}
      <div className="flex gap-4">
        <input
          type="text"
          placeholder="Search appointments..."
          className="flex-1 px-4 py-2 rounded-lg bg-card border border-border text-foreground placeholder-muted"
        />
        <select className="px-4 py-2 rounded-lg bg-card border border-border text-foreground">
          <option>All Status</option>
          <option>Confirmed</option>
          <option>Pending</option>
          <option>Completed</option>
          <option>Cancelled</option>
        </select>
      </div>

      {/* Appointments Table */}
      <div className="bg-card rounded-lg border border-border overflow-hidden">
        <table className="w-full">
          <thead>
            <tr className="border-b border-border bg-card-foreground/5">
              <th className="px-6 py-3 text-left text-sm font-semibold">Customer</th>
              <th className="px-6 py-3 text-left text-sm font-semibold">Date & Time</th>
              <th className="px-6 py-3 text-left text-sm font-semibold">Service</th>
              <th className="px-6 py-3 text-left text-sm font-semibold">Staff</th>
              <th className="px-6 py-3 text-left text-sm font-semibold">Status</th>
              <th className="px-6 py-3 text-left text-sm font-semibold">Actions</th>
            </tr>
          </thead>
          <tbody>
            {[1, 2, 3, 4, 5].map((i) => (
              <tr key={i} className="border-b border-border hover:bg-card-foreground/5 transition">
                <td className="px-6 py-4 text-sm">John Doe</td>
                <td className="px-6 py-4 text-sm">Today at 2:00 PM</td>
                <td className="px-6 py-4 text-sm">Consultation</td>
                <td className="px-6 py-4 text-sm">Dr. Smith</td>
                <td className="px-6 py-4 text-sm">
                  <span className="px-3 py-1 rounded-full bg-success/20 text-success text-xs font-medium">
                    Confirmed
                  </span>
                </td>
                <td className="px-6 py-4 text-sm">
                  <button className="text-primary hover:text-primary/80">Edit</button>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>

      {/* Pagination */}
      <div className="flex justify-between items-center">
        <p className="text-sm text-muted">Showing 1 to 5 of 24 appointments</p>
        <div className="flex gap-2">
          <button className="px-3 py-1 rounded border border-border hover:bg-card-foreground/5 transition">Previous</button>
          <button className="px-3 py-1 rounded bg-primary text-white">1</button>
          <button className="px-3 py-1 rounded border border-border hover:bg-card-foreground/5 transition">2</button>
          <button className="px-3 py-1 rounded border border-border hover:bg-card-foreground/5 transition">Next</button>
        </div>
      </div>
    </div>
  );
}
