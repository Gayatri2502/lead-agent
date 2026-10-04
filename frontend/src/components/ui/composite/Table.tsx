'use client';

import React from 'react';
import { cn } from '@/lib/utils';
import { Checkbox } from './Checkbox';

export interface Column<T> {
  key: string;
  header: string;
  accessor: keyof T | ((item: T) => React.ReactNode);
  width?: string;
  minWidth?: string;
  align?: 'left' | 'center' | 'right';
  sortable?: boolean;
  filterable?: boolean;
  render?: (value: any, item: T) => React.ReactNode;
  cellClassName?: string;
  headerClassName?: string;
}

export interface PaginationConfig {
  page: number;
  pageSize: number;
  total: number;
  onPageChange: (page: number) => void;
  onPageSizeChange?: (pageSize: number) => void;
  pageSizeOptions?: number[];
  showPageSizeSelector?: boolean;
}

export interface SelectionConfig<T> {
  selected: Set<string | number>;
  onSelectionChange: (selected: Set<string | number>) => void;
  getKey: (item: T) => string | number;
}

interface TableProps<T> {
  columns: Column<T>[];
  data: T[];
  keyAccessor: (item: T) => string | number;
  sortable?: boolean;
  filterable?: boolean;
  pagination?: PaginationConfig;
  selection?: SelectionConfig<T>;
  emptyState?: React.ReactNode;
  loading?: boolean;
  rowClassName?: (item: T) => string;
  onRowClick?: (item: T) => void;
  className?: string;
}

