'use client';

import React, { useEffect, useRef } from 'react';
import { Chart, registerables } from 'chart.js';
import { cn } from '@/lib/utils';

Chart.register(...registerables);

interface ChartDataPoint {
  x: number;
  y: number;
}

interface LineChartProps {
  data: ChartDataPoint[];
  label?: string;
  color?: string;
  height?: number;
  className?: string;
  showPoints?: boolean;
  showGrid?: boolean;
  tension?: number;
  fill?: boolean;
}

const CHART_COLORS = {
  primary: 'rgb(59, 130, 246)',
  success: 'rgb(34, 197, 94)',
  warning: 'rgb(245, 158, 11)',
  destructive: 'rgb(239, 68, 68)',
};

export function LineChart({
  data,
  label,
  color = 'primary',
  height = 300,
  className,
  showPoints = false,
  showGrid = false,
  tension = 0.4,
  fill = false,
}: LineChartProps) {
  const canvasRef = useRef<HTMLCanvasElement>(null);
  const chartRef = useRef<Chart<'line'> | null>(null);

  useEffect(() => {
    if (!canvasRef.current) return;

    const ctx = canvasRef.current.getContext('2d');
    if (!ctx) return;

    if (chartRef.current) {
      chartRef.current.destroy();
    }

    const chartColor = CHART_COLORS[color as keyof typeof CHART_COLORS] || CHART_COLORS.primary;

    chartRef.current = new Chart(ctx, {
      type: 'line',
      data: {
        datasets: [
          {
            label: label || '',
            data,
            borderColor: chartColor,
            backgroundColor: fill ? `${chartColor}20` : 'transparent',
            borderWidth: 2,
            pointRadius: showPoints ? 4 : 0,
            pointHoverRadius: 6,
            pointBackgroundColor: chartColor,
            pointBorderColor: '#000000',
            pointBorderWidth: 2,
            tension,
            fill,
          },
        ],
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        interaction: {
          intersect: false,
          mode: 'index',
        },
        plugins: {
          legend: {
            display: false,
          },
          tooltip: {
            backgroundColor: '#1a1a1a',
            titleColor: '#ffffff',
            bodyColor: '#e5e5e5',
            borderColor: '#2a2a2a',
            borderWidth: 1,
            padding: 12,
            cornerRadius: 8,
            displayColors: false,
            callbacks: {
              label: (context) => {
                const value = context.parsed.y;
                return `${label || 'Value'}: ${value !== null ? value.toLocaleString() : 'N/A'}`;
              },
            },
          },
        },
        scales: {
          x: {
            display: true,
            grid: {
              display: showGrid,
              color: '#2a2a2a',
            },
            ticks: {
              color: '#737373',
              font: { size: 11 },
              maxRotation: 0,
              autoSkip: true,
              maxTicksLimit: 8,
            },
            border: {
              display: false,
            },
          },
          y: {
            display: true,
            grid: {
              display: showGrid,
              color: '#2a2a2a',
            },
            ticks: {
              color: '#737373',
              font: { size: 11 },
              callback: (value: number | string) => {
                const num = typeof value === 'string' ? parseFloat(value) : value;
                if (num >= 1000000) return (num / 1000000).toFixed(1) + 'M';
                if (num >= 1000) return (num / 1000).toFixed(1) + 'K';
                return num;
              },
            },
            border: {
              display: false,
            },
          },
        },
      },
    });

    return () => {
      chartRef.current?.destroy();
    };
  }, [data, label, color, height, showPoints, showGrid, tension, fill]);

  return (
    <canvas
      ref={canvasRef}
      className={cn('w-full h-full', className)}
      style={{ height }}
      role="img"
      aria-label={label || 'Line chart'}
    />
  );
}