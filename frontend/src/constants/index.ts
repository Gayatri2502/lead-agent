/** Application constants */
export const APP_NAME = 'AI Voice Receptionist';
export const APP_DESCRIPTION = 'Manage appointments and calls with AI assistance';

/** API Configuration */
export const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000/api/v1';
export const API_TIMEOUT = 30000;

/** Pagination defaults */
export const DEFAULT_PAGE_SIZE = 20;
export const PAGE_SIZE_OPTIONS = [10, 20, 50, 100];

/** Date formats */
export const DATE_FORMAT = 'MMM d, yyyy';
export const DATE_TIME_FORMAT = 'MMM d, yyyy h:mm a';
export const TIME_FORMAT = 'h:mm a';
export const ISO_DATE_FORMAT = 'yyyy-MM-dd';
export const ISO_DATETIME_FORMAT = "yyyy-MM-dd'T'HH:mm:ss";

/** Timezones */
export const COMMON_TIMEZONES = [
  { value: 'UTC', label: 'UTC' },
  { value: 'America/New_York', label: 'Eastern Time (ET)' },
  { value: 'America/Chicago', label: 'Central Time (CT)' },
  { value: 'America/Denver', label: 'Mountain Time (MT)' },
  { value: 'America/Los_Angeles', label: 'Pacific Time (PT)' },
  { value: 'America/Anchorage', label: 'Alaska Time (AKT)' },
  { value: 'Pacific/Honolulu', label: 'Hawaii Time (HT)' },
  { value: 'Europe/London', label: 'London (GMT/BST)' },
  { value: 'Europe/Paris', label: 'Paris (CET/CEST)' },
  { value: 'Asia/Tokyo', label: 'Tokyo (JST)' },
  { value: 'Asia/Shanghai', label: 'Shanghai (CST)' },
  { value: 'Australia/Sydney', label: 'Sydney (AEST/AEDT)' },
];

/** Business types */
export const BUSINESS_TYPES = [
  { value: 'medical', label: 'Medical Practice' },
  { value: 'dental', label: 'Dental Office' },
  { value: 'legal', label: 'Law Firm' },
  { value: 'real_estate', label: 'Real Estate' },
  { value: 'home_services', label: 'Home Services' },
  { value: 'automotive', label: 'Automotive' },
  { value: 'beauty', label: 'Beauty & Wellness' },
  { value: 'fitness', label: 'Fitness & Gym' },
  { value: 'education', label: 'Education' },
  { value: 'consulting', label: 'Consulting' },
  { value: 'other', label: 'Other' },
];

/** Appointment statuses */
export const APPOINTMENT_STATUSES = [
  { value: 'pending', label: 'Pending', color: 'warning' },
  { value: 'confirmed', label: 'Confirmed', color: 'primary' },
  { value: 'completed', label: 'Completed', color: 'success' },
  { value: 'cancelled', label: 'Cancelled', color: 'destructive' },
  { value: 'no-show', label: 'No Show', color: 'destructive' },
] as const;

export const APPOINTMENT_STATUS_COLORS = {
  pending: 'warning',
  confirmed: 'primary',
  completed: 'success',
  cancelled: 'destructive',
  'no-show': 'destructive',
} as const;

/** Call statuses */
export const CALL_STATUSES = [
  { value: 'completed', label: 'Completed', color: 'success' },
  { value: 'missed', label: 'Missed', color: 'destructive' },
  { value: 'voicemail', label: 'Voicemail', color: 'warning' },
  { value: 'failed', label: 'Failed', color: 'destructive' },
] as const;

export const CALL_DIRECTIONS = [
  { value: 'incoming', label: 'Incoming' },
  { value: 'outgoing', label: 'Outgoing' },
] as const;

/** Sentiments */
export const SENTIMENTS = [
  { value: 'positive', label: 'Positive', color: 'success' },
  { value: 'neutral', label: 'Neutral', color: 'warning' },
  { value: 'negative', label: 'Negative', color: 'destructive' },
] as const;

/** User roles */
export const USER_ROLES = [
  { value: 'owner', label: 'Owner', permissions: ['all'] },
  { value: 'admin', label: 'Admin', permissions: ['manage_users', 'manage_settings', 'view_analytics', 'manage_appointments', 'manage_customers', 'manage_calls'] },
  { value: 'staff', label: 'Staff', permissions: ['view_appointments', 'manage_appointments', 'view_customers', 'view_calls'] },
  { value: 'viewer', label: 'Viewer', permissions: ['view_appointments', 'view_customers', 'view_calls'] },
] as const;

