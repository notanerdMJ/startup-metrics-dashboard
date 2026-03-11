// frontend/src/lib/utils.ts
/**
 * Utility functions used across the frontend.
 * clsx + tailwind-merge = smart class name merging.
 */

import { clsx, type ClassValue } from 'clsx';
import { twMerge } from 'tailwind-merge';

// Merge Tailwind classes intelligently (avoids conflicts)
export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs));
}

// Format numbers as currency
export function formatCurrency(value: number): string {
  return new Intl.NumberFormat('en-US', {
    style: 'currency',
    currency: 'USD',
    minimumFractionDigits: 0,
    maximumFractionDigits: 0,
  }).format(value);
}

// Format numbers with commas
export function formatNumber(value: number): string {
  return new Intl.NumberFormat('en-US').format(value);
}

// Format percentage
export function formatPercent(value: number): string {
  return `${(value * 100).toFixed(1)}%`;
}

// Determine health color based on metric
export function getHealthColor(value: number, thresholds: { good: number; warning: number }): string {
  if (value >= thresholds.good) return 'text-emerald-500';
  if (value >= thresholds.warning) return 'text-amber-500';
  return 'text-red-500';
}