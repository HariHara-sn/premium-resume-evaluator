import React, { useState } from 'react';
import { Sparkles, Loader2, Code, FolderKanban, GraduationCap } from 'lucide-react';
import { Button } from '@/components/ui/button';
import { Textarea } from '@/components/ui/textarea';
import { Label } from '@/components/ui/label';
import { MultiFileUpload } from '@/components/MultiFileUpload';
import { toast } from '@/hooks/use-toast';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs';
import { fetchJson } from '@/lib/api';

interface InterviewQuestionsResult {
  technical_questions: string[];
  project_questions: string[];
  cs_fundamentals_questions: string[];
}

const InterviewQuestionsPage = () => {
  const [files, setFiles] = useState<File[]>([]);
  const [jobDescription, setJobDescription] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [result, setResult] = useState<InterviewQuestionsResult | null>(null);

  const handleRemoveFile = (index: number) => {
    setFiles(files.filter((_, i) => i !== index));
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();

    if (files.length === 0) {
      toast({ title: 'No resumes uploaded', description: 'Please upload at least one resume.', variant: 'destructive' });
      return;
    }

    if (!jobDescription.trim()) {
      toast({ title: 'Job description required', description: 'Please enter the job description.', variant: 'destructive' });
      return;
    }

    setIsLoading(true);

    try {
      const formData = new FormData();
      // Backend supports one resume_file; send the first uploaded file
      formData.append('resume_file', files[0]);
      formData.append('jd_text', jobDescription);

      const data = await fetchJson<InterviewQuestionsResult & { cs_fundamentals_questions: string[] }>(
        '/interview-questions/generate',
        {
          method: 'POST',
          body: formData,
        }
      );

      setResult({
        technical_questions: data.technical_questions,
        project_questions: data.project_questions,
        cs_fundamentals_questions: data.cs_fundamentals_questions,
      });
      toast({ title: 'Questions Generated!', description: 'Interview questions are ready for review.' });
    } catch (error) {
      console.error('Generation error:', error);
      toast({ title: 'Generation failed', description: 'Please try again.', variant: 'destructive' });
    } finally {
      setIsLoading(false);
    }
  };

  const QuestionCard = ({ question, index }: { question: string; index: number }) => (
    <div className="p-4 rounded-lg border border-border bg-background hover:border-primary/30 transition-colors">
      <div className="flex gap-3">
        <span className="flex-shrink-0 h-6 w-6 rounded-full bg-primary/10 text-primary text-sm font-medium flex items-center justify-center">
          {index + 1}
        </span>
        <p className="text-foreground text-sm">{question}</p>
      </div>
    </div>
  );

  return (
    <div className="p-6 lg:p-10 gradient-surface min-h-full">
      <div className="max-w-6xl mx-auto">
        <div className="text-center mb-8 animate-fade-in">
          <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-accent/10 text-accent text-sm mb-4">
            <Sparkles className="h-4 w-4" />
            Advanced Feature
          </div>
          <h1 className="text-3xl md:text-4xl font-display font-bold text-foreground mb-3">
            Interview Question{" "}
            <span className="bg-gradient-to-r from-primary to-accent bg-clip-text text-transparent">Generator</span>
          </h1>
          <p className="text-muted-foreground max-w-lg mx-auto">
            Generate tailored interview questions based on resumes and job description.
          </p>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-5 gap-8">
          {/* Input Section */}
          <div className="lg:col-span-2 animate-slide-up">
            <div className="p-6 rounded-xl border border-border bg-card shadow-soft sticky top-6">
              <form onSubmit={handleSubmit} className="space-y-5">
                <div className="space-y-2">
                  <Label className="text-base font-medium">Resumes (PDF)</Label>
                  <MultiFileUpload
                    onFilesSelect={setFiles}
                    selectedFiles={files}
                    onRemoveFile={handleRemoveFile}
                    onClear={() => setFiles([])}
                    disabled={isLoading}
                  />
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
                  disabled={isLoading || files.length === 0 || !jobDescription.trim()}
                >
                  {isLoading ? (
                    <>
                      <Loader2 className="h-5 w-5 animate-spin" />
                      <span>Generating...</span>
                    </>
                  ) : (
                    <>
                      <Sparkles className="h-5 w-5" />
                      <span>Generate Questions</span>
                    </>
                  )}
                </Button>
              </form>
            </div>
          </div>

          {/* Results Section */}
          <div className="lg:col-span-3 animate-slide-up" style={{ animationDelay: '100ms' }}>
            {result ? (
              <Tabs defaultValue="technical" className="w-full">
                <TabsList className="w-full grid grid-cols-3 mb-4">
                  <TabsTrigger value="technical" className="gap-2">
                    <Code className="h-4 w-4" />
                    Technical
                  </TabsTrigger>
                  <TabsTrigger value="project" className="gap-2">
                    <FolderKanban className="h-4 w-4" />
                    Project
                  </TabsTrigger>
                  <TabsTrigger value="fundamentals" className="gap-2">
                    <GraduationCap className="h-4 w-4" />
                    CS Basics
                  </TabsTrigger>
                </TabsList>

                <TabsContent value="technical" className="space-y-3">
                  {result.technical_questions.map((q, i) => (
                    <QuestionCard key={i} question={q} index={i} />
                  ))}
                </TabsContent>

                <TabsContent value="project" className="space-y-3">
                  {result.project_questions.map((q, i) => (
                    <QuestionCard key={i} question={q} index={i} />
                  ))}
                </TabsContent>

                <TabsContent value="fundamentals" className="space-y-3">
                  {result.cs_fundamentals_questions.map((q, i) => (
                    <QuestionCard key={i} question={q} index={i} />
                  ))}
                </TabsContent>
              </Tabs>
            ) : (
              <div className="h-80 flex items-center justify-center rounded-xl border border-border bg-card/50">
                <div className="text-center text-muted-foreground">
                  <Sparkles className="h-12 w-12 mx-auto mb-3 opacity-50" />
                  <p>Upload resumes and job description to generate questions</p>
                </div>
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
};

export default InterviewQuestionsPage;