/** Languages */
export const LANGUAGES = [
  { value: 'en', label: 'English' },
  { value: 'es', label: 'Spanish' },
  { value: 'fr', label: 'French' },
  { value: 'de', label: 'German' },
  { value: 'it', label: 'Italian' },
  { value: 'pt', label: 'Portuguese' },
  { value: 'zh', label: 'Chinese' },
  { value: 'ja', label: 'Japanese' },
  { value: 'ko', label: 'Korean' },
];

/** Genders */
export const GENDERS = [
  { value: 'male', label: 'Male' },
  { value: 'female', label: 'Female' },
  { value: 'other', label: 'Other' },
  { value: 'prefer_not_to_say', label: 'Prefer not to say' },
] as const;

/** Intent categories */
export const CALL_INTENTS = [
  'booking',
  'cancellation',
  'rescheduling',
  'inquiry',
  'complaint',
  'confirmation',
  'follow_up',
  'emergency',
  'billing',
  'general',
] as const;

/** Chart colors */
export const CHART_COLORS = [
  '#3b82f6', // primary
  '#22c55e', // success
  '#f59e0b', // warning
  '#ef4444', // destructive
  '#8b5cf6', // purple
  '#06b6d4', // cyan
  '#f97316', // orange
  '#ec4899', // pink
];

/** Toast durations */
export const TOAST_DURATION = {
  short: 2000,
  normal: 4000,
  long: 6000,
} as const;

/** Animation durations */
export const ANIMATION_DURATION = {
  fast: 100,
  normal: 200,
  slow: 300,
} as const;

/** Breakpoints (matching Tailwind) */
export const BREAKPOINTS = {
  sm: 640,
  md: 768,
  lg: 1024,
  xl: 1280,
  '2xl': 1536,
} as const;

/** Local storage keys */
export const STORAGE_KEYS = {
  auth_token: 'access_token',
  user_id: 'user_id',
  business_id: 'business_id',
  theme: 'theme',
  sidebar_collapsed: 'sidebar_collapsed',
  recent_searches: 'recent_searches',
} as const;

/** Cookie options */
export const COOKIE_OPTIONS = {
  expires: 7,
  secure: process.env.NODE_ENV === 'production',
  sameSite: 'lax' as const,
};

/** Regex patterns */
export const REGEX = {
  email: /^[^\s@]+@[^\s@]+\.[^\s@]+$/,
  phone: /^[\+]?[(]?[0-9]{3}[)]?[-\s\.]?[0-9]{3}[-\s\.]?[0-9]{4,6}$/,
  url: /^(https?:\/\/)?([\da-z\.-]+)\.([a-z\.]{2,6})([\/\w \.-]*)*\/?$/,
  slug: /^[a-z0-9]+(?:-[a-z0-9]+)*$/,
} as const;

/** Default values */
export const DEFAULTS = {
  appointment_duration: 30,
  booking_advance_days: 60,
  cancellation_notice_hours: 24,
  reminder_before_hours: 2,
  ai_temperature: 0.7,
  page_size: DEFAULT_PAGE_SIZE,
} as const;

/** Error codes */
export const ERROR_CODES = {
  UNAUTHORIZED: 'UNAUTHORIZED',
  FORBIDDEN: 'FORBIDDEN',
  NOT_FOUND: 'NOT_FOUND',
  VALIDATION_ERROR: 'VALIDATION_ERROR',
  CONFLICT: 'CONFLICT',
  RATE_LIMITED: 'RATE_LIMITED',
  SERVER_ERROR: 'SERVER_ERROR',
  NETWORK_ERROR: 'NETWORK_ERROR',
} as const;

/** Route paths */
export const ROUTES = {
  root: '/',
  dashboard: '/dashboard',
  bookings: '/bookings',
  bookings_new: '/bookings/new',
  bookings_detail: (id: number) => `/bookings/${id}`,
  bookings_edit: (id: number) => `/bookings/${id}/edit`,
  customers: '/customers',
  customers_new: '/customers/new',
  customers_detail: (id: number) => `/customers/${id}`,
  customers_edit: (id: number) => `/customers/${id}/edit`,
  calls: '/calls',
  calls_detail: (id: number) => `/calls/${id}`,
  calls_transcript: (id: number) => `/calls/${id}/transcript`,
  analytics: '/analytics',
  staff: '/staff',
  staff_new: '/staff/new',
  staff_detail: (id: number) => `/staff/${id}`,
  staff_edit: (id: number) => `/staff/${id}/edit`,
  settings: '/settings',
  profile: '/profile',
  api_settings: '/api-settings',
  billing: '/billing',
  login: '/auth/login',
  register: '/auth/register',
  forgot_password: '/auth/forgot-password',
  reset_password: '/auth/reset-password',
} as const;