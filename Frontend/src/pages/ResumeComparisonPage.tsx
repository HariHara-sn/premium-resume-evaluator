import React, { useState } from 'react';
import { Crown, Loader2, Trophy, FileText } from 'lucide-react';
import { Button } from '@/components/ui/button';
import { Textarea } from '@/components/ui/textarea';
import { Label } from '@/components/ui/label';
import { MultiFileUpload } from '@/components/MultiFileUpload';
import { toast } from '@/hooks/use-toast';
import { Progress } from '@/components/ui/progress';
import { fetchJson } from '@/lib/api';

interface ComparisonResult {
  scores: Record<string, number>;
  best_resume: string;
  reason: string;
}

const ResumeComparisonPage = () => {
  const [files, setFiles] = useState<File[]>([]);
  const [jobDescription, setJobDescription] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [result, setResult] = useState<ComparisonResult | null>(null);

  const handleRemoveFile = (index: number) => {
    setFiles(files.filter((_, i) => i !== index));
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();

    if (files.length < 2) {
      toast({ title: 'Upload more resumes', description: 'Please upload at least 2 resumes to compare.', variant: 'destructive' });
      return;
    }

    if (!jobDescription.trim()) {
      toast({ title: 'Job description required', description: 'Please enter the job description.', variant: 'destructive' });
      return;
    }

    setIsLoading(true);

    try {
      const formData = new FormData();
      files.forEach((file) => formData.append('files', file));
      // Backend compare-resumes ignores JD, but we collect it for UI; no need to send.

      const data = await fetchJson<ComparisonResult>('/compare-resumes', {
        method: 'POST',
        body: formData,
      });

      setResult(data);
      toast({ title: 'Comparison Complete!', description: 'Resume rankings are ready.' });
    } catch (error) {
      console.error('Comparison error:', error);
      toast({ title: 'Comparison failed', description: 'Please try again.', variant: 'destructive' });
    } finally {
      setIsLoading(false);
    }
  };

  const sortedScores = result
    ? Object.entries(result.scores).sort((a, b) => b[1] - a[1])
    : [];

  return (
    <div className="p-6 lg:p-10 gradient-surface min-h-full">
      <div className="max-w-5xl mx-auto">
        <div className="text-center mb-8 animate-fade-in">
          <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-warning/10 text-warning text-sm mb-4">
            <Crown className="h-4 w-4" />
            Elite Feature
          </div>
          <h1 className="text-3xl md:text-4xl font-display font-bold text-foreground mb-3">
            Multi-Resume{" "}
            <span className="bg-gradient-to-r from-primary to-accent bg-clip-text text-transparent">Comparison</span>
          </h1>
          <p className="text-muted-foreground max-w-lg mx-auto">
            Compare multiple resumes and find the best match for the job.
          </p>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
          {/* Input Section */}
          <div className="animate-slide-up">
            <div className="p-6 rounded-xl border border-border bg-card shadow-soft">
              <form onSubmit={handleSubmit} className="space-y-5">
                <div className="space-y-2">
                  <Label className="text-base font-medium">Resumes to Compare (PDF)</Label>
                  <MultiFileUpload
                    onFilesSelect={setFiles}
                    selectedFiles={files}
                    onRemoveFile={handleRemoveFile}
                    onClear={() => { setFiles([]); setResult(null); }}
                    disabled={isLoading}
                  />
                  <p className="text-xs text-muted-foreground">Upload 2 or more resumes</p>
                </div>

                <div className="space-y-2">
                  <Label className="text-base font-medium">Job Description</Label>
                  <Textarea
                    placeholder="Paste the job description here..."
                    value={jobDescription}
                    onChange={(e) => setJobDescription(e.target.value)}
                    disabled={isLoading}
                    className="min-h-[140px] bg-background"
                  />
                </div>

                <Button
                  type="submit"
                  variant="gradient"
                  size="lg"
                  className="w-full"
                  disabled={isLoading || files.length < 2 || !jobDescription.trim()}
                >
                  {isLoading ? (
                    <>
                      <Loader2 className="h-5 w-5 animate-spin" />
                      <span>Comparing...</span>
                    </>
                  ) : (
                    <>
                      <Crown className="h-5 w-5" />
                      <span>Compare Resumes</span>
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
                {/* Winner Card */}
                <div className="p-5 rounded-xl border-2 border-warning/30 bg-warning/5">
                  <div className="flex items-start gap-4">
                    <div className="h-12 w-12 rounded-full bg-warning/20 flex items-center justify-center flex-shrink-0">
                      <Trophy className="h-6 w-6 text-warning" />
                    </div>
                    <div>
                      <p className="text-sm text-muted-foreground mb-1">Best Resume</p>
                      <h3 className="font-bold text-foreground mb-2 break-all">{result.best_resume}</h3>
                      <p className="text-sm text-muted-foreground">{result.reason}</p>
                    </div>
                  </div>
                </div>

                {/* Rankings */}
                <div className="p-5 rounded-xl border border-border bg-card">
                  <h3 className="font-semibold text-foreground mb-4">Resume Rankings</h3>
                  <div className="space-y-4">
                    {sortedScores.map(([name, score], index) => (
                      <div key={name} className="space-y-2">
                        <div className="flex items-center gap-3">
                          <span className={`flex-shrink-0 h-6 w-6 rounded-full flex items-center justify-center text-xs font-bold ${
                            index === 0 
                              ? 'bg-warning/20 text-warning' 
                              : index === 1 
                                ? 'bg-muted text-muted-foreground' 
                                : 'bg-muted/50 text-muted-foreground'
                          }`}>
                            {index + 1}
                          </span>
                          <div className="flex-1 min-w-0">
                            <div className="flex items-center justify-between mb-1">
                              <span className="text-sm text-foreground truncate flex items-center gap-2">
                                <FileText className="h-4 w-4 text-primary flex-shrink-0" />
                                {name}
                              </span>
                              <span className={`text-sm font-bold ${
                                score >= 85 ? 'text-success' : score >= 70 ? 'text-warning' : 'text-muted-foreground'
                              }`}>
                                {score}%
                              </span>
                            </div>
                            <Progress value={score} className="h-2" />
                          </div>
                        </div>
                      </div>
                    ))}
                  </div>
                </div>
              </div>
            ) : (
              <div className="h-80 flex items-center justify-center rounded-xl border border-border bg-card/50">
                <div className="text-center text-muted-foreground">
                  <Crown className="h-12 w-12 mx-auto mb-3 opacity-50" />
                  <p>Upload multiple resumes to compare them</p>
                </div>
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
};

export default ResumeComparisonPage;
