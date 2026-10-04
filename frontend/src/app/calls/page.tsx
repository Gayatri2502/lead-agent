'use client';

import { useState } from 'react';
import { useCalls } from '@/services/queries';
import { PageHeader } from '@/components/ui/patterns/PageHeader';
import { DataTable, Column, RowAction } from '@/components/ui/patterns/DataTable';
import { Card, CardContent } from '@/components/ui/composite/Card';
import { Input } from '@/components/ui/composite/Input';
import { Select, SelectOption } from '@/components/ui/composite/Select';
import { Badge } from '@/components/ui/composite/Badge';
import { Search, Phone, Clock, FileText, Play, Eye, Trash2, Flag } from 'lucide-react';
import { formatDate, formatTime, formatDuration, getStatusColor } from '@/lib/utils';
import type { Call } from '@/types';

const CALL_STATUS_OPTIONS: SelectOption[] = [
  { value: 'all', label: 'All Calls' },
  { value: 'completed', label: 'Completed' },
  { value: 'missed', label: 'Missed' },
  { value: 'voicemail', label: 'Voicemail' },
  { value: 'failed', label: 'Failed' },
];

const CALL_DIRECTION_OPTIONS: SelectOption[] = [
  { value: 'all', label: 'All Calls' },
  { value: 'incoming', label: 'Incoming' },
  { value: 'outgoing', label: 'Outgoing' },
];

const rowActions: RowAction<Call>[] = [
  { label: 'Listen', icon: <Play className="h-4 w-4" />, onClick: (call) => {
    if (call.recording_url) {
      // Open audio player modal
      alert('Listen to recording');
    } else {
      alert('No recording available');
    }
  }},
  { label: 'View Transcript', icon: <FileText className="h-4 w-4" />, onClick: (call) => {
    window.location.href = `/calls/${call.id}/transcript`;
  }},
  { label: 'View Details', icon: <Eye className="h-4 w-4" />, onClick: (call) => {
    window.location.href = `/calls/${call.id}`;
  }},
  { label: 'Flag for Review', icon: <Flag className="h-4 w-4" />, onClick: () => {
    alert('Call flagged for review');
  }},
  { label: 'Delete', icon: <Trash2 className="h-4 w-4" />, destructive: true, onClick: () => {
    if (confirm('Delete this call record?')) {
      alert('Call deleted');
    }
  }},
];

const columns: Column<Call>[] = [
  {
    key: 'phone_number',
    header: 'Phone Number',
    accessor: (call) => (
      <div className="flex items-center gap-2">
        <Phone className="h-4 w-4 text-muted-foreground" />
        <span className="font-medium">{call.phone_number}</span>
        {call.customer && (
          <Badge variant="outline" className="ml-2">
            {call.customer.first_name} {call.customer.last_name}
          </Badge>
        )}
      </div>
    ),
  },
  {
    key: 'datetime',
    header: 'Date & Time',
    accessor: (call) => (
      <div>
        <p>{formatDate(call.start_time)}</p>
        <p className="text-sm text-muted-foreground">{formatTime(call.start_time)}</p>
      </div>
    ),
  },
  {
    key: 'duration',
    header: 'Duration',
    accessor: (call) => (call.duration ? formatDuration(call.duration) : '—'),
  },
  {
    key: 'direction',
    header: 'Direction',
    accessor: (call) => (
      <Badge variant={call.direction === 'incoming' ? 'info' : 'success'} dot>
        {call.direction === 'incoming' ? 'Incoming' : 'Outgoing'}
      </Badge>
    ),
  },
  {
    key: 'intent',
    header: 'Intent',
    accessor: (call) => (
      <Badge variant="outline">{call.intent || 'Unknown'}</Badge>
    ),
  },
  {
    key: 'sentiment',
    header: 'Sentiment',
    accessor: (call) => (
      <Badge variant={getStatusColor(call.sentiment) as any} dot>
        {call.sentiment.charAt(0).toUpperCase() + call.sentiment.slice(1)}
      </Badge>
    ),
  },
];

