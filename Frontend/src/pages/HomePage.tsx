import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { Send, Loader2 } from 'lucide-react';
import { Button } from '@/components/ui/button';
import { Textarea } from '@/components/ui/textarea';
import { Label } from '@/components/ui/label';
import { FileUpload } from '@/components/FileUpload';
import { useEvaluation } from '@/context/EvaluationContext';
import { toast } from '@/hooks/use-toast';
import { fetchJson } from '@/lib/api';

const HomePage = () => {
  const navigate = useNavigate();
  const { setResult, setResumeFile, setResumeUrl } = useEvaluation();
  
  const [file, setFile] = useState<File | null>(null);
  const [jobDescription, setJobDescription] = useState('');
  const [isLoading, setIsLoading] = useState(false);

  const handleFileSelect = (selectedFile: File) => {
    setFile(selectedFile);
  };

  const handleClearFile = () => {
    setFile(null);
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();

    if (!file) {
      toast({
        title: 'No resume uploaded',
        description: 'Please upload your resume in PDF format.',
        variant: 'destructive',
      });
      return;
    }

    if (!jobDescription.trim()) {
      toast({
        title: 'Job description required',
        description: 'Please enter the job description.',
        variant: 'destructive',
      });
      return;
    }

    setIsLoading(true);

    try {
      const formData = new FormData();
      formData.append('resume_file', file);
      formData.append('jd_text', jobDescription);

      const data = await fetchJson<{
        verdict: string;
        match_score: number;
        missing_skills: string[];
        one_tip: string;
        improvements: { area: string; suggestion: string }[];
      }>('/analyze', {
        method: 'POST',
        body: formData,
      });

      setResult({
        verdict: data.verdict,
        matchScore: data.match_score,
        missingSkills: data.missing_skills,
        tip: data.one_tip,
        improvements: data.improvements,
      });
      setResumeFile(file);
      setResumeUrl(URL.createObjectURL(file));
      navigate('/scorepage');
    } catch (error) {
      console.error('Evaluation error:', error);
      toast({
        title: 'Evaluation failed',
        description: 'Something went wrong. Please try again.',
        variant: 'destructive',
      });
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="p-6 lg:p-10 gradient-surface min-h-full">
      <div className="mx-auto max-w-2xl">
        <div className="text-center mb-10 animate-fade-in">
          <h1 className="text-3xl md:text-4xl font-display font-bold text-foreground mb-4">
            AI Resume{" "}
            <span className="bg-gradient-to-r from-primary to-accent bg-clip-text text-transparent">
              Evaluator
            </span>
          </h1>
          <p className="text-muted-foreground max-w-lg mx-auto">
            Upload your resume and job description to get instant AI-powered feedback.
          </p>
        </div>

        <form onSubmit={handleSubmit} className="space-y-6">
          <div className="space-y-3 animate-slide-up" style={{ animationDelay: '100ms' }}>
            <Label htmlFor="resume-upload" className="text-base font-medium">
              Resume (PDF)
            </Label>
            <FileUpload
              onFileSelect={handleFileSelect}
              selectedFile={file}
              onClear={handleClearFile}
              disabled={isLoading}
            />
          </div>

          <div className="space-y-3 animate-slide-up" style={{ animationDelay: '200ms' }}>
            <Label htmlFor="job-description" className="text-base font-medium">
              Job Description
            </Label>
            <Textarea
              id="job-description"
              placeholder="Paste the job description here..."
              value={jobDescription}
              onChange={(e) => setJobDescription(e.target.value)}
              disabled={isLoading}
              className="min-h-[180px] resize-y bg-card border-input"
            />
          </div>

          <div className="animate-slide-up" style={{ animationDelay: '300ms' }}>
            <Button
              type="submit"
              variant="gradient"
              size="lg"
              className="w-full"
              disabled={isLoading || !file || !jobDescription.trim()}
            >
              {isLoading ? (
                <>
                  <Loader2 className="h-5 w-5 animate-spin" />
                  <span>Analyzing...</span>
                </>
              ) : (
                <>
                  <Send className="h-5 w-5" />
                  <span>Evaluate Resume</span>
                </>
              )}
            </Button>
          </div>
        </form>

        <div className="mt-12 grid grid-cols-1 md:grid-cols-3 gap-4 animate-fade-in" style={{ animationDelay: '400ms' }}>
          {[
            { title: 'AI-Powered', description: 'Advanced ML analysis' },
            { title: 'Instant Results', description: 'Get feedback in seconds' },
            { title: 'Actionable Tips', description: 'Clear improvements' },
          ].map((feature) => (
            <div key={feature.title} className="text-center p-4 rounded-lg border border-border bg-card/50">
              <h3 className="font-semibold text-foreground mb-1">{feature.title}</h3>
              <p className="text-sm text-muted-foreground">{feature.description}</p>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
};

export default HomePage;
