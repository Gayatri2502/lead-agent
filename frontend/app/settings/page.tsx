export default function SettingsPage() {
  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-3xl font-bold">Settings</h1>
        <p className="text-muted mt-2">Configure business and system settings</p>
      </div>

      {/* Tabs */}
      <div className="bg-card rounded-lg border border-border">
        <div className="flex border-b border-border">
          <button className="px-6 py-4 font-semibold text-primary border-b-2 border-primary">
            Business
          </button>
          <button className="px-6 py-4 font-semibold text-muted hover:text-foreground transition">
            AI Configuration
          </button>
          <button className="px-6 py-4 font-semibold text-muted hover:text-foreground transition">
            Integrations
          </button>
          <button className="px-6 py-4 font-semibold text-muted hover:text-foreground transition">
            Notifications
          </button>
        </div>

        {/* Settings Content */}
        <div className="p-6 space-y-6">
          {/* Business Name */}
          <div>
            <label className="block text-sm font-semibold mb-2">Business Name</label>
            <input
              type="text"
              placeholder="Your business name"
              className="w-full px-4 py-2 rounded-lg bg-card-foreground/5 border border-border text-foreground placeholder-muted"
              defaultValue="Healthcare Clinic"
            />
          </div>

          {/* Business Type */}
          <div>
            <label className="block text-sm font-semibold mb-2">Business Type</label>
            <select className="w-full px-4 py-2 rounded-lg bg-card-foreground/5 border border-border text-foreground">
              <option>Medical Practice</option>
              <option>Dental Clinic</option>
              <option>Salon</option>
              <option>Fitness Center</option>
              <option>Other</option>
            </select>
          </div>

          {/* Working Hours */}
          <div>
            <label className="block text-sm font-semibold mb-4">Working Hours</label>
            <div className="grid grid-cols-2 gap-4">
              <div>
                <label className="text-sm text-muted block mb-1">Open Time</label>
                <input
                  type="time"
                  className="w-full px-4 py-2 rounded-lg bg-card-foreground/5 border border-border text-foreground"
                  defaultValue="09:00"
                />
              </div>
              <div>
                <label className="text-sm text-muted block mb-1">Close Time</label>
                <input
                  type="time"
                  className="w-full px-4 py-2 rounded-lg bg-card-foreground/5 border border-border text-foreground"
                  defaultValue="17:00"
                />
              </div>
            </div>
          </div>

          {/* Timezone */}
          <div>
            <label className="block text-sm font-semibold mb-2">Timezone</label>
            <select className="w-full px-4 py-2 rounded-lg bg-card-foreground/5 border border-border text-foreground">
              <option>UTC</option>
              <option>EST (UTC-5)</option>
              <option>CST (UTC-6)</option>
              <option>MST (UTC-7)</option>
              <option>PST (UTC-8)</option>
            </select>
          </div>

          {/* Appointment Duration */}
          <div>
            <label className="block text-sm font-semibold mb-2">Default Appointment Duration</label>
            <div className="flex gap-2">
              <input
                type="number"
                min="15"
                step="15"
                className="w-32 px-4 py-2 rounded-lg bg-card-foreground/5 border border-border text-foreground"
                defaultValue="30"
              />
              <span className="flex items-center text-muted">minutes</span>
            </div>
          </div>

          {/* Buttons */}
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
