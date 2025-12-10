import React from 'react';
import { AlertTriangle } from 'lucide-react';
import { cn } from '@/lib/utils';

interface SkillsListProps {
  skills: string[];
  className?: string;
}

export function SkillsList({ skills, className }: SkillsListProps) {
  if (skills.length === 0) {
    return (
      <p className="text-muted-foreground text-sm">No missing skills detected!</p>
    );
  }

  return (
    <div className={cn('space-y-3', className)}>
      <div className="flex items-center gap-2 text-warning">
        <AlertTriangle className="h-5 w-5" aria-hidden="true" />
        <h3 className="font-semibold">Missing Skills</h3>
      </div>
      <div className="flex flex-wrap gap-2" role="list" aria-label="Missing skills">
        {skills.map((skill, index) => (
          <span
            key={skill}
            className="inline-flex items-center rounded-full bg-warning/10 border border-warning/20 px-3 py-1 text-sm font-medium text-warning animate-fade-in"
            style={{ animationDelay: `${index * 50}ms` }}
            role="listitem"
          >
            {skill}
          </span>
        ))}
      </div>
    </div>
  );
}
