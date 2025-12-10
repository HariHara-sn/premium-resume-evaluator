import React, { useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { ArrowLeft, RefreshCw } from 'lucide-react';
import { Button } from '@/components/ui/button';
import { Header } from '@/components/Header';
import { CircularProgress } from '@/components/CircularProgress';
import { VerdictBadge } from '@/components/VerdictBadge';
import { SkillsList } from '@/components/SkillsList';
import { ImprovementsList } from '@/components/ImprovementsList';
import { TipCard } from '@/components/TipCard';
import { PDFViewer } from '@/components/PDFViewer';
import { useEvaluation } from '@/context/EvaluationContext';

const ScorePage = () => {
  const navigate = useNavigate();
  const { result, resumeFile, resumeUrl, clearState } = useEvaluation();

  useEffect(() => {
    // Redirect to home if no result is available
    if (!result) {
      navigate('/');
    }
  }, [result, navigate]);

  const handleStartOver = () => {
    clearState();
    navigate('/');
  };

  if (!result) {
    return null;
  }

  return (
    <div className="min-h-screen bg-background">
      <Header />
      
      <main className="container py-8">
        {/* Back Button */}
        <div className="mb-6 animate-fade-in">
          <Button
            variant="ghost"
            onClick={handleStartOver}
            className="gap-2"
          >
            <ArrowLeft className="h-4 w-4" aria-hidden="true" />
            Start Over
          </Button>
        </div>

        {/* Split Layout */}
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
          {/* Left Side - Results */}
          <div className="space-y-8 order-2 lg:order-1">
            {/* Score and Verdict Section */}
            <section
              className="rounded-xl border border-border bg-card p-8 shadow-soft animate-scale-in"
              aria-labelledby="score-section-title"
            >
              <h2 id="score-section-title" className="sr-only">
                Evaluation Score
              </h2>
              <div className="flex flex-col items-center gap-6">
                <CircularProgress value={result.matchScore} />
                <VerdictBadge verdict={result.verdict} />
              </div>
            </section>

            {/* Pro Tip */}
            <section aria-labelledby="tip-section-title">
              <h2 id="tip-section-title" className="sr-only">
                Pro Tip
              </h2>
              <TipCard tip={result.tip} />
            </section>

            {/* Missing Skills */}
            <section
              className="rounded-xl border border-border bg-card p-6 shadow-soft animate-slide-up"
              aria-labelledby="skills-section-title"
              style={{ animationDelay: '200ms' }}
            >
              <h2 id="skills-section-title" className="sr-only">
                Missing Skills
              </h2>
              <SkillsList skills={result.missingSkills} />
            </section>

            {/* Improvements */}
            <section
              className="animate-slide-up"
              aria-labelledby="improvements-section-title"
              style={{ animationDelay: '300ms' }}
            >
              <h2 id="improvements-section-title" className="sr-only">
                Suggested Improvements
              </h2>
              <ImprovementsList improvements={result.improvements} />
            </section>

            {/* Action Buttons */}
            <div className="flex flex-col sm:flex-row gap-4 animate-fade-in" style={{ animationDelay: '400ms' }}>
              <Button
                variant="gradient"
                size="lg"
                onClick={handleStartOver}
                className="flex-1"
              >
                <RefreshCw className="h-5 w-5" aria-hidden="true" />
                Evaluate Another Resume
              </Button>
            </div>
          </div>

          {/* Right Side - PDF Viewer */}
          <div className="order-1 lg:order-2 lg:sticky lg:top-24 lg:self-start">
            <section
              className="rounded-xl border border-border bg-card shadow-soft overflow-hidden animate-scale-in h-[500px] lg:h-[calc(100vh-10rem)]"
              aria-labelledby="resume-section-title"
            >
              <h2 id="resume-section-title" className="sr-only">
                Your Resume
              </h2>
              <PDFViewer
                url={resumeUrl}
                fileName={resumeFile?.name}
                className="h-full"
              />
            </section>
          </div>
        </div>
      </main>
    </div>
  );
};

export default ScorePage;
