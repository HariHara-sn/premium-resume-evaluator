import React from 'react';
import { Link } from 'react-router-dom';
import { FileSearch } from 'lucide-react';

export function Header() {
  return (
    <header className="sticky top-0 z-50 w-full border-b border-border bg-background/80 backdrop-blur-sm">
      <div className="container flex h-16 items-center">
        <Link
          to="/"
          className="flex items-center gap-2 font-display font-bold text-xl text-foreground hover:text-primary transition-colors"
          aria-label="Resume Evaluator Home"
        >
          <div className="flex h-9 w-9 items-center justify-center rounded-lg gradient-primary">
            <FileSearch className="h-5 w-5 text-primary-foreground" aria-hidden="true" />
          </div>
          <span>ResumeAI</span>
        </Link>
      </div>
    </header>
  );
}
