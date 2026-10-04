'use client';

import { useState } from 'react';
import { useDebounce } from '@/hooks/useDebounce';
import { useCustomers } from '@/services/queries';
import { DataTable, Column, RowAction } from '@/components/ui/patterns/DataTable';
import { Card, CardContent } from '@/components/ui/composite/Card';
import { Input } from '@/components/ui/composite/Input';
import { Select, SelectOption } from '@/components/ui/composite/Select';
import { Badge } from '@/components/ui/composite/Badge';
import { Avatar } from '@/components/ui/composite/Avatar';
import { Search, Edit, Eye, Trash2 } from 'lucide-react';
import { formatDate, getInitials } from '@/lib/utils';
import type { Customer } from '@/types';

const columns: Column<Customer>[] = [
  {
    key: 'name',
    header: 'Customer',
    accessor: (customer) => (
      <div className="flex items-center gap-3">
        <Avatar
          fallback={getInitials(customer.first_name, customer.last_name)}
          size="sm"
        />
        <div>
          <p className="font-medium">{customer.first_name} {customer.last_name}</p>
          <p className="text-sm text-muted-foreground">{customer.email || 'No email'}</p>
        </div>
      </div>
    ),
    cellClassName: 'max-w-xs',
  },
  {
    key: 'phone',
    header: 'Phone',
    accessor: 'phone',
  },
  {
    key: 'status',
    header: 'Status',
    accessor: (customer) => (
      <Badge
        variant={customer.is_returning ? 'success' : 'default'}
        dot
      >
        {customer.is_returning ? 'Returning' : 'New'}
      </Badge>
    ),
  },
  {
    key: 'last_appointment',
    header: 'Last Visit',
    accessor: (customer) =>
      customer.last_appointment ? formatDate(customer.last_appointment) : 'Never',
  },
  {
    key: 'created_at',
    header: 'Joined',
    accessor: (customer) => formatDate(customer.created_at),
  },
];

const filterOptions: SelectOption[] = [
  { value: 'all', label: 'All Customers' },
  { value: 'returning', label: 'Returning' },
  { value: 'new', label: 'New' },
];

const rowActions: RowAction<Customer>[] = [
  { label: 'View Details', icon: <Eye className="h-4 w-4" />, onClick: (customer) => window.location.href = `/customers/${customer.id}` },
  { label: 'Edit', icon: <Edit className="h-4 w-4" />, onClick: (customer) => window.location.href = `/customers/${customer.id}/edit` },
  { label: 'Delete', icon: <Trash2 className="h-4 w-4" />, destructive: true, onClick: () => {
    if (confirm('Delete this customer?')) {
      alert('Customer deleted');
    }
  }},
];

export default function CustomersTable() {
  const [searchQuery, setSearchQuery] = useState('');
  const [filterType, setFilterType] = useState('all');
  const debouncedSearch = useDebounce(searchQuery, 300);

  const { data: customersResponse, isLoading } = useCustomers(1, {
    search: debouncedSearch,
    type: filterType !== 'all' ? filterType : undefined,
    page: 1,
    page_size: 20,
  });

  const customers = (customersResponse as { data: Customer[] } | undefined)?.data || [];

  return (
    <div className="space-y-6 animate-in fade-in-0 zoom-in-95">
      {/* Search and Filters */}
      <Card>
        <CardContent className="p-4">
          <div className="flex flex-col sm:flex-row gap-4">
            <div className="relative flex-1">
              <Search className="absolute left-3 top-1/2 -translate-y-1/2 h-4 w-4 text-muted-foreground" />
              <Input
                placeholder="Search customers by name, phone, or email..."
                value={searchQuery}
                onChange={(e) => setSearchQuery(e.target.value)}
                leftIcon={<Search className="h-4 w-4" />}
                className="pl-10"
              />
            </div>
            <Select
              value={filterType}
              onChange={(e) => setFilterType(e.target.value)}
              options={filterOptions}
              className="w-full sm:w-48"
            />
          </div>
        </CardContent>
      </Card>

      {/* Customers Table */}
      <DataTable
        columns={columns}
        data={customers}
        keyAccessor={(customer) => customer.id}
        rowActions={rowActions}
        loading={isLoading}
        emptyState={
          <div className="text-center py-12">
            <Search className="h-12 w-12 text-muted-foreground mx-auto mb-4" />
            <p className="text-muted-foreground text-lg">No customers found</p>
            <p className="text-sm text-muted-foreground">
              {searchQuery || filterType !== 'all'
                ? 'Try adjusting your search or filters'
                : 'Get started by adding your first customer'}
            </p>
          </div>
        }
      />
    </div>
  );
}