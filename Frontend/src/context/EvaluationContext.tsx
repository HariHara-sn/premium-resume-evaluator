import React, { createContext, useContext, useState, ReactNode } from 'react';
import { EvaluationResult, EvaluationState } from '@/types/evaluation';

interface EvaluationContextType extends EvaluationState {
  setResult: (result: EvaluationResult) => void;
  setResumeFile: (file: File) => void;
  setResumeUrl: (url: string) => void;
  clearState: () => void;
}

const EvaluationContext = createContext<EvaluationContextType | undefined>(undefined);

export function EvaluationProvider({ children }: { children: ReactNode }) {
  const [result, setResult] = useState<EvaluationResult | null>(null);
  const [resumeFile, setResumeFile] = useState<File | null>(null);
  const [resumeUrl, setResumeUrl] = useState<string | null>(null);

  const clearState = () => {
    setResult(null);
    setResumeFile(null);
    setResumeUrl(null);
  };

  return (
    <EvaluationContext.Provider
      value={{
        result,
        resumeFile,
        resumeUrl,
        setResult,
        setResumeFile,
        setResumeUrl,
        clearState,
      }}
    >
      {children}
    </EvaluationContext.Provider>
  );
}

export function useEvaluation() {
  const context = useContext(EvaluationContext);
  if (context === undefined) {
    throw new Error('useEvaluation must be used within an EvaluationProvider');
  }
  return context;
}
