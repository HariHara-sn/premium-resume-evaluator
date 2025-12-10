import React, { useState, useRef, useEffect } from 'react';
import { MessageSquare, Send, Loader2, Bot, User, FileText } from 'lucide-react';
import { Button } from '@/components/ui/button';
import { Textarea } from '@/components/ui/textarea';
import { Label } from '@/components/ui/label';
import { FileUpload } from '@/components/FileUpload';
import { Input } from '@/components/ui/input';
import { toast } from '@/hooks/use-toast';
import { ScrollArea } from '@/components/ui/scroll-area';
import { fetchJson } from '@/lib/api';

interface Message {
  role: 'user' | 'assistant';
  content: string;
}

const ChatbotPage = () => {
  const [file, setFile] = useState<File | null>(null);
  const [jobDescription, setJobDescription] = useState('');
  const [isChatEnabled, setIsChatEnabled] = useState(false);
  const [messages, setMessages] = useState<Message[]>([]);
  const [input, setInput] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const scrollRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    if (scrollRef.current) {
      scrollRef.current.scrollTop = scrollRef.current.scrollHeight;
    }
  }, [messages]);

  const handleStartChat = () => {
    if (!file) {
      toast({ title: 'No resume uploaded', description: 'Please upload your resume.', variant: 'destructive' });
      return;
    }
    if (!jobDescription.trim()) {
      toast({ title: 'Job description required', description: 'Please enter the job description.', variant: 'destructive' });
      return;
    }

    setIsChatEnabled(true);
    setMessages([
      {
        role: 'assistant',
        content: `Hello! I've analyzed your resume and the job description. I'm ready to help you prepare for your interview. Feel free to ask me any questions about:\n\n• Your resume strengths and weaknesses\n• Am I suitable for this job?\n• Potential interview questions\n• Tips for the specific role\n\nWhat would you like to know?`,
      },
    ]);
  };

  const handleSendMessage = async () => {
    if (!input.trim() || isLoading) return;

    const userMessage: Message = { role: 'user', content: input };
    setMessages((prev) => [...prev, userMessage]);
    setInput('');
    setIsLoading(true);

    try {
      const formData = new FormData();
      formData.append('resume_file', file as File);
      formData.append('jd_text', jobDescription);
      formData.append('question', userMessage.content);

      const data = await fetchJson<{ answer: string }>('/chatbot', {
        method: 'POST',
        body: formData,
      });

      const assistantMessage: Message = {
        role: 'assistant',
        content: data.answer,
      };

      setMessages((prev) => [...prev, assistantMessage]);
    } catch (error) {
      console.error('Chat error:', error);
      toast({ title: 'Error', description: 'Failed to get response. Please try again.', variant: 'destructive' });
    } finally {
      setIsLoading(false);
    }
  };

  const handleKeyPress = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSendMessage();
    }
  };

  return (
    <div className="p-6 lg:p-10 gradient-surface min-h-full">
      <div className="max-w-4xl mx-auto">
        <div className="text-center mb-8 animate-fade-in">
          <h1 className="text-3xl md:text-4xl font-display font-bold text-foreground mb-3">
            Resume{" "}
            <span className="bg-gradient-to-r from-primary to-accent bg-clip-text text-transparent">Chatbot</span>
          </h1>
          <p className="text-muted-foreground max-w-lg mx-auto">
            Upload your resume and job description to chat with AI about your application.
          </p>
        </div>

        {!isChatEnabled ? (
          <div className="max-w-xl mx-auto animate-slide-up">
            <div className="p-6 rounded-xl border border-border bg-card shadow-soft space-y-5">
              <div className="space-y-2">
                <Label className="text-base font-medium">Your Resume (PDF)</Label>
                <FileUpload
                  onFileSelect={setFile}
                  selectedFile={file}
                  onClear={() => setFile(null)}
                />
              </div>

              <div className="space-y-2">
                <Label className="text-base font-medium">Job Description</Label>
                <Textarea
                  placeholder="Paste the job description here..."
                  value={jobDescription}
                  onChange={(e) => setJobDescription(e.target.value)}
                  className="min-h-[140px] bg-background"
                />
              </div>

              <Button
                variant="gradient"
                size="lg"
                className="w-full"
                onClick={handleStartChat}
                disabled={!file || !jobDescription.trim()}
              >
                <MessageSquare className="h-5 w-5" />
                <span>Start Chat</span>
              </Button>
            </div>
          </div>
        ) : (
          <div className="animate-fade-in">
            {/* Context Bar */}
            <div className="mb-4 p-3 rounded-lg border border-border bg-card flex items-center gap-4 text-sm">
              <div className="flex items-center gap-2 text-muted-foreground">
                <FileText className="h-4 w-4 text-primary" />
                <span className="truncate max-w-[150px]">{file?.name}</span>
              </div>
              <div className="h-4 w-px bg-border" />
              <span className="text-muted-foreground truncate flex-1">
                JD: {jobDescription.slice(0, 50)}...
              </span>
              <Button
                variant="ghost"
                size="sm"
                onClick={() => {
                  setIsChatEnabled(false);
                  setMessages([]);
                }}
              >
                Change
              </Button>
            </div>

            {/* Chat Container */}
            <div className="rounded-xl border border-border bg-card shadow-soft overflow-hidden">
              <ScrollArea className="h-[400px] p-4" ref={scrollRef}>
                <div className="space-y-4">
                  {messages.map((message, index) => (
                    <div
                      key={index}
                      className={`flex gap-3 ${message.role === 'user' ? 'flex-row-reverse' : ''}`}
                    >
                      <div className={`flex-shrink-0 h-8 w-8 rounded-full flex items-center justify-center ${
                        message.role === 'user' 
                          ? 'bg-primary text-primary-foreground' 
                          : 'bg-accent/20 text-accent'
                      }`}>
                        {message.role === 'user' ? (
                          <User className="h-4 w-4" />
                        ) : (
                          <Bot className="h-4 w-4" />
                        )}
                      </div>
                      <div className={`max-w-[80%] p-3 rounded-lg ${
                        message.role === 'user'
                          ? 'bg-primary text-primary-foreground'
                          : 'bg-muted text-foreground'
                      }`}>
                        <p className="text-sm whitespace-pre-wrap">{message.content}</p>
                      </div>
                    </div>
                  ))}
                  {isLoading && (
                    <div className="flex gap-3">
                      <div className="h-8 w-8 rounded-full bg-accent/20 flex items-center justify-center">
                        <Bot className="h-4 w-4 text-accent" />
                      </div>
                      <div className="bg-muted p-3 rounded-lg">
                        <Loader2 className="h-4 w-4 animate-spin text-muted-foreground" />
                      </div>
                    </div>
                  )}
                </div>
              </ScrollArea>

              {/* Input */}
              <div className="border-t border-border p-4">
                <div className="flex gap-2">
                  <Input
                    placeholder="Ask a question about your resume..."
                    value={input}
                    onChange={(e) => setInput(e.target.value)}
                    onKeyDown={handleKeyPress}
                    disabled={isLoading}
                    className="flex-1"
                  />
                  <Button
                    onClick={handleSendMessage}
                    disabled={!input.trim() || isLoading}
                    variant="gradient"
                  >
                    <Send className="h-4 w-4" />
                  </Button>
                </div>
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  );
};

export default ChatbotPage;
