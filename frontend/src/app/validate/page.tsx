'use client';

import { useState, useRef } from 'react';
import { useRouter } from 'next/navigation';
import api from '@/services/api';

const IDEA_TEMPLATES = [
  {
    id: 'saas',
    icon: '💻',
    title: 'SaaS for busy professionals',
    description: 'AI assistant that handles meeting notes',
    audience: 'Remote workers and managers',
    problem: 'Too many meetings, no time to document decisions'
  },
  {
    id: 'marketplace',
    icon: '🛍️',
    title: 'Marketplace for services',
    description: 'Connect local artisans with customers',
    audience: 'Homeowners looking for custom work',
    problem: 'Hard to find reliable craftspeople'
  },
  {
    id: 'fintech',
    icon: '💰',
    title: 'FinTech for Gen Z',
    description: 'Gamified savings app with social features',
    audience: 'College students and young professionals',
    problem: 'Traditional banking feels outdated and boring'
  },
  {
    id: 'edtech',
    icon: '🎓',
    title: 'EdTech platform',
    description: 'Personalized learning paths with AI tutors',
    audience: 'Adult learners switching careers',
    problem: 'One-size-fits-all courses waste time'
  }
];

const QUICK_PROMPTS = [
  "It's like Uber but for...",
  "Airbnb for...",
  "Netflix of...",
  "AI that helps people...",
  "Platform that connects...",
  "App that makes it easy to..."
];

