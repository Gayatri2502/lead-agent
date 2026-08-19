'use client';


import { ChangeEvent, useEffect, useState } from 'react';
import { apiClient } from '@/lib/api-client';
import { useAppStore } from '@/lib/store';

interface Customer {
  id: number;
  first_name: string;
  last_name: string;
  phone: string;
  email: string;
  created_at: string;
}

export default function CustomersPage() {
  const [customers, setCustomers] = useState<Customer[]>([]);
  const [filteredCustomers, setFilteredCustomers] = useState<Customer[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState('');
  const [searchQuery, setSearchQuery] = useState('');
  const [filterType, setFilterType] = useState('all');
  const [currentPage, setCurrentPage] = useState(1);
  const itemsPerPage = 6;

  const business = useAppStore((state: any) => state.business);

  useEffect(() => {
    fetchCustomers();
  }, [business?.id]);

  const fetchCustomers = async () => {
    try {
      setIsLoading(true);
      setError('');
      if (business?.id) {
        const response = await apiClient.getCustomers(business.id);
        setCustomers(response.data);
        setFilteredCustomers(response.data);
      }
    } catch (err) {
      setError('Failed to fetch customers');
      console.error(err);
    } finally {
      setIsLoading(false);
    }
  };

  const handleSearch = (query: string) => {
    setSearchQuery(query);
    filterCustomers(query, filterType);
    setCurrentPage(1);
  };

  const handleFilterChange = (type: string) => {
    setFilterType(type);
    filterCustomers(searchQuery, type);
    setCurrentPage(1);
  };

  const filterCustomers = (query: string, type: string) => {
    let filtered = customers;

    if (query) {
      filtered = filtered.filter((c: Customer) =>
        `${c.first_name} ${c.last_name}`.toLowerCase().includes(query.toLowerCase()) ||
        c.phone.includes(query) ||
        c.email.toLowerCase().includes(query.toLowerCase())
      );
    }

    if (type !== 'all') {
      if (type === 'returning') {
        filtered = filtered.filter(() => Math.random() > 0.5); // Mock returning filter
      } else if (type === 'new') {
        filtered = filtered.filter(() => Math.random() > 0.5); // Mock new filter
      }
    }

    setFilteredCustomers(filtered);
  };

  const paginatedCustomers = filteredCustomers.slice(
    (currentPage - 1) * itemsPerPage,
    currentPage * itemsPerPage
  );

  const totalPages = Math.ceil(filteredCustomers.length / itemsPerPage);

  const getInitials = (firstName: string, lastName: string) => {
    return `${firstName[0]}${lastName[0]}`.toUpperCase();
  };

  const handleViewCustomer = (customerId: number) => {
    // Navigate to customer detail page
    window.location.href = `/customers/${customerId}`;
  };

  const handleEditCustomer = (customerId: number) => {
    // Navigate to edit customer page
    window.location.href = `/customers/${customerId}/edit`;
  };

  return (
    <div className="space-y-6">
      <div className="flex justify-between items-center">
        <div>
          <h1 className="text-3xl font-bold">Customers</h1>
          <p className="text-muted mt-2">Manage customer profiles and interactions</p>
        </div>
        <button
          onClick={() => (window.location.href = '/customers/new')}
          className="px-4 py-2 rounded-lg bg-primary text-white hover:bg-primary/90 transition"
        >
          + New Customer
        </button>
      </div>

      {/* Search and Filters */}
      <div className="flex gap-4">
        <input
          type="text"
          placeholder="Search customers by name or phone..."
          value={searchQuery}
          onChange={(e: ChangeEvent<HTMLInputElement>) => handleSearch(e.target.value)}
          className="flex-1 px-4 py-2 rounded-lg bg-card border border-border text-foreground placeholder-muted focus:outline-none focus:border-primary"
        />
        <select
          value={filterType}
          onChange={(e: ChangeEvent<HTMLSelectElement>) => handleFilterChange(e.target.value)}
          className="px-4 py-2 rounded-lg bg-card border border-border text-foreground focus:outline-none focus:border-primary"
        >
          <option value="all">All Customers</option>
          <option value="returning">Returning</option>
          <option value="new">New</option>
        </select>
      </div>

      {/* Loading State */}
      {isLoading && (
        <div className="flex justify-center items-center py-12">
          <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-primary"></div>
        </div>
      )}

      {/* Error State */}
      {error && (
        <div className="bg-destructive/10 border border-destructive/50 text-destructive p-4 rounded-lg">
          {error}
        </div>
      )}

      {/* Customer Cards Grid */}
      {!isLoading && filteredCustomers.length === 0 && (
        <div className="text-center py-12">
          <p className="text-muted text-lg">No customers found</p>
        </div>
      )}

      {!isLoading && filteredCustomers.length > 0 && (
        <>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
            {paginatedCustomers.map((customer: Customer) => (
              <div
                key={customer.id}
                className="bg-card rounded-lg p-6 border border-border hover:border-primary/50 transition"
              >
                <div className="flex items-start justify-between mb-4">
                  <div className="w-12 h-12 rounded-full bg-primary/20 flex items-center justify-center">
                    <span className="font-bold text-sm">{getInitials(customer.first_name, customer.last_name)}</span>
                  </div>
                  <span className="px-2 py-1 text-xs rounded bg-success/20 text-success">Active</span>
                </div>
                <h3 className="font-semibold mb-1">
                  {customer.first_name} {customer.last_name}
                </h3>
                <p className="text-sm text-muted mb-3">{customer.phone}</p>
                <p className="text-sm text-muted mb-4">{customer.email}</p>
                <div className="text-sm text-muted mb-4 pb-4 border-b border-border">
                  <p>Joined: {new Date(customer.created_at).toLocaleDateString()}</p>
                  <p>Total appointments: --</p>
                </div>
                <div className="flex gap-2">
                  <button
                    onClick={() => handleViewCustomer(customer.id)}
                    className="flex-1 px-3 py-2 rounded text-sm bg-primary/10 text-primary hover:bg-primary/20 transition"
                  >
                    View
                  </button>
                  <button
                    onClick={() => handleEditCustomer(customer.id)}
                    className="flex-1 px-3 py-2 rounded text-sm border border-border hover:bg-card-foreground/5 transition"
                  >
                    Edit
                  </button>
                </div>
              </div>
            ))}
          </div>

          {/* Pagination */}
          {totalPages > 1 && (
            <div className="flex justify-between items-center">
              <p className="text-sm text-muted">
                Showing {(currentPage - 1) * itemsPerPage + 1} to{' '}
                {Math.min(currentPage * itemsPerPage, filteredCustomers.length)} of {filteredCustomers.length} customers
              </p>
              <div className="flex gap-2">
                <button
                  onClick={() => setCurrentPage(Math.max(1, currentPage - 1))}
                  disabled={currentPage === 1}
                  className="px-3 py-1 rounded border border-border hover:bg-card-foreground/5 transition disabled:opacity-50"
                >
                  Previous
                </button>
                {Array.from({ length: totalPages }, (_, i) => i + 1).map((page) => (
                  <button
                    key={page}
                    onClick={() => setCurrentPage(page)}
                    className={`px-3 py-1 rounded transition ${
                      page === currentPage
                        ? 'bg-primary text-white'
                        : 'border border-border hover:bg-card-foreground/5'
                    }`}
                  >
                    {page}
                  </button>
                ))}
                <button
                  onClick={() => setCurrentPage(Math.min(totalPages, currentPage + 1))}
                  disabled={currentPage === totalPages}
                  className="px-3 py-1 rounded border border-border hover:bg-card-foreground/5 transition disabled:opacity-50"
                >
                  Next
                </button>
              </div>
            </div>
          )}
        </>
      )}
    </div>
  );
}
