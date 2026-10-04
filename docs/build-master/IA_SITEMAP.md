# Information Architecture & Sitemap

## Site Hierarchy

```
AI Voice Receptionist Dashboard
├── / (Root) → Redirects to /dashboard
├── /auth
│   ├── /login
│   ├── /register
│   ├── /forgot-password
│   └── /reset-password
├── /dashboard (Home)
├── /bookings
│   ├── /bookings/new
│   ├── /bookings/[id]
│   └── /bookings/[id]/edit
├── /customers
│   ├── /customers/new
│   ├── /customers/[id]
│   ├── /customers/[id]/edit
│   └── /customers/import
├── /calls
│   ├── /calls/[id]
│   ├── /calls/[id]/transcript
│   └── /calls/export
├── /analytics
│   ├── /analytics/overview
│   ├── /analytics/calls
│   ├── /analytics/appointments
│   ├── /analytics/customers
│   └── /analytics/revenue
├── /staff
│   ├── /staff/new
│   ├── /staff/[id]
│   └── /staff/[id]/edit
├── /settings
│   ├── /settings/general
│   ├── /settings/business
│   ├── /settings/integrations
│   ├── /settings/notifications
│   └── /settings/appearance
├── /profile
├── /api-settings
│   ├── /api-settings/keys
│   ├── /api-settings/webhooks
│   └── /api-settings/documentation
└── /billing
    ├── /billing/plans
    ├── /billing/invoices
    ├── /billing/payment-methods
    └── /billing/usage
```

---

## URL Structure Conventions

| Pattern | Example | Purpose |
|---------|---------|---------|
| `/resource` | `/customers` | List view with search/filter |
| `/resource/new` | `/customers/new` | Create new resource |
| `/resource/[id]` | `/customers/123` | Detail view |
| `/resource/[id]/edit` | `/customers/123/edit` | Edit form |
| `/resource/[id]/action` | `/calls/123/transcript` | Sub-resource/action |

---

## Navigation Patterns

### Global Navigation (Sidebar)
Persistent across all authenticated pages:
- Dashboard
- Bookings
- Customers
- Calls
- Analytics
- Staff
- Settings (nested)
- Profile
- API Settings
- Billing

### Contextual Navigation
- **Bookings**: Tabs for Upcoming / Past / Cancelled
- **Customers**: Filter tabs for All / Returning / New
- **Calls**: Filter tabs for All / Incoming / Outgoing
- **Analytics**: Sub-nav for Overview / Calls / Appointments / Customers / Revenue
- **Settings**: Vertical tabs for General / Business / Integrations / Notifications / Appearance

### Breadcrumb Pattern
```
Dashboard > Customers > John Doe > Edit
Settings > Integrations > Google Calendar
```

---

## Content Models

### Business
```typescript
interface Business {
  id: number;
  name: string;
  businessType: string;
  timezone: string;
  appointmentDuration: number;
  bookingAdvanceDays: number;
  cancellationNoticeHours: number;
  workingHours: WorkingHours;
  holidaySchedule: Holiday[];
  isActive: boolean;
  isVerified: boolean;
}
```

### User
```typescript
interface User {
  id: number;
  businessId: number;
  email: string;
  username: string;
  role: 'owner' | 'admin' | 'staff' | 'viewer';
  firstName: string;
  lastName: string;
  phone?: string;
  avatarUrl?: string;
  isActive: boolean;
  lastLogin?: Date;
}
```

### Customer
```typescript
interface Customer {
  id: number;
  businessId: number;
  firstName: string;
  lastName: string;
  phone: string;
  email?: string;
  address?: string;
  dateOfBirth?: Date;
  gender?: string;
  language: string;
  medicalHistory?: string;
  preferences: CustomerPreferences;
  isReturning: boolean;
  doNotCall: boolean;
  createdAt: Date;
  lastAppointment?: Date;
}
```

### Appointment
```typescript
interface Appointment {
  id: number;
  businessId: number;
  customerId: number;
  staffId?: number;
  serviceId?: number;
  startTime: Date;
  endTime: Date;
  duration: number;
  status: 'pending' | 'confirmed' | 'completed' | 'cancelled' | 'no-show';
  reason?: string;
  notes?: string;
  specialRequests?: string;
  bookingSource: 'phone' | 'web' | 'walk-in' | 'api';
  reminderSent: boolean;
  callId?: number;
}
```

