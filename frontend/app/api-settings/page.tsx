export default function APISettingsPage() {
  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-3xl font-bold">API Settings</h1>
        <p className="text-muted mt-2">Manage API keys and integrations</p>
      </div>

      {/* API Keys Section */}
      <div className="bg-card rounded-lg p-6 border border-border">
        <div className="flex justify-between items-center mb-6">
          <h3 className="text-lg font-semibold">API Keys</h3>
          <button className="px-4 py-2 rounded-lg bg-primary text-white hover:bg-primary/90 transition text-sm">
            + Generate Key
          </button>
        </div>

        {/* API Keys Table */}
        <div className="overflow-x-auto">
          <table className="w-full">
            <thead>
              <tr className="border-b border-border">
                <th className="px-4 py-3 text-left text-sm font-semibold">Name</th>
                <th className="px-4 py-3 text-left text-sm font-semibold">Key</th>
                <th className="px-4 py-3 text-left text-sm font-semibold">Created</th>
                <th className="px-4 py-3 text-left text-sm font-semibold">Last Used</th>
                <th className="px-4 py-3 text-left text-sm font-semibold">Status</th>
                <th className="px-4 py-3 text-left text-sm font-semibold">Actions</th>
              </tr>
            </thead>
            <tbody>
              {[1, 2].map((i) => (
                <tr key={i} className="border-b border-border hover:bg-card-foreground/5 transition">
                  <td className="px-4 py-3 text-sm">Production API Key {i}</td>
                  <td className="px-4 py-3 text-sm font-mono text-xs">sk_live_••••••••••••{i}{i}{i}{i}</td>
                  <td className="px-4 py-3 text-sm">2 months ago</td>
                  <td className="px-4 py-3 text-sm">Today</td>
                  <td className="px-4 py-3 text-sm">
                    <span className="px-2 py-1 rounded-full bg-success/20 text-success text-xs">Active</span>
                  </td>
                  <td className="px-4 py-3 text-sm">
                    <button className="text-primary hover:text-primary/80 mr-3">Rotate</button>
                    <button className="text-destructive hover:text-destructive/80">Revoke</button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>

      {/* Webhooks Section */}
      <div className="bg-card rounded-lg p-6 border border-border">
        <div className="flex justify-between items-center mb-6">
          <h3 className="text-lg font-semibold">Webhooks</h3>
          <button className="px-4 py-2 rounded-lg bg-primary text-white hover:bg-primary/90 transition text-sm">
            + Add Webhook
          </button>
        </div>

        {/* Webhooks List */}
        <div className="space-y-4">
          {[1, 2].map((i) => (
            <div key={i} className="p-4 rounded-lg bg-card-foreground/5 border border-border">
              <div className="flex justify-between items-start mb-2">
                <div>
                  <h4 className="font-semibold">Call Completed Event</h4>
                  <p className="text-sm text-muted">https://yourserver.com/webhooks/call-completed</p>
                </div>
                <span className="px-2 py-1 rounded text-xs bg-success/20 text-success">Active</span>
              </div>
              <div className="text-xs text-muted mb-3">
                Last triggered: 2 hours ago • Success rate: 99.8%
              </div>
              <div className="flex gap-2">
                <button className="text-primary hover:text-primary/80 text-sm">Edit</button>
                <button className="text-primary hover:text-primary/80 text-sm">Test</button>
                <button className="text-destructive hover:text-destructive/80 text-sm">Delete</button>
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* Documentation */}
      <div className="bg-card rounded-lg p-6 border border-border">
        <h3 className="text-lg font-semibold mb-4">API Documentation</h3>
        <p className="text-muted mb-4">
          Complete documentation for integrating with our AI Voice Receptionist API is available at:
        </p>
        <div className="flex gap-4">
          <button className="px-4 py-2 rounded-lg bg-primary/10 text-primary hover:bg-primary/20 transition text-sm">
            📖 API Docs
          </button>
          <button className="px-4 py-2 rounded-lg bg-primary/10 text-primary hover:bg-primary/20 transition text-sm">
            🔗 Webhook Guide
          </button>
          <button className="px-4 py-2 rounded-lg bg-primary/10 text-primary hover:bg-primary/20 transition text-sm">
            💻 Code Examples
          </button>
        </div>
      </div>
    </div>
  );
}
