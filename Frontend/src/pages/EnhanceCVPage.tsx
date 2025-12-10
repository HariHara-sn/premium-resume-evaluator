import React, { useState } from 'react';
import { Wand2, Loader2, Download, FileText } from 'lucide-react';
import { Button } from '@/components/ui/button';
import { Textarea } from '@/components/ui/textarea';
import { Label } from '@/components/ui/label';
import { FileUpload } from '@/components/FileUpload';
import { toast } from '@/hooks/use-toast';
import { fetchBlob } from '@/lib/api';

const EnhanceCVPage = () => {
  const [file, setFile] = useState<File | null>(null);
  const [jobDescription, setJobDescription] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [enhancedResumeUrl, setEnhancedResumeUrl] = useState<string | null>(null);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();

    if (!file) {
      toast({ title: 'No resume uploaded', description: 'Please upload your resume.', variant: 'destructive' });
      return;
    }

    if (!jobDescription.trim()) {
      toast({ title: 'Job description required', description: 'Please enter the job description.', variant: 'destructive' });
      return;
    }

    setIsLoading(true);

    try {
      const formData = new FormData();
      formData.append('file', file);
      formData.append('jd_text', jobDescription);

      const blob = await fetchBlob('/rewrite-resume', {
        method: 'POST',
        body: formData,
      });

      const url = URL.createObjectURL(blob);
      setEnhancedResumeUrl(url);

      toast({ title: 'Resume Enhanced!', description: 'Your ATS-friendly resume is ready.' });
    } catch (error) {
      console.error('Enhancement error:', error);
      toast({ title: 'Enhancement failed', description: 'Please try again.', variant: 'destructive' });
    } finally {
      setIsLoading(false);
    }
  };

  const handleDownload = () => {
    if (enhancedResumeUrl) {
      const a = document.createElement('a');
      a.href = enhancedResumeUrl;
      a.download = 'enhanced-resume.pdf';
      a.click();
    }
  };

  return (
    <div className="p-6 lg:p-10 gradient-surface min-h-full">
      <div className="max-w-6xl mx-auto">
        <div className="text-center mb-8 animate-fade-in">
          <h1 className="text-3xl md:text-4xl font-display font-bold text-foreground mb-3">
            Enhance Your{" "}
            <span className="bg-gradient-to-r from-primary to-accent bg-clip-text text-transparent">CV</span>
          </h1>
          <p className="text-muted-foreground max-w-lg mx-auto">
            AI-powered resume rewriting to make your CV ATS-friendly and optimized for the job.
          </p>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
          {/* Input Section */}
          <div className="space-y-6 animate-slide-up">
            <div className="p-6 rounded-xl border border-border bg-card shadow-soft">
              <form onSubmit={handleSubmit} className="space-y-5">
                <div className="space-y-2">
                  <Label className="text-base font-medium">Your Resume (PDF)</Label>
                  <FileUpload
                    onFileSelect={setFile}
                    selectedFile={file}
                    onClear={() => setFile(null)}
                    disabled={isLoading}
                  />
                </div>

                <div className="space-y-2">
                  <Label className="text-base font-medium">Target Job Description</Label>
                  <Textarea
                    placeholder="Paste the job description here..."
                    value={jobDescription}
                    onChange={(e) => setJobDescription(e.target.value)}
                    disabled={isLoading}
                    className="min-h-[160px] bg-background"
                  />
                </div>

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
                      <span>Enhancing...</span>
                    </>
                  ) : (
                    <>
                      <Wand2 className="h-5 w-5" />
                      <span>AI Rewrite Resume</span>
                    </>
                  )}
                </Button>
              </form>
            </div>
          </div>

          {/* Preview Section */}
          <div className="animate-slide-up" style={{ animationDelay: '100ms' }}>
            <div className="p-6 rounded-xl border border-border bg-card shadow-soft h-full min-h-[500px] flex flex-col">
              <div className="flex items-center justify-between mb-4">
                <h2 className="font-semibold text-foreground flex items-center gap-2">
                  <FileText className="h-5 w-5 text-primary" />
                  Enhanced Resume Preview
                </h2>
                {enhancedResumeUrl && (
                  <Button variant="outline" size="sm" onClick={handleDownload}>
                    <Download className="h-4 w-4 mr-2" />
                    Download
                  </Button>
                )}
              </div>
              
              <div className="flex-1 rounded-lg border border-border bg-muted/30 overflow-hidden">
                {enhancedResumeUrl ? (
                  <iframe
                    src={enhancedResumeUrl}
                    className="w-full h-full min-h-[450px]"
                    title="Enhanced Resume Preview"
                  />
                ) : (
                  <div className="h-full flex items-center justify-center text-muted-foreground">
                    <div className="text-center">
                      <FileText className="h-12 w-12 mx-auto mb-3 opacity-50" />
                      <p>Enhanced resume will appear here</p>
                    </div>
                  </div>
                )}
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default EnhanceCVPage;
