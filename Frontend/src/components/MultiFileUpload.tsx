import React, { useCallback, useState } from 'react';
import { Upload, FileText, X } from 'lucide-react';
import { cn } from '@/lib/utils';
import { Button } from '@/components/ui/button';

interface MultiFileUploadProps {
  onFilesSelect: (files: File[]) => void;
  selectedFiles: File[];
  onRemoveFile: (index: number) => void;
  onClear: () => void;
  disabled?: boolean;
  maxFiles?: number;
}

export function MultiFileUpload({
  onFilesSelect,
  selectedFiles,
  onRemoveFile,
  onClear,
  disabled,
  maxFiles = 10,
}: MultiFileUploadProps) {
  const [isDragging, setIsDragging] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const validateFile = (file: File): boolean => {
    if (file.type !== 'application/pdf') {
      setError('Please upload PDF files only');
      return false;
    }
    if (file.size > 10 * 1024 * 1024) {
      setError('Each file must be less than 10MB');
      return false;
    }
    return true;
  };

  const handleDrop = useCallback(
    (e: React.DragEvent<HTMLDivElement>) => {
      e.preventDefault();
      setIsDragging(false);
      if (disabled) return;

      const droppedFiles = Array.from(e.dataTransfer.files);
      const validFiles = droppedFiles.filter(validateFile);
      
      if (selectedFiles.length + validFiles.length > maxFiles) {
        setError(`Maximum ${maxFiles} files allowed`);
        return;
      }

      if (validFiles.length > 0) {
        setError(null);
        onFilesSelect([...selectedFiles, ...validFiles]);
      }
    },
    [onFilesSelect, selectedFiles, disabled, maxFiles]
  );

  const handleDragOver = useCallback((e: React.DragEvent<HTMLDivElement>) => {
    e.preventDefault();
    if (!disabled) setIsDragging(true);
  }, [disabled]);

  const handleDragLeave = useCallback((e: React.DragEvent<HTMLDivElement>) => {
    e.preventDefault();
    setIsDragging(false);
  }, []);

  const handleFileInput = useCallback(
    (e: React.ChangeEvent<HTMLInputElement>) => {
      const files = Array.from(e.target.files || []);
      const validFiles = files.filter(validateFile);
      
      if (selectedFiles.length + validFiles.length > maxFiles) {
        setError(`Maximum ${maxFiles} files allowed`);
        return;
      }

      if (validFiles.length > 0) {
        setError(null);
        onFilesSelect([...selectedFiles, ...validFiles]);
      }
      e.target.value = '';
    },
    [onFilesSelect, selectedFiles, maxFiles]
  );

  const formatFileSize = (bytes: number): string => {
    if (bytes < 1024) return bytes + ' B';
    if (bytes < 1024 * 1024) return (bytes / 1024).toFixed(1) + ' KB';
    return (bytes / (1024 * 1024)).toFixed(1) + ' MB';
  };

  return (
    <div className="space-y-4">
      <div
        onDrop={handleDrop}
        onDragOver={handleDragOver}
        onDragLeave={handleDragLeave}
        className={cn(
          'relative rounded-lg border-2 border-dashed p-6 transition-all duration-200 cursor-pointer',
          isDragging
            ? 'border-primary bg-primary/5 scale-[1.01]'
            : 'border-muted-foreground/25 hover:border-primary/50 hover:bg-muted/50',
          disabled && 'opacity-50 cursor-not-allowed',
          error && 'border-destructive/50'
        )}
        role="button"
        tabIndex={0}
        aria-label="Upload multiple PDF files"
        onKeyDown={(e) => {
          if (e.key === 'Enter' || e.key === ' ') {
            document.getElementById('multi-file-input')?.click();
          }
        }}
      >
        <input
          id="multi-file-input"
          type="file"
          accept=".pdf,application/pdf"
          multiple
          onChange={handleFileInput}
          className="absolute inset-0 w-full h-full opacity-0 cursor-pointer disabled:cursor-not-allowed"
          disabled={disabled}
        />
        <div className="flex flex-col items-center gap-2 text-center">
          <div className={cn(
            'flex h-12 w-12 items-center justify-center rounded-full transition-colors',
            isDragging ? 'bg-primary/20' : 'bg-muted'
          )}>
            <Upload className={cn('h-6 w-6', isDragging ? 'text-primary' : 'text-muted-foreground')} />
          </div>
          <div>
            <p className="font-medium text-foreground">
              {isDragging ? 'Drop files here' : 'Upload resumes'}
            </p>
            <p className="text-sm text-muted-foreground">
              Drag and drop or click to browse (PDF only)
            </p>
          </div>
        </div>
      </div>

      {error && (
        <p className="text-sm text-destructive" role="alert">{error}</p>
      )}

      {selectedFiles.length > 0 && (
        <div className="space-y-2">
          <div className="flex items-center justify-between">
            <span className="text-sm font-medium text-foreground">
              {selectedFiles.length} file(s) selected
            </span>
            <Button variant="ghost" size="sm" onClick={onClear} disabled={disabled}>
              Clear all
            </Button>
          </div>
          <div className="space-y-2 max-h-48 overflow-y-auto">
            {selectedFiles.map((file, index) => (
              <div
                key={`${file.name}-${index}`}
                className="flex items-center gap-3 p-3 rounded-lg border border-border bg-card"
              >
                <FileText className="h-5 w-5 text-primary flex-shrink-0" />
                <div className="flex-1 min-w-0">
                  <p className="text-sm font-medium text-foreground truncate">{file.name}</p>
                  <p className="text-xs text-muted-foreground">{formatFileSize(file.size)}</p>
                </div>
                <Button
                  variant="ghost"
                  size="icon"
                  onClick={() => onRemoveFile(index)}
                  disabled={disabled}
                  className="h-8 w-8 text-muted-foreground hover:text-destructive"
                >
                  <X className="h-4 w-4" />
                </Button>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
}
