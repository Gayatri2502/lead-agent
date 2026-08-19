import type { Metadata } from "next";
import "@/styles/globals.css";

export const metadata: Metadata = {
  title: "AI Voice Receptionist - Dashboard",
  description: "Manage appointments and calls with AI assistance",
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en">
      <body className="bg-background text-foreground">
        <div className="flex h-screen">
          {/* Sidebar */}
          <aside className="hidden md:flex w-64 bg-card border-r border-border flex-col">
            <div className="p-6 border-b border-border">
              <h1 className="text-2xl font-bold text-primary">
                Voice AI
              </h1>
              <p className="text-sm text-muted mt-1">Receptionist</p>
            </div>
            <nav className="flex-1 overflow-y-auto p-4 space-y-2">
              <a
                href="/dashboard"
                className="block px-4 py-2 rounded-lg bg-primary/10 text-primary hover:bg-primary/20 transition"
              >
                Dashboard
              </a>
              <a
                href="/bookings"
                className="block px-4 py-2 rounded-lg text-muted hover:bg-card-foreground/5 transition"
              >
                Bookings
              </a>
              <a
                href="/customers"
                className="block px-4 py-2 rounded-lg text-muted hover:bg-card-foreground/5 transition"
              >
                Customers
              </a>
              <a
                href="/calls"
                className="block px-4 py-2 rounded-lg text-muted hover:bg-card-foreground/5 transition"
              >
                Calls
              </a>
              <a
                href="/analytics"
                className="block px-4 py-2 rounded-lg text-muted hover:bg-card-foreground/5 transition"
              >
                Analytics
              </a>
              <a
                href="/staff"
                className="block px-4 py-2 rounded-lg text-muted hover:bg-card-foreground/5 transition"
              >
                Staff
              </a>
              <a
                href="/settings"
                className="block px-4 py-2 rounded-lg text-muted hover:bg-card-foreground/5 transition"
              >
                Settings
              </a>
            </nav>
            <div className="p-4 border-t border-border">
              <a
                href="/profile"
                className="block px-4 py-2 rounded-lg text-muted hover:bg-card-foreground/5 transition"
              >
                Profile
              </a>
              <a
                href="/api-settings"
                className="block px-4 py-2 rounded-lg text-muted hover:bg-card-foreground/5 transition"
              >
                API Settings
              </a>
            </div>
          </aside>

          {/* Main content */}
          <main className="flex-1 flex flex-col overflow-hidden">
            {/* Header */}
            <header className="bg-card border-b border-border px-6 py-4 flex items-center justify-between">
              <div>
                <h2 className="text-xl font-semibold">Welcome back</h2>
              </div>
              <div className="flex items-center gap-4">
                <button className="px-4 py-2 rounded-lg bg-primary text-white hover:bg-primary/90 transition">
                  + New Appointment
                </button>
                <div className="w-10 h-10 rounded-full bg-primary/20 flex items-center justify-center">
                  <span className="text-sm font-semibold">JD</span>
                </div>
              </div>
            </header>

            {/* Content */}
            <div className="flex-1 overflow-y-auto bg-background p-6">
              {children}
            </div>
          </main>
        </div>
      </body>
    </html>
  );
}
