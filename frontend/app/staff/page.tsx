export default function StaffPage() {
  return (
    <div className="space-y-6">
      <div className="flex justify-between items-center">
        <div>
          <h1 className="text-3xl font-bold">Staff Management</h1>
          <p className="text-muted mt-2">Manage team members and availability</p>
        </div>
        <button className="px-4 py-2 rounded-lg bg-primary text-white hover:bg-primary/90 transition">
          + Add Staff
        </button>
      </div>

      {/* Staff Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
        {[1, 2, 3, 4, 5, 6].map((i) => (
          <div key={i} className="bg-card rounded-lg p-6 border border-border">
            <div className="flex items-center gap-4 mb-4">
              <div className="w-12 h-12 rounded-full bg-primary/20 flex items-center justify-center font-bold">
                DS
              </div>
              <div className="flex-1">
                <h3 className="font-semibold">Dr. Smith {i}</h3>
                <p className="text-sm text-muted">Specialist</p>
              </div>
              <span className="px-2 py-1 rounded text-xs bg-success/20 text-success">Active</span>
            </div>
            <div className="space-y-2 mb-4 pb-4 border-b border-border">
              <p className="text-sm text-muted">📧 dr.smith@business.com</p>
              <p className="text-sm text-muted">📱 +1 (555) 987-6543</p>
            </div>
            <div className="mb-4">
              <p className="text-sm font-semibold mb-2">Available Hours</p>
              <p className="text-sm text-muted">Monday - Friday</p>
              <p className="text-sm text-muted">9:00 AM - 5:00 PM</p>
            </div>
            <div className="flex gap-2">
              <button className="flex-1 px-3 py-2 rounded text-sm bg-primary/10 text-primary hover:bg-primary/20 transition">
                Edit
              </button>
              <button className="flex-1 px-3 py-2 rounded text-sm border border-border hover:bg-card-foreground/5 transition">
                View Calendar
              </button>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
