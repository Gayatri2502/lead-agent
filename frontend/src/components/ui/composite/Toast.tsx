'use client';

import React from 'react';
import { Toaster as SonnerToaster, toast } from 'sonner';

interface ToastOptions {
  description?: string;
  action?: { label: string; onClick: () => void };
  [key: string]: any;
}

interface ToastProps extends ToastOptions {
  title: string;
  description?: string;
  action?: { label: string; onClick: () => void };
}

export function useToast() {
  const showToast = React.useCallback(
    ({ title, description, action, ...options }: ToastProps) => {
      return toast(title, {
        description,
        action: action
          ? {
              label: action.label,
              onClick: action.onClick,
            }
          : undefined,
        ...options,
      });
    },
    []
  );

  const success = React.useCallback(
    (title: string, options?: Omit<ToastProps, 'title'>) => {
      return toast.success(title, options);
    },
    []
  );

  const error = React.useCallback(
    (title: string, options?: Omit<ToastProps, 'title'>) => {
      return toast.error(title, options);
    },
    []
  );

  const loading = React.useCallback(
    (title: string, options?: Omit<ToastProps, 'title'>) => {
      return toast.loading(title, options);
    },
    []
  );

  const promise = React.useCallback(
    <T,>(
      promise: Promise<T>,
      messages: { loading: string; success: string | ((data: T) => string); error: string | ((error: Error) => string) },
      options?: Omit<ToastOptions, 'description'>
    ) => {
      return toast.promise(promise, { ...messages, ...options });
    },
    []
  );

  const dismiss = React.useCallback((toastId?: string | number) => {
    return toast.dismiss(toastId);
  }, []);

  return { 
    toast: showToast, 
    success, 
    error, 
    loading, 
    promise, 
    dismiss 
  } as const;
}

export function Toaster() {
  return (
    <SonnerToaster
      position="bottom-right"
      theme="dark"
      toastOptions={{
        classNames: {
          toast: 'bg-card border border-border',
          description: 'text-muted-foreground',
          actionButton: 'bg-primary text-primary-foreground hover:bg-primary-hover',
          closeButton: 'text-muted-foreground hover:text-foreground',
        },
      }}
    />
  );
}

export { toast };