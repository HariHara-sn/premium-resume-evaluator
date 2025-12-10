import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { Send, Loader2 } from 'lucide-react';
import { Button } from '@/components/ui/button';
import { Textarea } from '@/components/ui/textarea';
import { Label } from '@/components/ui/label';
import { FileUpload } from '@/components/FileUpload';
import { Header } from '@/components/Header';
import { useEvaluation } from '@/context/EvaluationContext';
import { toast } from '@/hooks/use-toast';

const Index = () => {
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
      // Create FormData for the API request
      const formData = new FormData();
      formData.append('resume', file);
      formData.append('jobDescription', jobDescription);

      // TODO: Replace with actual API endpoint
      // const response = await fetch('/api/evaluate', {
      //   method: 'POST',
      //   body: formData,
      // });
      // const data = await response.json();

      // Simulated API response for demo
      await new Promise((resolve) => setTimeout(resolve, 2000));
      
      const mockResponse = {
        verdict: 'Shortlisted',
        matchScore: 85.0,
        missingSkills: ['PyTorch', 'FastAPI', 'AWS', 'GCP', 'Azure'],
        tip: 'Quantify the impact of your AI projects with metrics to demonstrate your accomplishments.',
        improvements: [
          {
            area: 'Skills',
            suggestion: 'Add experience with cloud platforms (AWS, GCP, or Azure) to strengthen your profile.',
          },
          {
            area: 'Skills',
            suggestion: 'Include PyTorch or TensorFlow certifications if available.',
          },
          {
            area: 'Experience',
            suggestion: 'Highlight specific metrics and KPIs achieved in previous roles.',
          },
          {
            area: 'Experience',
            suggestion: 'Add more details about team collaboration and leadership experience.',
          },
          {
            area: 'Format',
            suggestion: 'Consider adding a brief professional summary at the top of your resume.',
          },
        ],
      };

      // Store results in context
      setResult(mockResponse);
      setResumeFile(file);
      setResumeUrl(URL.createObjectURL(file));

      // Navigate to score page
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
    <div className="min-h-screen gradient-surface">
      <Header />
      
      <main className="container py-12">
        <div className="mx-auto max-w-2xl">
          {/* Hero Section */}
          <div className="text-center mb-10 animate-fade-in">
            <h1 className="text-4xl md:text-5xl font-display font-bold text-foreground mb-4">
              AI Resume{" "}
              <span className="bg-gradient-to-r from-primary to-accent bg-clip-text text-transparent">Evaluator</span>
            </h1>
            <p className="text-lg text-muted-foreground max-w-lg mx-auto">
              Upload your resume and job description to get instant AI-powered feedback and improve your chances of landing the job.
            </p>
          </div>

          {/* Form */}
          <form onSubmit={handleSubmit} className="space-y-8">
            {/* File Upload Section */}
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

            {/* Job Description Section */}
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
                className="min-h-[200px] resize-y bg-card border-input focus:border-primary focus:ring-primary/20"
                aria-describedby="job-description-hint"
              />
              <p id="job-description-hint" className="text-sm text-muted-foreground">
                Include the full job posting for the most accurate evaluation.
              </p>
            </div>

            {/* Submit Button */}
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
                    <Loader2 className="h-5 w-5 animate-spin" aria-hidden="true" />
                    <span>Analyzing...</span>
                  </>
                ) : (
                  <>
                    <Send className="h-5 w-5" aria-hidden="true" />
                    <span>Evaluate Resume</span>
                  </>
                )}
              </Button>
            </div>
          </form>

          {/* Features */}
          <div className="mt-16 grid grid-cols-1 md:grid-cols-3 gap-6 animate-fade-in" style={{ animationDelay: '400ms' }}>
            {[
              { title: 'AI-Powered', description: 'Advanced analysis using machine learning' },
              { title: 'Instant Results', description: 'Get feedback in seconds' },
              { title: 'Actionable Tips', description: 'Clear improvements to boost your resume' },
            ].map((feature, index) => (
              <div
                key={feature.title}
                className="text-center p-4 rounded-lg border border-border bg-card/50 shadow-soft"
              >
                <h3 className="font-semibold text-foreground mb-1">{feature.title}</h3>
                <p className="text-sm text-muted-foreground">{feature.description}</p>
              </div>
            ))}
          </div>
        </div>
      </main>
    </div>
  );
};

export default Index;
