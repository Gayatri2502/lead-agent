'use client';

import React, { useEffect, useRef } from 'react';
import { Chart, registerables } from 'chart.js';
import { cn } from '@/lib/utils';

Chart.register(...registerables);

const DEFAULT_COLORS = [
  'rgb(59, 130, 246)',
  'rgb(34, 197, 94)',
  'rgb(245, 158, 11)',
  'rgb(239, 68, 68)',
  'rgb(139, 92, 246)',
  'rgb(6, 182, 212)',
  'rgb(249, 115, 22)',
  'rgb(236, 72, 153)',
];

interface PieChartDataPoint {
  label: string;
  value: number;
  color?: string;
}

interface PieChartProps {
  data: PieChartDataPoint[];
  height?: number;
  className?: string;
  showLegend?: boolean;
  legendPosition?: 'right' | 'bottom';
  cutout?: string | number;
}

export function PieChart({
  data,
  height = 300,
  className,
  showLegend = true,
  legendPosition = 'right',
  cutout = '60%',
}: PieChartProps) {
  const canvasRef = useRef<HTMLCanvasElement>(null);
  const chartRef = useRef<Chart<'doughnut'> | null>(null);

  const total = data.reduce((sum, d) => sum + d.value, 0);

  useEffect(() => {
    if (!canvasRef.current) return;

    const ctx = canvasRef.current.getContext('2d');
    if (!ctx) return;

    if (chartRef.current) {
      chartRef.current.destroy();
    }

    const colors = data.map((d, i) => d.color || DEFAULT_COLORS[i % DEFAULT_COLORS.length]);

    chartRef.current = new Chart(ctx, {
      type: 'doughnut',
      data: {
        labels: data.map((d) => d.label),
        datasets: [
          {
            data: data.map((d) => d.value),
            backgroundColor: colors,
            borderWidth: 0,
            spacing: 2,
          },
        ],
      },
      options: {
        cutout,
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
          legend: {
            display: showLegend,
            position: legendPosition,
            labels: {
              color: '#e5e5e5',
              font: { size: 12 },
              padding: 16,
              usePointStyle: true,
              pointStyle: 'circle',
            },
          },
          tooltip: {
            backgroundColor: '#1a1a1a',
            titleColor: '#ffffff',
            bodyColor: '#e5e5e5',
            borderColor: '#2a2a2a',
            borderWidth: 1,
            padding: 12,
            cornerRadius: 8,
            displayColors: true,
            callbacks: {
              label: (context) => {
                const value = context.parsed;
                const percentage = ((value / total) * 100).toFixed(1);
                return `${context.label}: ${value.toLocaleString()} (${percentage}%)`;
              },
            },
          },
        },
      },
    });

    return () => {
      chartRef.current?.destroy();
    };
  }, [data, cutout, showLegend, legendPosition]);

  return (
    <div className={cn('flex items-center justify-center gap-6', className)}>
      <div style={{ width: height, height }} role="img" aria-label="Pie chart">
        <canvas ref={canvasRef} className="w-full h-full" />
      </div>
      {showLegend && (
        <div className="space-y-2">
          {data.map((item, index) => (
            <div key={item.label} className="flex items-center gap-2">
              <span
                className="h-3 w-3 rounded-full flex-shrink-0"
                style={{ backgroundColor: item.color || DEFAULT_COLORS[index % DEFAULT_COLORS.length] }}
                aria-hidden="true"
              />
              <span className="text-sm truncate flex-1">{item.label}</span>
              <div className="flex items-center gap-1 ml-auto">
                <span className="font-mono text-sm text-foreground">{item.value.toLocaleString()}</span>
                <span className="text-sm text-muted-foreground">({((item.value / total) * 100).toFixed(1)}%)</span>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}