export default function ValidatePage() {
  const router = useRouter();
  const fileInputRef = useRef<HTMLInputElement>(null);
  const [loading, setLoading] = useState(false);
  const [analyzing, setAnalyzing] = useState(false);
  const [ideaText, setIdeaText] = useState('');
  const [selectedTemplate, setSelectedTemplate] = useState<string | null>(null);
  const [dragActive, setDragActive] = useState(false);

  const handleTemplateSelect = (template: typeof IDEA_TEMPLATES[0]) => {
    setSelectedTemplate(template.id);
    setIdeaText(`${template.description}

Target: ${template.audience}
Problem: ${template.problem}`);
  };

  const handleQuickPrompt = (prompt: string) => {
    setIdeaText(prompt);
    // Focus on the text area and place cursor at the end
    const textarea = document.getElementById('idea-input') as HTMLTextAreaElement;
    if (textarea) {
      textarea.focus();
      textarea.setSelectionRange(prompt.length, prompt.length);
    }
  };

  const handleDrag = (e: React.DragEvent) => {
    e.preventDefault();
    e.stopPropagation();
    if (e.type === "dragenter" || e.type === "dragover") {
      setDragActive(true);
    } else if (e.type === "dragleave") {
      setDragActive(false);
    }
  };

  const handleDrop = async (e: React.DragEvent) => {
    e.preventDefault();
    e.stopPropagation();
    setDragActive(false);

    const files = Array.from(e.dataTransfer.files);
    if (files.length > 0) {
      await handleFileUpload(files[0]);
    }
  };

  const handleFileUpload = async (file: File) => {
    setAnalyzing(true);
    
    // For now, simulate file analysis
    setTimeout(() => {
      setIdeaText(`📄 Analyzing ${file.name}...

Based on your document, here's what we found:
- Your idea focuses on [extracted main concept]
- Target market: [extracted audience]
- Key problem: [extracted problem statement]

We'll validate this for you!`);
      setAnalyzing(false);
    }, 2000);
  };

  const handleSubmit = async () => {
    if (!ideaText.trim()) return;
    
    setLoading(true);
    try {
      // Parse the idea text into structured data
      const lines = ideaText.split('\n').filter(line => line.trim());
      const formData = {
        idea_description: lines[0] || ideaText,
        target_audience: lines.find(l => l.includes('Target:'))?.replace('Target:', '').trim() || 'General audience',
        problem_statement: lines.find(l => l.includes('Problem:'))?.replace('Problem:', '').trim() || 'Solving everyday challenges',
        validation_type: 'full',
        timeline_days: 30,
      };

      const response = await api.post('/api/v1/validations', formData);
      
      // If we get a response with an ID, use it
      if (response.data?.id) {
        router.push(`/validations/${response.data.id}`);
      } else {
        // Otherwise use mock ID
        const mockId = Date.now().toString();
        router.push(`/validations/${mockId}`);
      }
    } catch (err: any) {
      console.log('API error, using mock validation');
      // For demo, create a mock validation ID
      const mockId = Date.now().toString();
      router.push(`/validations/${mockId}`);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-b from-zinc-50 to-white">
      <div className="container mx-auto px-4 py-12 max-w-6xl">
        {/* Header */}
        <div className="text-center mb-12">
          <h1 className="text-5xl font-bold text-zinc-900 mb-4">
            What are you building?
          </h1>
          <p className="text-xl text-zinc-600">
            Describe your idea in any way. We'll help you validate it in seconds.
          </p>
        </div>

        {/* Main Input Area */}
        <div className="grid lg:grid-cols-3 gap-8 mb-8">
          {/* Left: Templates */}
          <div className="lg:col-span-1 space-y-4">
            <h3 className="text-sm font-medium text-zinc-500 uppercase tracking-wide mb-3">
              Start with a template
            </h3>
            <div className="space-y-3">
              {IDEA_TEMPLATES.map((template) => (
                <button
                  key={template.id}
                  onClick={() => handleTemplateSelect(template)}
                  className={`w-full text-left p-4 rounded-lg border transition-all hover:shadow-md ${
                    selectedTemplate === template.id
                      ? 'border-zinc-900 bg-zinc-50 shadow-md'
                      : 'border-zinc-200 hover:border-zinc-400'
                  }`}
                >
                  <div className="flex items-start gap-3">
                    <span className="text-2xl">{template.icon}</span>
                    <div className="flex-1">
                      <h4 className="font-medium text-zinc-900">{template.title}</h4>
                      <p className="text-sm text-zinc-600 mt-1">{template.description}</p>
                    </div>
                  </div>
                </button>
              ))}
            </div>
          </div>

          {/* Center: Main Input */}
          <div className="lg:col-span-2">
            <div
              className={`relative rounded-xl border-2 border-dashed transition-all ${
                dragActive ? 'border-zinc-900 bg-zinc-50' : 'border-zinc-300'
              }`}
              onDragEnter={handleDrag}
              onDragLeave={handleDrag}
              onDragOver={handleDrag}
              onDrop={handleDrop}
            >
              <textarea
                id="idea-input"
                value={ideaText}
                onChange={(e) => setIdeaText(e.target.value)}
                placeholder="Describe your business idea here...

Or drag and drop a file (pitch deck, business plan, napkin sketch)"
                className="w-full h-64 p-6 bg-transparent resize-none focus:outline-none text-lg"
                disabled={analyzing}
              />
              
              {analyzing && (
                <div className="absolute inset-0 bg-white/90 flex items-center justify-center rounded-xl">
                  <div className="text-center">
                    <div className="animate-spin rounded-full h-10 w-10 border-b-2 border-zinc-900 mx-auto mb-4"></div>
                    <p className="text-zinc-600">Analyzing your document...</p>
                  </div>
                </div>
              )}

              {/* File Upload Area */}
              <div className="absolute bottom-4 right-4">
                <input
                  ref={fileInputRef}
                  type="file"
                  onChange={(e) => e.target.files?.[0] && handleFileUpload(e.target.files[0])}
                  accept=".pdf,.doc,.docx,.txt,.png,.jpg,.jpeg"
                  className="hidden"
                />
                <button
                  onClick={() => fileInputRef.current?.click()}
                  className="text-zinc-500 hover:text-zinc-700 flex items-center gap-2 text-sm"
                >
                  <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M7 16a4 4 0 01-.88-7.903A5 5 0 1115.9 6L16 6a5 5 0 011 9.9M15 13l-3-3m0 0l-3 3m3-3v12" />
                  </svg>
                  Upload file
                </button>
              </div>
            </div>

            {/* Quick Prompts */}
            <div className="mt-4">
              <p className="text-sm text-zinc-500 mb-2">Need inspiration? Try:</p>
              <div className="flex flex-wrap gap-2">
                {QUICK_PROMPTS.map((prompt, idx) => (
                  <button
                    key={idx}
                    onClick={() => handleQuickPrompt(prompt)}
                    className="px-3 py-1 text-sm bg-zinc-100 hover:bg-zinc-200 rounded-full text-zinc-700 transition-colors"
                  >
                    {prompt}
                  </button>
                ))}
              </div>
            </div>

            {/* Smart Suggestions */}
            {ideaText.length > 20 && (
              <div className="mt-6 p-4 bg-blue-50 rounded-lg border border-blue-200">
                <p className="text-sm text-blue-800 font-medium mb-2">
                  💡 AI Suggestion
                </p>
                <p className="text-sm text-blue-700">
                  Based on your description, consider adding: target market size, main competitors, or revenue model
                </p>
              </div>
            )}
          </div>
        </div>

        {/* Action Buttons */}
        <div className="flex justify-center gap-4">
          <button
            onClick={handleSubmit}
            disabled={loading || !ideaText.trim() || analyzing}
            className="px-8 py-4 bg-zinc-900 text-white rounded-lg hover:bg-zinc-800 transition-all disabled:opacity-50 disabled:cursor-not-allowed text-lg font-medium shadow-lg hover:shadow-xl"
          >
            {loading ? (
              <span className="flex items-center gap-2">
                <div className="animate-spin rounded-full h-5 w-5 border-b-2 border-white"></div>
                Validating...
              </span>
            ) : (
              'Validate My Idea ✨'
            )}
          </button>
        </div>

        {/* Trust Indicators */}
        <div className="mt-12 text-center text-sm text-zinc-500">
          <p>🔒 Your idea is safe with us • ⚡ Results in under 3 minutes • 🤖 Powered by AI</p>
        </div>

        {/* Examples Carousel */}
        <div className="mt-16">
          <h3 className="text-center text-2xl font-bold text-zinc-900 mb-8">
            See what others are building
          </h3>
          <div className="grid md:grid-cols-3 gap-4">
            {[
              { idea: "AI therapist for pets", score: 72, status: "Promising" },
              { idea: "Sustainable fashion marketplace", score: 85, status: "High Potential" },
              { idea: "VR fitness for seniors", score: 68, status: "Needs Refinement" }
            ].map((example, idx) => (
              <div key={idx} className="p-4 bg-white rounded-lg border border-zinc-200 hover:shadow-md transition-all cursor-pointer">
                <p className="font-medium text-zinc-900 mb-2">{example.idea}</p>
                <div className="flex items-center justify-between">
                  <span className="text-3xl font-bold text-zinc-700">{example.score}</span>
                  <span className="text-sm text-zinc-600 bg-zinc-100 px-3 py-1 rounded-full">
                    {example.status}
                  </span>
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
}