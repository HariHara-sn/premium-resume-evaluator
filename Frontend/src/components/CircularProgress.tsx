import React, { useEffect, useState } from 'react';
import { cn } from '@/lib/utils';

interface CircularProgressProps {
  value: number;
  size?: number;
  strokeWidth?: number;
  className?: string;
}

export function CircularProgress({
  value,
  size = 180,
  strokeWidth = 12,
  className,
}: CircularProgressProps) {
  const [animatedValue, setAnimatedValue] = useState(0);
  const radius = (size - strokeWidth) / 2;
  const circumference = radius * 2 * Math.PI;
  const offset = circumference - (animatedValue / 100) * circumference;

  useEffect(() => {
    const timer = setTimeout(() => {
      setAnimatedValue(value);
    }, 100);
    return () => clearTimeout(timer);
  }, [value]);

  const getScoreColor = () => {
    if (value >= 80) return 'text-success';
    if (value >= 60) return 'text-primary';
    if (value >= 40) return 'text-warning';
    return 'text-destructive';
  };

  const getStrokeColor = () => {
    if (value >= 80) return 'stroke-success';
    if (value >= 60) return 'stroke-primary';
    if (value >= 40) return 'stroke-warning';
    return 'stroke-destructive';
  };

  return (
    <div className={cn('relative inline-flex items-center justify-center', className)}>
      <svg
        width={size}
        height={size}
        className="transform -rotate-90"
        aria-hidden="true"
      >
        {/* Background circle */}
        <circle
          cx={size / 2}
          cy={size / 2}
          r={radius}
          fill="none"
          stroke="currentColor"
          strokeWidth={strokeWidth}
          className="text-muted/50"
        />
        {/* Progress circle */}
        <circle
          cx={size / 2}
          cy={size / 2}
          r={radius}
          fill="none"
          strokeWidth={strokeWidth}
          strokeLinecap="round"
          className={cn('transition-all duration-1000 ease-out', getStrokeColor())}
          style={{
            strokeDasharray: circumference,
            strokeDashoffset: offset,
          }}
        />
      </svg>
      <div className="absolute inset-0 flex flex-col items-center justify-center">
        <span
          className={cn('text-5xl font-display font-bold tabular-nums', getScoreColor())}
          aria-label={`Match score: ${value}%`}
        >
          {Math.round(animatedValue)}
        </span>
        <span className="text-sm text-muted-foreground font-medium mt-1">Match Score</span>
      </div>
    </div>
  );
}