### Call
```typescript
interface Call {
  id: number;
  businessId: number;
  customerId?: number;
  callId: string; // Twilio/Vapi ID
  phoneNumber: string;
  direction: 'incoming' | 'outgoing';
  startTime: Date;
  endTime?: Date;
  duration?: number;
  recordingUrl?: string;
  transcript?: string;
  summary?: string;
  sentiment: 'positive' | 'neutral' | 'negative';
  intent?: string;
  status: 'completed' | 'missed' | 'voicemail' | 'failed';
  escalatedToHuman: boolean;
}
```

### Analytics (Aggregated)
```typescript
interface AnalyticsOverview {
  totalCalls: number;
  callsToday: number;
  avgDuration: number;
  appointmentsBooked: number;
  sentimentScore: number;
  conversionRate: number;
  missedCalls: number;
  peakHours: HourlyStats[];
}

interface HourlyStats {
  hour: number;
  callCount: number;
  avgSentiment: number;
}
```

---

## Page Content Requirements

### /dashboard
- **Primary**: Stats grid (4 KPIs), Charts (2), Quick Actions
- **Secondary**: Recent activity feed, Alerts/Notifications
- **Loading**: Skeleton for each stat card and chart
- **Empty**: Onboarding CTA if no data

### /bookings
- **Primary**: Filterable, sortable, paginated table
- **Secondary**: Calendar view (toggle), Stats summary
- **Actions**: New, Edit, Cancel, Reschedule, View Details
- **Bulk**: Multi-select for bulk actions

### /customers
- **Primary**: Searchable, filterable card grid (mobile) / table (desktop)
- **Secondary**: Customer detail drawer/modal
- **Actions**: New, Edit, View History, Delete, Import/Export

### /calls
- **Primary**: Filterable table with audio player inline
- **Secondary**: Transcript viewer, Sentiment timeline
- **Actions**: Listen, View Details, Tag, Export

### /analytics
- **Primary**: Interactive charts (Recharts/Chart.js)
- **Secondary**: Date range picker, Export controls
- **Tabs**: Overview / Calls / Appointments / Customers / Revenue

### /staff
- **Primary**: Grid of staff cards with availability
- **Secondary**: Schedule view, Performance metrics
- **Actions**: New, Edit, View Schedule, Deactivate

### /settings
- **Structure**: Vertical tabs, each tab = separate page section
- **Forms**: Auto-save with dirty state indicator
- **Validation**: Client + server validation

---

## Scalability Considerations

### Future Pages (Phase 2+)
- `/campaigns` - Outbound calling campaigns
- `/recordings` - Call recording library
- `/transcripts` - Full transcript search
- `/integrations/marketplace` - Third-party integrations
- `/team/activity` - Team performance dashboard
- `/ai/training` - AI model feedback/training

### Multi-Business Support
- URL: `/business/[businessId]/dashboard`
- Switcher in header for multi-business users
- Shared components, isolated data

### Mobile-First Breakpoints
| Breakpoint | Min Width | Layout Changes |
|------------|-----------|----------------|
| Mobile | 320px | Single column, drawer navigation |
| Mobile LG | 375px | Slightly wider cards |
| Tablet | 768px | 2-col grids, sidebar collapsible |
| Desktop | 1024px | 3-4 col grids, persistent sidebar |
| Desktop LG | 1440px | Max-width containers |
| Ultra-wide | 1920px | Constrained content width |

---

## SEO URL Strategy

| Page | Title Template | Description Template |
|------|----------------|---------------------|
| Dashboard | "Dashboard - {Business Name}" | "Overview of calls, appointments, and customer insights for {Business Name}" |
| Bookings | "Appointments - {Business Name}" | "Manage and schedule appointments for {Business Name}" |
| Customers | "Customers - {Business Name}" | "Customer profiles and interaction history for {Business Name}" |
| Calls | "Call History - {Business Name}" | "Review and analyze calls for {Business Name}" |
| Analytics | "Analytics - {Business Name}" | "Business performance analytics and insights for {Business Name}" |

---

## Canonical URLs & Robots

- All authenticated pages: `noindex, nofollow` (private dashboard)
- Public pages (login, marketing): `index, follow`
- API routes: `noindex`
- Sitemap: Only public marketing pages