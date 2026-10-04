# Visual Direction: AI Voice Receptionist Dashboard

## Art Direction Statement

**Professional. Intelligent. Calm.**

A dark-mode-first dashboard that feels like mission control for voice AI—where data density meets breathing room, and every interaction communicates competence. No decorative gradients, no glassmorphism for its own sake. Visual hierarchy driven by typography and spacing, not effects.

---

## Mood Board References

| Reference | What We Borrow |
|-----------|----------------|
| Linear.app | Clean typography, purposeful motion, keyboard-first |
| Vercel Dashboard | Dark mode execution, data density, technical credibility |
| Stripe Dashboard | Trust signals, clear hierarchy, refined components |
| GitHub | Information density, monospace for data, subtle borders |
| Notion | Calm color palette, generous whitespace, focus on content |

---

## Color Philosophy

**Dark Mode First** — Not an afterthought. Designed for darkened rooms, late nights, multi-monitor setups.

**Semantic, Not Decorative** — Every color has a job:
- Primary = Action/Interactive
- Success = Positive confirmation
- Warning = Attention needed
- Destructive = Irreversible actions
- Muted = Secondary information

**No Arbitrary Gradients** — Gradients only for:
- Hero/marketing areas (not dashboard)
- Data visualization (chart series)
- Loading skeletons (subtle shimmer)

---

## Visual Language

### Photography
- **None in dashboard** — This is a tool, not a brochure
- Marketing pages only: Abstract sound wave visualizations, not stock photos

### Illustration
- **Minimal, functional** — Empty states use simple line icons
- **No characters/mascots** — Reduces cognitive load, feels more professional

### Iconography
- **Lucide React** — Consistent 2px stroke, 24x24 default
- **Semantic mapping**: Phone=Calls, Calendar=Bookings, Users=Customers, BarChart=Analytics
- **State variants**: Filled for active, outline for inactive

---

## Key Page Art Direction

### Dashboard
- **Hero stat cards**: Large numbers, subtle icon, trend indicator
- **Charts**: Clean axes, no chart junk, tooltips on hover
- **Activity feed**: Compact, scannable, timestamp-right alignment

### Bookings
- **Table-first** — Dense, sortable, keyboard-navigable
- **Status pills**: Semantic colors, consistent width
- **Inline actions**: Edit on click, no separate detail page for simple edits

### Customers
- **Card grid (mobile) / Table (desktop)** — Responsive pattern
- **Avatar initials** — No external image dependencies
- **Quick actions**: View/Edit always accessible

### Calls
- **Audio-first** — Play button prominent, waveform preview
- **Transcript**: Monospace, speaker labels, timestamp sync
- **Sentiment**: Color-coded timeline, not just badge

### Analytics
- **Chart-first** — Full width, interactive, exportable
- **Date picker**: Prominent, preset ranges (7d, 30d, 90d)
- **KPIs**: Above fold, large, with sparklines

---

## Motion Direction

| Interaction | Motion | Duration | Easing |
|-------------|--------|----------|--------|
| Page transition | Fade + slide up | 200ms | ease-out |
| Modal/Dialog | Scale + fade | 150ms | ease-out |
| Dropdown | Slide down + fade | 100ms | ease-out |
| Toast | Slide in from right | 200ms | ease-out |
| Table row hover | Background shift | 100ms | ease-out |
| Button press | Scale 0.98 | 50ms | ease-out |
| Tab switch | Cross-fade | 150ms | ease-in-out |
| Skeleton → Content | Cross-fade | 300ms | ease-out |

**Reduced Motion**: All animations disabled via `prefers-reduced-motion`

---

## Typography Tone

- **Headings**: System font, semibold, tight tracking
- **Body**: System font, regular, relaxed line-height (1.6)
- **Data/Monospace**: JetBrains Mono / SF Mono for numbers, codes, timestamps
- **Labels**: Uppercase, tracking-wide, text-xs, muted

---

## Spacing Rhythm

Base unit: **4px** (0.25rem)

| Token | Value | Use Case |
|-------|-------|----------|
| space-1 | 4px | Icon gaps, inline elements |
| space-2 | 8px | Button padding, form gaps |
| space-3 | 12px | Card internal padding |
| space-4 | 16px | Standard component padding |
| space-6 | 24px | Section gaps, card margins |
| space-8 | 32px | Page section spacing |
| space-12 | 48px | Major section breaks |

---

## Elevation & Depth

**Flat by default** — No box-shadows on cards
- **Level 0**: Base (cards, inputs) — border only
- **Level 1**: Hover/Active — border color shift
- **Level 2**: Dropdowns, Tooltips — subtle shadow (4px blur)
- **Level 3**: Modals, Drawers — medium shadow (16px blur) + overlay
- **Level 4**: Toasts — high shadow (24px blur) + overlay

---

## Data Visualization Style

- **Colors**: Semantic palette (primary, success, warning, destructive)
- **Grid**: Subtle, dashed, muted
- **Axes**: Muted labels, no axis lines
- **Tooltips**: Dark bg, white text, monospace values
- **Legends**: Bottom, horizontal, interactive (click to toggle)
- **Empty**: Centered icon + helpful text + CTA

---

## Responsive Behavior

| Component | Mobile (<768px) | Tablet (768-1024px) | Desktop (>1024px) |
|-----------|-----------------|---------------------|-------------------|
| Sidebar | Drawer (hamburger) | Collapsible (icons only) | Full labels |
| Stats Grid | 1 col | 2 col | 4 col |
| Tables | Card stack | Horizontal scroll | Full table |
| Charts | Full width, stacked | 2 col | 2-3 col |
| Forms | Full width fields | 2 col fields | 2-3 col fields |
| Modals | Full screen | Centered, max-w-2xl | Centered, max-w-lg |

---

## Accessibility Visual Requirements

- **Contrast**: All text ≥ 4.5:1, UI elements ≥ 3:1
- **Focus**: Visible 2px ring, offset 2px, primary color
- **Color Blind**: Never rely on color alone (icons + text + patterns)
- **Zoom**: Tested at 200%, no horizontal scroll
- **High Contrast Mode**: Windows HCM tested, borders visible