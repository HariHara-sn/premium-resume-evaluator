import React from 'react';
import { FileText } from 'lucide-react';
import { cn } from '@/lib/utils';

interface PDFViewerProps {
  url: string | null;
  fileName?: string;
  className?: string;
}

export function PDFViewer({ url, fileName, className }: PDFViewerProps) {
  if (!url) {
    return (
      <div
        className={cn(
          'flex flex-col items-center justify-center h-full min-h-[400px] rounded-lg border-2 border-dashed border-muted-foreground/25 bg-muted/30',
          className
        )}
      >
        <FileText className="h-12 w-12 text-muted-foreground/50 mb-3" aria-hidden="true" />
        <p className="text-muted-foreground">No resume uploaded</p>
      </div>
    );
  }

  return (
    <div className={cn('flex flex-col h-full', className)}>
      {fileName && (
        <div className="flex items-center gap-2 p-3 border-b border-border bg-muted/50 rounded-t-lg">
          <FileText className="h-4 w-4 text-primary" aria-hidden="true" />
          <span className="text-sm font-medium text-foreground truncate">{fileName}</span>
        </div>
      )}
      <div className="flex-1 min-h-0">
        <iframe
          src={`${url}#toolbar=0&navpanes=0`}
          className="w-full h-full rounded-b-lg border-0"
          title="Resume PDF Viewer"
          aria-label="Your uploaded resume"
        />
      </div>
    </div>
  );
}
