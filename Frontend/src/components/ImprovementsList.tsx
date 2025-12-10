import React from 'react';
import { Lightbulb, ChevronRight } from 'lucide-react';
import { cn } from '@/lib/utils';
import { Improvement } from '@/types/evaluation';

interface ImprovementsListProps {
  improvements: Improvement[];
  className?: string;
}

export function ImprovementsList({ improvements, className }: ImprovementsListProps) {
  if (improvements.length === 0) {
    return (
      <p className="text-muted-foreground text-sm">No improvements suggested!</p>
    );
  }

  // Group improvements by area
  const groupedImprovements = improvements.reduce((acc, item) => {
    if (!acc[item.area]) {
      acc[item.area] = [];
    }
    acc[item.area].push(item.suggestion);
    return acc;
  }, {} as Record<string, string[]>);

  return (
    <div className={cn('space-y-4', className)}>
      <div className="flex items-center gap-2 text-primary">
        <Lightbulb className="h-5 w-5" aria-hidden="true" />
        <h3 className="font-semibold">Suggested Improvements</h3>
      </div>
      <div className="space-y-4" role="list" aria-label="Suggested improvements">
        {Object.entries(groupedImprovements).map(([area, suggestions], areaIndex) => (
          <div
            key={area}
            className="rounded-lg border border-border bg-card p-4 shadow-soft animate-slide-up"
            style={{ animationDelay: `${areaIndex * 100}ms` }}
            role="listitem"
          >
            <h4 className="font-medium text-foreground mb-3 capitalize flex items-center gap-2">
              <span className="h-2 w-2 rounded-full bg-primary" aria-hidden="true" />
              {area}
            </h4>
            <ul className="space-y-2">
              {suggestions.map((suggestion, suggestionIndex) => (
                <li
                  key={suggestionIndex}
                  className="flex items-start gap-2 text-sm text-muted-foreground"
                >
                  <ChevronRight className="h-4 w-4 text-primary mt-0.5 shrink-0" aria-hidden="true" />
                  <span>{suggestion}</span>
                </li>
              ))}
            </ul>
          </div>
        ))}
      </div>
    </div>
  );
}
