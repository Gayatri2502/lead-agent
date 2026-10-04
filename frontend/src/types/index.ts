/** Base entity types */
export interface BaseEntity {
  id: number;
  created_at: string;
  updated_at: string;
}

/** Business types */
export interface Business extends BaseEntity {
  name: string;
  business_type: string;
  description?: string;
  address?: string;
  phone?: string;
  email?: string;
  website?: string;
  timezone: string;
  logo_url?: string;
  working_hours: WorkingHours;
  holiday_schedule: Holiday[];
  appointment_duration: number;
  booking_advance_days: number;
  cancellation_notice_hours: number;
  is_active: boolean;
  is_verified: boolean;
}

export interface WorkingHours {
  [day: string]: {
    open: string;
    close: string;
    closed: boolean;
  };
}

export interface Holiday {
  date: string;
  name: string;
  recurring: boolean;
}

export interface BusinessSettings extends BaseEntity {
  business_id: number;
  ai_voice: string;
  ai_temperature: number;
  ai_system_prompt: string;
  enable_sms_reminders: boolean;
  enable_email_reminders: boolean;
  reminder_before_hours: number;
  sync_google_calendar: boolean;
  sync_outlook_calendar: boolean;
  crm_type: string;
  crm_integration_enabled: boolean;
  enable_video_calls: boolean;
  enable_custom_branding: boolean;
  enable_advanced_analytics: boolean;
}

/** User types */
export interface User extends BaseEntity {
  business_id: number;
  email: string;
  username: string;
  role: 'owner' | 'admin' | 'staff' | 'viewer';
  first_name: string;
  last_name: string;
  phone?: string;
  avatar_url?: string;
  is_active: boolean;
  is_verified: boolean;
  last_login?: string;
}

export interface Staff extends BaseEntity {
  business_id: number;
  user_id?: number;
  name: string;
  specialization?: string;
  phone?: string;
  email?: string;
  bio?: string;
  photo_url?: string;
  available_days: string[];
  available_hours: { start: string; end: string }[];
  is_active: boolean;
}

/** Customer types */
export interface Customer extends BaseEntity {
  business_id: number;
  first_name: string;
  last_name: string;
  phone: string;
  email?: string;
  address?: string;
  date_of_birth?: string;
  gender?: string;
  language: string;
  medical_history?: string;
  preferences: CustomerPreferences;
  is_returning: boolean;
  do_not_call: boolean;
  last_appointment?: string;
}

export interface CustomerPreferences {
  communication: ('sms' | 'email' | 'call')[];
  reminder_time?: string;
  preferred_staff?: number[];
  notes?: string;
}

/** Appointment types */
export interface Appointment extends BaseEntity {
  business_id: number;
  customer_id: number;
  staff_id?: number;
  service_id?: number;
  start_time: string;
  end_time: string;
  duration: number;
  status: 'pending' | 'confirmed' | 'completed' | 'cancelled' | 'no-show';
  reason?: string;
  notes?: string;
  special_requests?: string;
  booking_source: 'phone' | 'web' | 'walk-in' | 'api';
  reminder_sent: boolean;
  call_id?: number;
  customer?: Customer;
  staff?: Staff;
  service?: Service;
}

export interface Service extends BaseEntity {
  business_id: number;
  name: string;
  description?: string;
  duration: number;
  price: number;
  is_active: boolean;
}

/** Call types */
export interface Call extends BaseEntity {
  business_id: number;
  customer_id?: number;
  call_id: string;
  phone_number: string;
  direction: 'incoming' | 'outgoing';
  start_time: string;
  end_time?: string;
  duration?: number;
  recording_url?: string;
  recording_duration?: number;
  transcript?: string;
  transcript_language?: string;
  summary?: string;
  sentiment: 'positive' | 'neutral' | 'negative';
  intent?: string;
  status: 'completed' | 'missed' | 'voicemail' | 'failed';
  escalated_to_human: boolean;
  customer?: Customer;
}

/** Analytics types */
export interface AnalyticsOverview {
  total_calls: number;
  calls_today: number;
  avg_duration: number;
  appointments_booked: number;
  sentiment_score: number;
  conversion_rate: number;
  missed_calls: number;
  peak_hours: HourlyStats[];
}

