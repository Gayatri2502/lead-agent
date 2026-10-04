'use client';

import { useCallback, useState } from 'react';

/**
 * Toggle boolean state
 */
export function useToggle(initialValue = false): [boolean, () => void, (value: boolean) => void] {
  const [value, setValue] = useState(initialValue);

  const toggle = useCallback(() => setValue((v) => !v), []);
  const set = useCallback((v: boolean) => setValue(v), []);

  return [value, toggle, set];
}

/**
 * Manage a set of selected items
 */
export function useSelection<T>(initialSelection: Set<T> = new Set()): [
  Set<T>,
  (item: T) => void,
  (item: T) => boolean,
  () => void,
  (items: T[]) => void
] {
  const [selection, setSelection] = useState<Set<T>>(initialSelection);

  const toggle = useCallback((item: T) => {
    setSelection((prev) => {
      const next = new Set(prev);
      if (next.has(item)) {
        next.delete(item);
      } else {
        next.add(item);
      }
      return next;
    });
  }, []);

  const isSelected = useCallback(
    (item: T) => selection.has(item),
    [selection]
  );

  const clear = useCallback(() => setSelection(new Set()), []);

  const selectAll = useCallback((items: T[]) => {
    setSelection(new Set(items));
  }, []);

  return [selection, toggle, isSelected, clear, selectAll];
}

/**
 * Manage open/close state for modals, drawers, etc.
 */
export function useDisclosure(initialOpen = false): [
  boolean,
  () => void,
  () => void,
  () => void
] {
  const [isOpen, setIsOpen] = useState(initialOpen);

  const open = useCallback(() => setIsOpen(true), []);
  const close = useCallback(() => setIsOpen(false), []);
  const toggle = useCallback(() => setIsOpen((prev) => !prev), []);

  return [isOpen, open, close, toggle];
}

/**
 * Manage active tab/index state
 */
export function useTabs<T extends string>(initialTab: T, tabs: T[]): [
  T,
  (tab: T) => void,
  (direction: 'next' | 'prev') => void
] {
  const [activeTab, setActiveTab] = useState<T>(initialTab);

  const setTab = useCallback((tab: T) => {
    if (tabs.includes(tab)) {
      setActiveTab(tab);
    }
  }, [tabs]);

  const navigate = useCallback(
    (direction: 'next' | 'prev') => {
      const currentIndex = tabs.indexOf(activeTab);
      if (currentIndex === -1) return;

      const nextIndex = direction === 'next' ? currentIndex + 1 : currentIndex - 1;
      if (nextIndex >= 0 && nextIndex < tabs.length) {
        setActiveTab(tabs[nextIndex]);
      }
    },
    [activeTab, tabs]
  );

  return [activeTab, setTab, navigate];
}