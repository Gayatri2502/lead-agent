export default function BillingPage() {
  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-3xl font-bold">Billing</h1>
        <p className="text-muted mt-2">Manage your subscription and billing</p>
      </div>

      {/* Current Plan */}
      <div className="bg-card rounded-lg p-6 border border-border">
        <div className="flex justify-between items-start mb-6 pb-6 border-b border-border">
          <div>
            <h3 className="text-lg font-semibold mb-2">Current Plan</h3>
            <p className="text-2xl font-bold text-primary">Professional</p>
            <p className="text-muted text-sm mt-1">$99/month • Billed monthly</p>
          </div>
          <div className="text-right">
            <p className="text-muted text-sm mb-4">Renews on December 15, 2024</p>
            <button className="px-4 py-2 rounded-lg border border-border hover:bg-card-foreground/5 transition text-sm">
              Change Plan
            </button>
          </div>
        </div>

        {/* Plan Features */}
        <div className="grid grid-cols-2 gap-4">
          <div>
            <p className="text-muted text-sm mb-1">Calls per month</p>
            <p className="font-semibold">5,000</p>
          </div>
          <div>
            <p className="text-muted text-sm mb-1">Team members</p>
            <p className="font-semibold">10</p>
          </div>
          <div>
            <p className="text-muted text-sm mb-1">Call recordings</p>
            <p className="font-semibold">Unlimited</p>
          </div>
          <div>
            <p className="text-muted text-sm mb-1">Support</p>
            <p className="font-semibold">Priority</p>
          </div>
        </div>
      </div>

      {/* Usage */}
      <div className="bg-card rounded-lg p-6 border border-border">
        <h3 className="text-lg font-semibold mb-4">Usage This Month</h3>
        <div className="space-y-4">
          <div>
            <div className="flex justify-between mb-2">
              <span className="text-sm">Calls Used</span>
              <span className="text-sm font-semibold">3,245 / 5,000</span>
            </div>
            <div className="w-full bg-card-foreground/10 rounded-full h-2">
              <div className="bg-primary h-2 rounded-full" style={{width: '65%'}}></div>
            </div>
          </div>
          <div>
            <div className="flex justify-between mb-2">
              <span className="text-sm">Storage Used</span>
              <span className="text-sm font-semibold">245 GB / 500 GB</span>
            </div>
            <div className="w-full bg-card-foreground/10 rounded-full h-2">
              <div className="bg-primary h-2 rounded-full" style={{width: '49%'}}></div>
            </div>
          </div>
        </div>
      </div>

      {/* Billing History */}
      <div className="bg-card rounded-lg p-6 border border-border">
        <div className="flex justify-between items-center mb-4">
          <h3 className="text-lg font-semibold">Billing History</h3>
          <button className="text-primary hover:text-primary/80 text-sm">Download All</button>
        </div>

        <table className="w-full">
          <thead>
            <tr className="border-b border-border">
              <th className="px-4 py-3 text-left text-sm font-semibold">Date</th>
              <th className="px-4 py-3 text-left text-sm font-semibold">Description</th>
              <th className="px-4 py-3 text-left text-sm font-semibold">Amount</th>
              <th className="px-4 py-3 text-left text-sm font-semibold">Status</th>
              <th className="px-4 py-3 text-left text-sm font-semibold">Invoice</th>
            </tr>
          </thead>
          <tbody>
            {[1, 2, 3, 4, 5].map((i) => (
              <tr key={i} className="border-b border-border hover:bg-card-foreground/5 transition">
                <td className="px-4 py-3 text-sm">Nov 15, 2024</td>
                <td className="px-4 py-3 text-sm">Professional Plan</td>
                <td className="px-4 py-3 text-sm font-semibold">$99.00</td>
                <td className="px-4 py-3 text-sm">
                  <span className="px-2 py-1 rounded-full bg-success/20 text-success text-xs">Paid</span>
                </td>
                <td className="px-4 py-3 text-sm">
                  <button className="text-primary hover:text-primary/80">Download</button>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>

      {/* Payment Method */}
      <div className="bg-card rounded-lg p-6 border border-border">
        <h3 className="text-lg font-semibold mb-4">Payment Method</h3>
        <div className="flex items-center justify-between p-4 rounded-lg bg-card-foreground/5 border border-border">
          <div className="flex items-center gap-3">
            <span className="text-2xl">💳</span>
            <div>
              <p className="font-semibold">Visa ending in 4242</p>
              <p className="text-sm text-muted">Expires 12/26</p>
            </div>
          </div>
          <button className="text-primary hover:text-primary/80 text-sm">Update</button>
        </div>
      </div>
    </div>
  );
}