export interface HourlyStats {
  hour: number;
  call_count: number;
  avg_sentiment: number;
}

export interface CallAnalytics {
  total: number;
  incoming: number;
  outgoing: number;
  missed: number;
  avg_duration: number;
  by_hour: HourlyStats[];
  by_sentiment: SentimentStats[];
  by_intent: IntentStats[];
}

export interface SentimentStats {
  sentiment: 'positive' | 'neutral' | 'negative';
  count: number;
  percentage: number;
}

export interface IntentStats {
  intent: string;
  count: number;
  percentage: number;
}

export interface AppointmentAnalytics {
  total: number;
  confirmed: number;
  completed: number;
  cancelled: number;
  no_show: number;
  by_status: { status: string; count: number }[];
  by_staff: { staff_id: number; staff_name: string; count: number }[];
  by_service: { service_id: number; service_name: string; count: number }[];
}

export interface CustomerAnalytics {
  total: number;
  new_this_month: number;
  returning: number;
  by_source: { source: string; count: number }[];
}

/** API types */
export interface ApiResponse<T> {
  data: T;
  meta?: {
    page?: number;
    page_size?: number;
    total?: number;
  };
}

export interface ApiError {
  detail: string;
  code?: string;
  field?: string;
}

export interface PaginatedResponse<T> {
  items: T[];
  total: number;
  page: number;
  page_size: number;
  total_pages: number;
}

/** Form types */
export interface LoginForm {
  email: string;
  password: string;
}

export interface RegisterForm {
  email: string;
  username: string;
  password: string;
  confirm_password: string;
  business_name: string;
  business_type: string;
}

/** Filter types */
export interface DateRangeFilter {
  start_date?: string;
  end_date?: string;
  preset?: 'today' | 'yesterday' | '7d' | '30d' | '90d' | 'custom';
}

export interface PaginationParams {
  page: number;
  page_size: number;
  sort_by?: string;
  sort_order?: 'asc' | 'desc';
}

export interface FilterParams extends PaginationParams {
  search?: string;
  status?: string;
  date_range?: DateRangeFilter;
  [key: string]: any;
}

/** Webhook types */
export interface WebhookEvent {
  id: string;
  event: string;
  timestamp: string;
  data: Record<string, any>;
}

export interface WebhookConfig {
  url: string;
  events: string[];
  secret: string;
  active: boolean;
}

/** Integration types */
export interface Integration {
  id: number;
  business_id: number;
  type: 'google_calendar' | 'outlook_calendar' | 'hubspot' | 'zoho' | 'custom';
  name: string;
  config: Record<string, any>;
  is_active: boolean;
  last_sync?: string;
  sync_status: 'idle' | 'syncing' | 'success' | 'error';
  error_message?: string;
}

/** Notification types */
export interface Notification {
  id: number;
  business_id: number;
  user_id?: number;
  type: 'info' | 'success' | 'warning' | 'error';
  title: string;
  message: string;
  read: boolean;
  action_url?: string;
  created_at: string;
}

/** Settings types */
export interface GeneralSettings {
  business_name: string;
  timezone: string;
  language: string;
  date_format: string;
  time_format: string;
}

export interface NotificationSettings {
  email_enabled: boolean;
  sms_enabled: boolean;
  push_enabled: boolean;
  appointment_reminders: boolean;
  appointment_confirmations: boolean;
  appointment_cancellations: boolean;
  daily_summary: boolean;
  weekly_report: boolean;
}

export interface AppearanceSettings {
  theme: 'dark' | 'light' | 'system';
  primary_color: string;
  logo_url?: string;
  favicon_url?: string;
}

/** API Key types */
export interface ApiKey {
  id: number;
  business_id: number;
  name: string;
  key: string;
  secret: string;
  scopes: string[];
  is_active: boolean;
  last_used?: string;
}

/** Audit log types */
export interface AuditLog {
  id: number;
  business_id: number;
  user_id?: number;
  action: string;
  resource_type: string;
  resource_id?: number;
  old_values?: Record<string, any>;
  new_values?: Record<string, any>;
  ip_address?: string;
  user_agent?: string;
  created_at: string;
}