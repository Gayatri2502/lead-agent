'use client';

import React from 'react';
import { cn } from '@/lib/utils';
import { Table, Column, PaginationConfig, SelectionConfig } from '../composite/Table';
export type { Column, PaginationConfig, SelectionConfig };
import { Button } from '../composite';
import { Text } from '../primitives';

export interface BulkAction<T> {
  label: string;
  icon?: React.ReactNode;
  onClick: (items: T[]) => void;
  disabled?: (items: T[]) => boolean;
  variant?: 'primary' | 'destructive';
}

export interface RowAction<T> {
  label: string;
  icon?: React.ReactNode;
  onClick: (item: T) => void;
  disabled?: (item: T) => boolean;
  variant?: 'default' | 'destructive';
  destructive?: boolean;
}

interface DataTableProps<T> {
  columns: Column<T>[];
  data: T[];
  keyAccessor: (item: T) => string | number;
  toolbar?: React.ReactNode;
  bulkActions?: BulkAction<T>[];
  rowActions?: RowAction<T>[];
  detailPanel?: (item: T) => React.ReactNode;
  virtualized?: boolean;
  stickyHeader?: boolean;
  resizableColumns?: boolean;
  reorderableColumns?: boolean;
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

export function DataTable<T>({
  columns,
  data,
  keyAccessor,
  toolbar,
  bulkActions,
  rowActions,
  detailPanel,
  sortable = true,
  filterable = true,
  pagination,
  selection,
  emptyState,
  loading,
  rowClassName,
  onRowClick,
  className,
}: DataTableProps<T>) {
  const [expandedRows] = React.useState<Set<string | number>>(new Set());

  const selectedItems = selection
    ? data.filter((item) => selection.selected.has(selection.getKey(item)))
    : [];

  const handleBulkAction = (action: BulkAction<T>) => {
    if (action.disabled?.(selectedItems)) return;
    action.onClick(selectedItems);
  };

  const actionColumns = rowActions && rowActions.length > 0 ? [
    {
      key: 'actions',
      header: '',
      accessor: 'actions' as keyof T,
      width: '120px',
      render: () => null,
      cellClassName: 'text-right',
    },
  ] : [];

  const allColumns = [...columns, ...actionColumns];

  return (
    <div className={cn('space-y-4', className)}>
      {toolbar && (
        <div className="flex flex-col sm:flex-row gap-4">
          <div className="flex-1">{toolbar}</div>
          {bulkActions && bulkActions.length > 0 && selection && selectedItems.length > 0 && (
            <div className="flex items-center gap-2">
              <Text variant="label-sm" color="muted">
                {selectedItems.length} selected
              </Text>
              {bulkActions.map((action) => (
                <Button
                  key={action.label}
                  variant={action.variant || 'primary'}
                  size="sm"
                  onClick={() => handleBulkAction(action)}
                  disabled={action.disabled?.(selectedItems)}
                  leftIcon={action.icon}
                >
                  {action.label}
                </Button>
              ))}
            </div>
          )}
        </div>
      )}
      <Table
        columns={allColumns}
        data={data}
        keyAccessor={keyAccessor}
        sortable={sortable}
        filterable={filterable}
        pagination={pagination}
        selection={selection}
        emptyState={emptyState}
        loading={loading}
        rowClassName={rowClassName}
        onRowClick={onRowClick}
      />
      {detailPanel && expandedRows.size > 0 && (
        <div className="space-y-2">
          {Array.from(expandedRows).map((key) => {
            const item = data.find((d) => keyAccessor(d) === key);
            if (!item) return null;
            return (
              <div key={key} className="bg-muted/50 rounded-lg border border-border p-4 animate-in slide-in-from-top-2 fade-in">
                {detailPanel(item)}
              </div>
            );
          })}
        </div>
      )}
    </div>
  );
}