import { Toaster } from "@/components/ui/toaster";
import { Toaster as Sonner } from "@/components/ui/sonner";
import { TooltipProvider } from "@/components/ui/tooltip";
import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import { BrowserRouter, Routes, Route } from "react-router-dom";
import { EvaluationProvider } from "@/context/EvaluationContext";
import { Layout } from "@/components/Layout";
import HomePage from "./pages/HomePage";
import EnhanceCVPage from "./pages/EnhanceCVPage";
import JobDetectorPage from "./pages/JobDetectorPage";
import ChatbotPage from "./pages/ChatbotPage";
import InterviewQuestionsPage from "./pages/InterviewQuestionsPage";
import ResumeComparisonPage from "./pages/ResumeComparisonPage";
import ScorePage from "./pages/ScorePage";
import NotFound from "./pages/NotFound";

const queryClient = new QueryClient();

const App = () => (
  <QueryClientProvider client={queryClient}>
    <TooltipProvider>
      <EvaluationProvider>
        <Toaster />
        <Sonner />
        <BrowserRouter>
          <Layout>
            <Routes>
              <Route path="/" element={<HomePage />} />
              <Route path="/enhance-cv" element={<EnhanceCVPage />} />
              <Route path="/job-detector" element={<JobDetectorPage />} />
              <Route path="/chatbot" element={<ChatbotPage />} />
              <Route path="/interview-questions" element={<InterviewQuestionsPage />} />
              <Route path="/resume-comparison" element={<ResumeComparisonPage />} />
              <Route path="/scorepage" element={<ScorePage />} />
              <Route path="*" element={<NotFound />} />
            </Routes>
          </Layout>
        </BrowserRouter>
      </EvaluationProvider>
    </TooltipProvider>
  </QueryClientProvider>
);

export default App;
