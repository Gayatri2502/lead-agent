export default function ProfilePage() {
  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-3xl font-bold">Profile</h1>
        <p className="text-muted mt-2">Manage your personal information</p>
      </div>

      {/* Profile Card */}
      <div className="bg-card rounded-lg p-6 border border-border max-w-2xl">
        <div className="flex items-center gap-4 mb-6 pb-6 border-b border-border">
          <div className="w-20 h-20 rounded-full bg-primary/20 flex items-center justify-center text-2xl font-bold">
            JD
          </div>
          <div>
            <h2 className="text-2xl font-bold">John Doe</h2>
            <p className="text-muted">Manager</p>
            <button className="text-sm text-primary hover:text-primary/80 mt-2">Change Avatar</button>
          </div>
        </div>

        {/* Form */}
        <div className="space-y-4">
          <div className="grid grid-cols-2 gap-4">
            <div>
              <label className="block text-sm font-semibold mb-2">First Name</label>
              <input
                type="text"
                className="w-full px-4 py-2 rounded-lg bg-card-foreground/5 border border-border text-foreground"
                defaultValue="John"
              />
            </div>
            <div>
              <label className="block text-sm font-semibold mb-2">Last Name</label>
              <input
                type="text"
                className="w-full px-4 py-2 rounded-lg bg-card-foreground/5 border border-border text-foreground"
                defaultValue="Doe"
              />
            </div>
          </div>

          <div>
            <label className="block text-sm font-semibold mb-2">Email</label>
            <input
              type="email"
              className="w-full px-4 py-2 rounded-lg bg-card-foreground/5 border border-border text-foreground"
              defaultValue="john@example.com"
            />
          </div>

          <div>
            <label className="block text-sm font-semibold mb-2">Phone</label>
            <input
              type="tel"
              className="w-full px-4 py-2 rounded-lg bg-card-foreground/5 border border-border text-foreground"
              defaultValue="+1 (555) 123-4567"
            />
          </div>

          <div>
            <label className="block text-sm font-semibold mb-2">Current Password</label>
            <input
              type="password"
              className="w-full px-4 py-2 rounded-lg bg-card-foreground/5 border border-border text-foreground"
              placeholder="Enter current password"
            />
          </div>

          <div className="grid grid-cols-2 gap-4">
            <div>
              <label className="block text-sm font-semibold mb-2">New Password</label>
              <input
                type="password"
                className="w-full px-4 py-2 rounded-lg bg-card-foreground/5 border border-border text-foreground"
                placeholder="New password"
              />
            </div>
            <div>
              <label className="block text-sm font-semibold mb-2">Confirm Password</label>
              <input
                type="password"
                className="w-full px-4 py-2 rounded-lg bg-card-foreground/5 border border-border text-foreground"
                placeholder="Confirm password"
              />
            </div>
          </div>

          <div className="flex gap-4 pt-6 border-t border-border">
            <button className="px-6 py-2 rounded-lg bg-primary text-white hover:bg-primary/90 transition">
              Save Changes
            </button>
            <button className="px-6 py-2 rounded-lg border border-border hover:bg-card-foreground/5 transition">
              Cancel
            </button>
          </div>
        </div>
      </div>
    </div>
  );
}
