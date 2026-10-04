'use client';

import dynamic from 'next/dynamic';
import { PageHeader } from '@/components/ui/patterns/PageHeader';
import { Button } from '@/components/ui/composite/Button';
import { Plus } from 'lucide-react';

const CustomersTable = dynamic(() => import('./CustomersTable'), {
  loading: () => <div className="animate-pulse space-y-6"><div className="h-8 bg-muted rounded w-1/4" /></div>,
});

export default function CustomersPage() {
  const handleCreate = async () => {
    window.location.href = '/customers/new';
  };

  return (
    <div className="space-y-6 animate-in fade-in-0 zoom-in-95">
      <PageHeader
        title="Customers"
        description="Manage customer profiles and interactions"
        action={
          <Button onClick={handleCreate} leftIcon={<Plus className="h-4 w-4" />}>
            New Customer
          </Button>
        }
      />

      <CustomersTable />
    </div>
  );
}