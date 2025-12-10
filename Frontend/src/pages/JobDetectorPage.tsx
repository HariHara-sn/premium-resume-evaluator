import React, { useState } from 'react';
import { Search, Loader2, Briefcase, CheckCircle } from 'lucide-react';
import { Button } from '@/components/ui/button';
import { Label } from '@/components/ui/label';
import { FileUpload } from '@/components/FileUpload';
import { toast } from '@/hooks/use-toast';
import { Progress } from '@/components/ui/progress';
import { fetchJson } from '@/lib/api';

interface JobRole {
  role: string;
  confidence: string;
}

interface JobDetectionResult {
  primary_role: string;
  roles: JobRole[];
  skills_detected: string[];
}

const JobDetectorPage = () => {
  const [file, setFile] = useState<File | null>(null);
  const [isLoading, setIsLoading] = useState(false);
  const [result, setResult] = useState<JobDetectionResult | null>(null);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();

    if (!file) {
      toast({ title: 'No resume uploaded', description: 'Please upload your resume.', variant: 'destructive' });
      return;
    }

    setIsLoading(true);

    try {
      const formData = new FormData();
      formData.append('file', file);

      const data = await fetchJson<JobDetectionResult>('/job-detector', {
        method: 'POST',
        body: formData,
      });

      setResult(data);
      toast({ title: 'Analysis Complete!', description: 'Job roles detected from your resume.' });
    } catch (error) {
      console.error('Detection error:', error);
      toast({ title: 'Detection failed', description: 'Please try again.', variant: 'destructive' });
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="p-6 lg:p-10 gradient-surface min-h-full">
      <div className="max-w-4xl mx-auto">
        <div className="text-center mb-8 animate-fade-in">
          <h1 className="text-3xl md:text-4xl font-display font-bold text-foreground mb-3">
            Job{" "}
            <span className="bg-gradient-to-r from-primary to-accent bg-clip-text text-transparent">Detector</span>
          </h1>
          <p className="text-muted-foreground max-w-lg mx-auto">
            Upload your resume to discover the best job roles matching your skills.
          </p>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
          {/* Upload Section */}
          <div className="animate-slide-up">
            <div className="p-6 rounded-xl border border-border bg-card shadow-soft">
              <form onSubmit={handleSubmit} className="space-y-5">
                <div className="space-y-2">
                  <Label className="text-base font-medium">Your Resume (PDF)</Label>
                  <FileUpload
                    onFileSelect={setFile}
                    selectedFile={file}
                    onClear={() => { setFile(null); setResult(null); }}
                    disabled={isLoading}
                  />
                </div>

                <Button
                  type="submit"
                  variant="gradient"
                  size="lg"
                  className="w-full"
                  disabled={isLoading || !file}
                >
                  {isLoading ? (
                    <>
                      <Loader2 className="h-5 w-5 animate-spin" />
                      <span>Analyzing...</span>
                    </>
                  ) : (
                    <>
                      <Search className="h-5 w-5" />
                      <span>Detect Job Roles</span>
                    </>
                  )}
                </Button>
              </form>
            </div>
          </div>

          {/* Results Section */}
          <div className="animate-slide-up" style={{ animationDelay: '100ms' }}>
            {result ? (
              <div className="space-y-6">
                {/* Primary Role */}
                <div className="p-5 rounded-xl border border-primary/30 bg-primary/5">
                  <div className="flex items-center gap-3">
                    <div className="h-12 w-12 rounded-full gradient-primary flex items-center justify-center">
                      <Briefcase className="h-6 w-6 text-primary-foreground" />
                    </div>
                    <div>
                      <p className="text-sm text-muted-foreground">Best Match</p>
                      <h2 className="text-xl font-bold text-foreground">{result.primary_role}</h2>
                    </div>
                  </div>
                </div>

                {/* All Roles */}
                <div className="p-5 rounded-xl border border-border bg-card">
                  <h3 className="font-semibold text-foreground mb-4">Matching Roles</h3>
                  <div className="space-y-3">
                    {result.roles.map((role, index) => {
                      const confidence = parseInt(role.confidence);
                      return (
                        <div key={index} className="space-y-1">
                          <div className="flex items-center justify-between text-sm">
                            <span className="text-foreground">{role.role}</span>
                            <span className="text-primary font-medium">{role.confidence}</span>
                          </div>
                          <Progress value={confidence} className="h-2" />
                        </div>
                      );
                    })}
                  </div>
                </div>

                {/* Skills */}
                <div className="p-5 rounded-xl border border-border bg-card">
                  <h3 className="font-semibold text-foreground mb-3">Skills Detected</h3>
                  <div className="flex flex-wrap gap-2">
                    {result.skills_detected.map((skill, index) => (
                      <span
                        key={index}
                        className="inline-flex items-center gap-1 px-2.5 py-1 rounded-full bg-accent/10 text-accent text-sm"
                      >
                        <CheckCircle className="h-3 w-3" />
                        {skill}
                      </span>
                    ))}
                  </div>
                </div>
              </div>
            ) : (
              <div className="h-full flex items-center justify-center p-8 rounded-xl border border-border bg-card/50">
                <div className="text-center text-muted-foreground">
                  <Search className="h-12 w-12 mx-auto mb-3 opacity-50" />
                  <p>Upload a resume to detect suitable job roles</p>
                </div>
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
};

export default JobDetectorPage;