function Table<T>({
  columns,
  data,
  keyAccessor,
  sortable = false,
  filterable = false,
  pagination,
  selection,
  emptyState,
  loading,
  rowClassName,
  onRowClick,
  className,
}: TableProps<T>) {
  const [sortConfig, setSortConfig] = React.useState<{ key: string; direction: 'asc' | 'desc' } | null>(null);
  const [columnFilters, setColumnFilters] = React.useState<Record<string, string>>({});

  const sortedData = React.useMemo(() => {
    let result = [...data];

    if (sortConfig && sortable) {
      const { key, direction } = sortConfig;
      result.sort((a, b) => {
        const aVal = a[key as keyof T];
        const bVal = b[key as keyof T];
        if (aVal < bVal) return direction === 'asc' ? -1 : 1;
        if (aVal > bVal) return direction === 'asc' ? 1 : -1;
        return 0;
      });
    }

    return result;
  }, [data, sortConfig, sortable]);

  const filteredData = React.useMemo(() => {
    if (!filterable || Object.keys(columnFilters).length === 0) return sortedData;

    return sortedData.filter((item) => {
      return Object.entries(columnFilters).every(([key, filterValue]) => {
        const column = columns.find((c) => c.key === key);
        if (!column?.filterable) return true;
        const value = column.accessor;
        const cellValue = typeof value === 'function' ? value(item) : item[value as keyof T];
        return String(cellValue).toLowerCase().includes(filterValue.toLowerCase());
      });
    });
  }, [sortedData, columnFilters, columns, filterable]);

  const paginatedData = pagination
    ? filteredData.slice((pagination.page - 1) * pagination.pageSize, pagination.page * pagination.pageSize)
    : filteredData;

  const handleSort = (key: string) => {
    if (!sortable) return;
    setSortConfig((prev) => ({
      key,
      direction: prev?.key === key && prev.direction === 'asc' ? 'desc' : 'asc',
    }));
  };

  const handleFilterChange = (key: string, value: string) => {
    setColumnFilters((prev) => {
      if (!value) {
        const next = { ...prev };
        delete next[key];
        return next;
      }
      return { ...prev, [key]: value };
    });
    if (pagination) pagination.onPageChange(1);
  };

  const isAllSelected = selection && data.length > 0 && selection.selected.size === data.length;
  const isIndeterminate = selection && selection.selected.size > 0 && selection.selected.size < data.length;

  if (loading) {
    return (
      <div className={cn('rounded-lg border border-border', className)}>
        <div className="overflow-x-auto">
          <table className="w-full" role="table">
            <thead>
              <tr className="border-b border-border bg-muted">
                {columns.map((column) => (
                  <th
                    key={column.key}
                    className={cn(
                      'px-4 py-3 text-left text-sm font-semibold text-muted-foreground',
                      column.headerClassName
                    )}
                    style={{ width: column.width, minWidth: column.minWidth }}
                  >
                    {column.header}
                  </th>
                ))}
              </tr>
            </thead>
            <tbody>
              {Array.from({ length: 5 }).map((_, i) => (
                <tr key={i} className="border-b border-border animate-pulse">
                  {columns.map((column) => (
                    <td
                      key={column.key}
                      className={cn('px-4 py-4', column.cellClassName)}
                      style={{ width: column.width, minWidth: column.minWidth }}
                    >
                      <div className="h-4 bg-muted rounded w-3/4" />
                    </td>
                  ))}
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    );
  }

  if (filteredData.length === 0) {
    return (
      <div className={cn('rounded-lg border border-border', className)}>
        <div className="flex items-center justify-center py-12">
          {emptyState || (
            <div className="text-center">
              <p className="text-muted-foreground">No data found</p>
            </div>
          )}
        </div>
      </div>
    );
  }

  return (
    <div className={cn('rounded-lg border border-border', className)}>
      <div className="overflow-x-auto">
        <table className="w-full" role="table">
          <thead>
            <tr className="border-b border-border bg-muted">
              {selection && (
                <th className="px-4 py-3 text-left">
                  <Checkbox
                    label={isAllSelected ? 'Deselect all' : 'Select all'}
                    className="sr-only"
                    checked={isAllSelected}
                    onChange={() => {
                      if (isAllSelected) {
                        selection.onSelectionChange(new Set());
                      } else {
                        selection.onSelectionChange(new Set(data.map(selection.getKey)));
                      }
                    }}
                    indeterminate={isIndeterminate}
                    aria-label={isAllSelected ? 'Deselect all' : 'Select all'}
                  />
                </th>
              )}
              {columns.map((column) => (
                <th
                  key={column.key}
                  className={cn(
                    'px-4 py-3 text-left text-sm font-semibold text-muted-foreground',
                    column.sortable && 'cursor-pointer select-none hover:text-foreground',
                    column.align === 'center' && 'text-center',
                    column.align === 'right' && 'text-right',
                    column.headerClassName
                  )}
                  style={{ width: column.width, minWidth: column.minWidth }}
                  onClick={() => column.sortable && handleSort(column.key)}
                  aria-sort={
                    sortConfig?.key === column.key
                      ? sortConfig.direction === 'asc'
                        ? 'ascending'
                        : 'descending'
                      : 'none'
                  }
                >
                  <div className="flex items-center gap-1.5">
                    {column.header}
                    {column.sortable && sortConfig?.key === column.key && (
                      <span aria-hidden="true">
                        {sortConfig.direction === 'asc' ? '↑' : '↓'}
                      </span>
                    )}
                  </div>
                </th>
              ))}
            </tr>
            {filterable && (
              <tr className="border-b border-border bg-muted/50">
                {selection && <th className="px-4 py-2" />}
                {columns.map((column) => (
                  <th
                    key={`${column.key}-filter`}
                    className={cn('px-4 py-2', column.align === 'center' && 'text-center', column.align === 'right' && 'text-right')}
                    style={{ width: column.width, minWidth: column.minWidth }}
                  >
                    {column.filterable ? (
                      <input
                        type="text"
                        placeholder={`Filter ${column.header}...`}
                        value={columnFilters[column.key] || ''}
                        onChange={(e) => handleFilterChange(column.key, e.target.value)}
                        className="w-full h-8 px-2 text-xs rounded border border-border bg-background focus:outline-none focus:ring-1 focus:ring-ring"
                        aria-label={`Filter ${column.header}`}
                      />
                    ) : null}
                  </th>
                ))}
              </tr>
            )}
          </thead>
          <tbody>
            {paginatedData.map((item) => {
              const key = keyAccessor(item);
              const isSelected = selection?.selected.has(key);
              return (
                <tr
                  key={key}
                  className={cn(
                    'border-b border-border transition-colors',
                    'hover:bg-muted/50',
                    isSelected && 'bg-primary/5',
                    rowClassName?.(item)
                  )}
                  onClick={() => onRowClick?.(item)}
                  style={onRowClick ? { cursor: 'pointer' } : undefined}
                >
                  {selection && (
                    <td className="px-4 py-4">
                      <Checkbox
                        label={isSelected ? 'Deselect row' : 'Select row'}
                        className="sr-only"
                        checked={isSelected}
                        onChange={() => {
                          const next = new Set(selection.selected);
                          if (next.has(key)) next.delete(key);
                          else next.add(key);
                          selection.onSelectionChange(next);
                        }}
                        aria-label={isSelected ? 'Deselect row' : 'Select row'}
                      />
                    </td>
                  )}
                  {columns.map((column) => {
                    const value = column.accessor;
                    const cellValue = typeof value === 'function' ? value(item) : item[value as keyof T];
                    const rendered = column.render ? column.render(cellValue, item) : cellValue;
                    return (
                      <td
                        key={column.key}
                        className={cn(
                          'px-4 py-4 text-sm',
                          column.align === 'center' && 'text-center',
                          column.align === 'right' && 'text-right',
                          column.cellClassName
                        )}
                        style={{ width: column.width, minWidth: column.minWidth }}
                      >
                        {React.isValidElement(rendered) ? rendered : String(rendered)}
                      </td>
                    );
                  })}
                </tr>
              );
            })}
          </tbody>
        </table>
      </div>
      {pagination && (
        <div className="flex flex-col sm:flex-row items-center justify-between gap-4 p-4 border-t border-border">
          <div className="flex items-center gap-2 text-sm text-muted-foreground">
            <span>
              Showing{' '}
              <strong>{(pagination.page - 1) * pagination.pageSize + 1}</strong>{' '}
              to{' '}
              <strong>{Math.min(pagination.page * pagination.pageSize, pagination.total)}</strong>{' '}
              of <strong>{pagination.total}</strong> results
            </span>
            {pagination.showPageSizeSelector && pagination.pageSizeOptions && (
              <>
                <span>|</span>
                <select
                  value={pagination.pageSize}
                  onChange={(e) => pagination.onPageSizeChange?.(Number(e.target.value))}
                  className="h-8 px-2 text-sm rounded border border-border bg-background focus:outline-none focus:ring-1 focus:ring-ring"
                  aria-label="Results per page"
                >
                  {pagination.pageSizeOptions.map((size) => (
                    <option key={size} value={size}>
                      {size} / page
                    </option>
                  ))}
                </select>
              </>
            )}
          </div>
          <div className="flex items-center gap-2">
            <button
              onClick={() => pagination.onPageChange(pagination.page - 1)}
              disabled={pagination.page === 1}
              className="h-8 px-3 text-sm rounded border border-border hover:bg-muted disabled:opacity-50 disabled:cursor-not-allowed"
              aria-label="Previous page"
            >
              Previous
            </button>
            <div className="flex items-center gap-1">
              {Array.from({ length: Math.min(5, Math.ceil(pagination.total / pagination.pageSize)) }, (_, i) => {
                const pageNum = i + 1;
                const showPage = pageNum === 1 || pageNum === Math.ceil(pagination.total / pagination.pageSize) || Math.abs(pageNum - pagination.page) <= 1;
                if (!showPage) return <span key={`ellipsis-${pageNum}`} className="px-2 text-muted-foreground">...</span>;
                return (
                  <button
                    key={pageNum}
                    onClick={() => pagination.onPageChange(pageNum)}
                    className={cn(
                      'h-8 w-8 text-sm rounded',
                      pageNum === pagination.page
                        ? 'bg-primary text-primary-foreground'
                        : 'border border-border hover:bg-muted'
                    )}
                    aria-label={`Page ${pageNum}`}
                    aria-current={pageNum === pagination.page ? 'page' : undefined}
                  >
                    {pageNum}
                  </button>
                );
              })}
            </div>
            <button
              onClick={() => pagination.onPageChange(pagination.page + 1)}
              disabled={pagination.page >= Math.ceil(pagination.total / pagination.pageSize)}
              className="h-8 px-3 text-sm rounded border border-border hover:bg-muted disabled:opacity-50 disabled:cursor-not-allowed"
              aria-label="Next page"
            >
              Next
            </button>
          </div>
        </div>
      )}
    </div>
  );
}

Table.displayName = 'Table';

export { Table };