export default function CallsPage() {
  const [searchQuery, setSearchQuery] = useState('');
  const [statusFilter, setStatusFilter] = useState('all');
  const [directionFilter, setDirectionFilter] = useState('all');

  const { data: callsResponse, isLoading } = useCalls(1, {
    search: searchQuery,
    status: statusFilter !== 'all' ? statusFilter : undefined,
    direction: directionFilter !== 'all' ? directionFilter : undefined,
    page: 1,
    page_size: 20,
  });

  const calls = callsResponse?.data || [];

  // Stats
  const stats = [
    { label: 'Total Calls', value: callsResponse?.meta?.total || 0, icon: Phone, color: 'primary' },
    { label: 'This Month', value: calls.filter((c: Call) => new Date(c.start_time).getMonth() === new Date().getMonth()).length, icon: Calendar, color: 'success' },
    { label: 'Avg Duration', value: calls.length > 0 ? formatDuration(Math.round(calls.reduce((sum: number, c: Call) => sum + (c.duration || 0), 0) / calls.length)) : '0s', icon: Clock, color: 'warning' },
    { label: 'Positive Sentiment', value: calls.length > 0 ? `${Math.round(calls.filter((c: Call) => c.sentiment === 'positive').length / calls.length * 100)}%` : '0%', icon: Smile, color: 'success' },
  ];

  return (
    <div className="space-y-6 animate-in fade-in-0 zoom-in-95">
      <PageHeader
        title="Call History"
        description="Review and analyze incoming and outgoing calls"
      />

      {/* Stats */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
        {stats.map((stat, index) => (
          <Card key={index}>
            <CardContent className="p-6">
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-label text-muted-foreground">{stat.label}</p>
                  <p className="text-data-lg font-semibold">{stat.value}</p>
                </div>
                <div className="w-12 h-12 rounded-lg bg-primary/20 flex items-center justify-center">
                  <stat.icon className="h-6 w-6 text-primary" />
                </div>
              </div>
            </CardContent>
          </Card>
        ))}
      </div>

      {/* Filters */}
      <Card>
        <CardContent className="p-4">
          <div className="flex flex-col sm:flex-row gap-4">
            <div className="relative flex-1">
              <Search className="absolute left-3 top-1/2 -translate-y-1/2 h-4 w-4 text-muted-foreground" />
              <Input
                placeholder="Search by phone number or customer..."
                value={searchQuery}
                onChange={(e) => setSearchQuery(e.target.value)}
                leftIcon={<Search className="h-4 w-4" />}
                className="pl-10"
              />
            </div>
            <Select
              value={statusFilter}
              onChange={(e) => setStatusFilter(e.target.value)}
              options={CALL_STATUS_OPTIONS}
              className="w-full sm:w-40"
            />
            <Select
              value={directionFilter}
              onChange={(e) => setDirectionFilter(e.target.value)}
              options={CALL_DIRECTION_OPTIONS}
              className="w-full sm:w-40"
            />
          </div>
        </CardContent>
      </Card>

      {/* Calls Table */}
      <DataTable
        columns={columns}
        data={calls}
        keyAccessor={(call) => call.id}
        rowActions={rowActions}
        loading={isLoading}
        emptyState={
          <div className="text-center py-12">
            <Phone className="h-12 w-12 text-muted-foreground mx-auto mb-4" />
            <p className="text-muted-foreground text-lg">No calls found</p>
            <p className="text-sm text-muted-foreground">
              {searchQuery || statusFilter !== 'all' || directionFilter !== 'all'
                ? 'Try adjusting your search or filters'
                : 'Calls will appear here once you start receiving them'}
            </p>
          </div>
        }
      />
    </div>
  );
}

import { Calendar, Smile } from 'lucide-react';