'use client';

import { useState } from 'react';
import { useAppointments, useUpdateAppointment, useCancelAppointment } from '@/services/queries';
import { PageHeader } from '@/components/ui/patterns/PageHeader';
import { DataTable, Column, RowAction } from '@/components/ui/patterns/DataTable';
import { Card, CardContent } from '@/components/ui/composite/Card';
import { Button } from '@/components/ui/composite/Button';
import { Input } from '@/components/ui/composite/Input';
import { Select, SelectOption } from '@/components/ui/composite/Select';
import { Badge } from '@/components/ui/composite/Badge';
import { useToast } from '@/components/ui/composite/Toast';
import { Plus, Search, Calendar, Edit, Eye, Trash2, CheckCircle, XCircle, RotateCcw } from 'lucide-react';
import { formatDate, formatTime, getStatusColor } from '@/lib/utils';
import type { Appointment } from '@/types';

const STATUS_OPTIONS: SelectOption[] = [
  { value: 'all', label: 'All Status' },
  { value: 'pending', label: 'Pending' },
  { value: 'confirmed', label: 'Confirmed' },
  { value: 'completed', label: 'Completed' },
  { value: 'cancelled', label: 'Cancelled' },
  { value: 'no-show', label: 'No Show' },
];

const columns: Column<Appointment>[] = [
  {
    key: 'customer',
    header: 'Customer',
    accessor: (appointment) => (
      <div>
        <p className="font-medium">
          {appointment.customer?.first_name} {appointment.customer?.last_name}
        </p>
        <p className="text-sm text-muted-foreground">{appointment.customer?.phone}</p>
      </div>
    ),
  },
  {
    key: 'datetime',
    header: 'Date & Time',
    accessor: (appointment) => (
      <div>
        <p className="font-medium">{formatDate(appointment.start_time)}</p>
        <p className="text-sm text-muted-foreground">
          {formatTime(appointment.start_time)} - {formatTime(appointment.end_time)}
        </p>
      </div>
    ),
  },
  {
    key: 'service',
    header: 'Service',
    accessor: (appointment) => appointment.service?.name || 'N/A',
  },
  {
    key: 'staff',
    header: 'Staff',
    accessor: (appointment) =>
      appointment.staff ? appointment.staff.name : 'Unassigned',
  },
  {
    key: 'status',
    header: 'Status',
    accessor: (appointment) => (
      <Badge variant={getStatusColor(appointment.status) as any}>
        {appointment.status.charAt(0).toUpperCase() + appointment.status.slice(1).replace('-', ' ')}
      </Badge>
    ),
  },
];

export default function BookingsPage() {
  const [searchQuery, setSearchQuery] = useState('');
  const [statusFilter, setStatusFilter] = useState('all');

  const { data: appointmentsResponse, isLoading } = useAppointments(1, {
    search: searchQuery,
    status: statusFilter !== 'all' ? statusFilter : undefined,
    page: 1,
    page_size: 20,
  });

  const updateMutation = useUpdateAppointment();
  const cancelMutation = useCancelAppointment();

  const { success } = useToast();

  const handleCreate = () => {
    window.location.href = '/bookings/new';
  };

  const appointments = appointmentsResponse?.data || [];

  const rowActions: RowAction<Appointment>[] = [
    { label: 'View Details', icon: <Eye className="h-4 w-4" />, onClick: (apt) => window.location.href = `/bookings/${apt.id}` },
    { label: 'Edit', icon: <Edit className="h-4 w-4" />, onClick: (apt) => window.location.href = `/bookings/${apt.id}/edit` },
{ label: 'Confirm', icon: <CheckCircle className="h-4 w-4" />, onClick: async (apt) => {
    if (apt.status === 'pending') {
      await updateMutation.mutateAsync({ id: apt.id, data: { status: 'confirmed' } });
      success('Appointment confirmed');
    }
  }},
  { label: 'Complete', icon: <CheckCircle className="h-4 w-4" />, onClick: async (apt) => {
    if (['confirmed', 'pending'].includes(apt.status)) {
      await updateMutation.mutateAsync({ id: apt.id, data: { status: 'completed' } });
      success('Appointment completed');
    }
  }},
    { label: 'Reschedule', icon: <RotateCcw className="h-4 w-4" />, onClick: () => {
      alert('Reschedule modal would open here');
    }},
  { label: 'Cancel', icon: <XCircle className="h-4 w-4" />, destructive: true, onClick: async (apt) => {
    if (!['cancelled', 'completed', 'no-show'].includes(apt.status)) {
      const reason = prompt('Cancellation reason:');
      if (reason) {
        await cancelMutation.mutateAsync({ id: apt.id, reason });
        success('Appointment cancelled');
      }
    }
  }},
  { label: 'Delete', icon: <Trash2 className="h-4 w-4" />, destructive: true, onClick: () => {
    if (confirm('Delete this appointment?')) {
      success('Appointment deleted');
    }
  }},
  ];

  return (
    <div className="space-y-6 animate-in fade-in-0 zoom-in-95">
      <PageHeader
        title="Appointments"
        description="Manage and schedule appointments"
        action={
          <Button onClick={handleCreate} leftIcon={<Plus className="h-4 w-4" />}>
            New Appointment
          </Button>
        }
      />

      {/* Search and Filters */}
      <Card>
        <CardContent className="p-4">
          <div className="flex flex-col sm:flex-row gap-4">
            <div className="relative flex-1">
              <Search className="absolute left-3 top-1/2 -translate-y-1/2 h-4 w-4 text-muted-foreground" />
              <Input
                placeholder="Search appointments..."
                value={searchQuery}
                onChange={(e) => setSearchQuery(e.target.value)}
                leftIcon={<Search className="h-4 w-4" />}
                className="pl-10"
              />
            </div>
            <Select
              value={statusFilter}
              onChange={(e) => setStatusFilter(e.target.value)}
              options={STATUS_OPTIONS}
              className="w-full sm:w-48"
            />
          </div>
        </CardContent>
      </Card>

      {/* Appointments Table */}
      <DataTable
        columns={columns}
        data={appointments}
        keyAccessor={(apt) => apt.id}
        rowActions={rowActions}
        loading={isLoading}
        emptyState={
          (
            <div className="text-center py-12">
              <Calendar className="h-12 w-12 text-muted-foreground mx-auto mb-4" />
              <p className="text-muted-foreground text-lg">No appointments found</p>
              <p className="text-sm text-muted-foreground">
                {searchQuery || statusFilter !== 'all'
                  ? 'Try adjusting your search or filters'
                  : 'Get started by creating your first appointment'}
              </p>
            </div>
          )
        }
      />
    </div>
  );
}