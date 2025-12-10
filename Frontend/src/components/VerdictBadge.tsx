import React from 'react';
import { CheckCircle, XCircle, AlertCircle } from 'lucide-react';
import { cn } from '@/lib/utils';

interface VerdictBadgeProps {
  verdict: string;
  className?: string;
}

export function VerdictBadge({ verdict, className }: VerdictBadgeProps) {
  const normalizedVerdict = verdict.toLowerCase();

  const getVerdictStyles = () => {
    if (normalizedVerdict.includes('shortlist') || normalizedVerdict.includes('accept')) {
      return {
        bg: 'bg-success/10',
        border: 'border-success/30',
        text: 'text-success',
        icon: CheckCircle,
      };
    }
    if (normalizedVerdict.includes('reject')) {
      return {
        bg: 'bg-destructive/10',
        border: 'border-destructive/30',
        text: 'text-destructive',
        icon: XCircle,
      };
    }
    return {
      bg: 'bg-warning/10',
      border: 'border-warning/30',
      text: 'text-warning',
      icon: AlertCircle,
    };
  };

  const styles = getVerdictStyles();
  const Icon = styles.icon;

  return (
    <div
      className={cn(
        'inline-flex items-center gap-2 rounded-full px-4 py-2 border font-medium animate-scale-in',
        styles.bg,
        styles.border,
        styles.text,
        className
      )}
      role="status"
      aria-label={`Verdict: ${verdict}`}
    >
      <Icon className="h-5 w-5" aria-hidden="true" />
      <span className="text-base">{verdict}</span>
    </div>
  );
}
