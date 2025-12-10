export interface Improvement {
  area: string;
  suggestion: string;
}

export interface EvaluationResult {
  verdict: string;
  matchScore: number;
  missingSkills: string[];
  tip: string;
  improvements: Improvement[];
}

export interface EvaluationState {
  result: EvaluationResult | null;
  resumeFile: File | null;
  resumeUrl: string | null;
}
