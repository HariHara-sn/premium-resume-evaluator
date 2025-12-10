import React from 'react';
import { Sparkles } from 'lucide-react';
import { cn } from '@/lib/utils';

interface TipCardProps {
  tip: string;
  className?: string;
}

export function TipCard({ tip, className }: TipCardProps) {
  return (
    <div
      className={cn(
        'relative overflow-hidden rounded-lg border border-accent/30 bg-gradient-to-br from-accent/5 to-primary/5 p-5 animate-slide-up',
        className
      )}
      role="complementary"
      aria-label="Pro tip"
    >
      <div className="absolute top-0 right-0 h-20 w-20 bg-accent/10 rounded-full blur-2xl" aria-hidden="true" />
      <div className="relative flex items-start gap-3">
        <div className="flex h-10 w-10 shrink-0 items-center justify-center rounded-lg gradient-primary">
          <Sparkles className="h-5 w-5 text-primary-foreground" aria-hidden="true" />
        </div>
        <div>
          <h3 className="font-semibold text-foreground mb-1">Pro Tip</h3>
          <p className="text-sm text-muted-foreground leading-relaxed">{tip}</p>
        </div>
      </div>
    </div>
  );
}
