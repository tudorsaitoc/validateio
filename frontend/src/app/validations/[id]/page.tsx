'use client';

import { useEffect, useState } from 'react';
import { useParams, useRouter } from 'next/navigation';
import Link from 'next/link';
import api from '@/services/api';

interface ValidationResult {
  id: string;
  idea_description: string;
  status: 'pending' | 'processing' | 'completed' | 'failed';
  created_at: string;
  completed_at?: string;
  results?: {
    market_analysis?: {
      market_size: string;
      growth_rate: string;
      trends: string[];
      opportunities: string[];
    };
    competitor_analysis?: {
      direct_competitors: Array<{
        name: string;
        strengths: string[];
        weaknesses: string[];
      }>;
      market_positioning: string;
    };
    viability_score?: {
      score: number;
      strengths: string[];
      weaknesses: string[];
      recommendations: string[];
    };
    experiments?: Array<{
      type: string;
      description: string;
      expected_outcome: string;
    }>;
  };
  error?: string;
}

export default function ValidationResultPage() {
  const params = useParams();
  const router = useRouter();
  const [validation, setValidation] = useState<ValidationResult | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    fetchValidation();
    // Poll for updates if status is pending/processing
    const interval = setInterval(() => {
      if (validation?.status === 'pending' || validation?.status === 'processing') {
        fetchValidation();
      }
    }, 3000);

    return () => clearInterval(interval);
  }, [params.id, validation?.status]);

  const fetchValidation = async () => {
    try {
      const response = await api.get(`/api/v1/validations/${params.id}`);
      setValidation(response.data);
    } catch (err: any) {
      console.error('Error fetching validation:', err);
      
      // Handle limited mode or missing endpoint
      if (err.response?.status === 404 || err.response?.data?.error === 'API running in limited mode') {
        // Mock data for demo purposes when API is limited
        setValidation({
          id: params.id as string,
          idea_description: 'Your business idea is being validated...',
          status: 'completed',
          created_at: new Date().toISOString(),
          completed_at: new Date().toISOString(),
          results: {
            market_analysis: {
              market_size: '$50 billion',
              growth_rate: '15% annually',
              trends: ['Digital transformation', 'Remote work adoption', 'AI integration'],
              opportunities: ['Underserved SMB segment', 'Mobile-first approach', 'Automation potential']
            },
            competitor_analysis: {
              direct_competitors: [
                {
                  name: 'Competitor A',
                  strengths: ['Market leader', 'Strong brand'],
                  weaknesses: ['High pricing', 'Complex UI']
                },
                {
                  name: 'Competitor B',
                  strengths: ['Good features', 'Fair pricing'],
                  weaknesses: ['Limited scalability', 'Poor support']
                }
              ],
              market_positioning: 'Opportunity to differentiate through simplicity and affordability'
            },
            viability_score: {
              score: 75,
              strengths: [
                'Addresses clear market need',
                'Scalable business model',
                'Strong differentiation potential'
              ],
              weaknesses: [
                'Competitive market',
                'Customer acquisition costs',
                'Technical complexity'
              ],
              recommendations: [
                'Start with MVP focusing on core features',
                'Target underserved SMB segment first',
                'Build strong content marketing strategy',
                'Consider freemium model for growth'
              ]
            },
            experiments: [
              {
                type: 'Landing Page',
                description: 'Create a simple landing page with value proposition',
                expected_outcome: 'Validate interest with 5% conversion rate'
              },
              {
                type: 'Customer Interviews',
                description: 'Interview 20 potential customers',
                expected_outcome: 'Validate problem-solution fit'
              }
            ]
          }
        });
        setError('Demo mode: Showing sample validation results');
      } else {
        setError('Failed to load validation results');
      }
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return (
      <div className="min-h-screen bg-gradient-to-b from-zinc-50 to-white py-8">
        <div className="container mx-auto px-4 max-w-4xl">
          <div className="animate-pulse">
            <div className="h-8 bg-zinc-200 rounded w-1/3 mb-4"></div>
            <div className="h-4 bg-zinc-200 rounded w-2/3 mb-8"></div>
            <div className="space-y-4">
              <div className="h-32 bg-zinc-200 rounded"></div>
              <div className="h-32 bg-zinc-200 rounded"></div>
            </div>
          </div>
        </div>
      </div>
    );
  }

  if (!validation) {
    return (
      <div className="min-h-screen bg-gradient-to-b from-zinc-50 to-white py-8">
        <div className="container mx-auto px-4 max-w-4xl text-center">
          <h1 className="text-2xl font-bold text-zinc-900 mb-4">Validation Not Found</h1>
          <Link href="/validate" className="text-zinc-600 hover:text-zinc-900">
            Start a new validation
          </Link>
        </div>
      </div>
    );
  }

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'completed': return 'bg-green-100 text-green-800';
      case 'processing': return 'bg-blue-100 text-blue-800';
      case 'failed': return 'bg-red-100 text-red-800';
      default: return 'bg-yellow-100 text-yellow-800';
    }
  };

  const getViabilityColor = (score: number) => {
    if (score >= 70) return 'text-green-600';
    if (score >= 50) return 'text-yellow-600';
    return 'text-red-600';
  };

  return (
    <div className="min-h-screen bg-gradient-to-b from-zinc-50 to-white py-8">
      <div className="container mx-auto px-4 max-w-4xl">
        <div className="mb-8">
          <Link href="/" className="text-zinc-600 hover:text-zinc-900 mb-4 inline-block">
            ← Back to Home
          </Link>
          
          {error && (
            <div className="bg-blue-50 border border-blue-200 text-blue-700 px-4 py-3 rounded-lg mb-4">
              {error}
            </div>
          )}

          <div className="flex items-center justify-between mb-4">
            <h1 className="text-3xl font-bold text-zinc-900">Validation Results</h1>
            <span className={`px-3 py-1 rounded-full text-sm font-medium ${getStatusColor(validation.status)}`}>
              {validation.status.charAt(0).toUpperCase() + validation.status.slice(1)}
            </span>
          </div>
          
          <p className="text-zinc-600">{validation.idea_description}</p>
        </div>

        {validation.status === 'pending' || validation.status === 'processing' ? (
          <div className="bg-white p-8 rounded-lg shadow-sm border border-zinc-200 text-center">
            <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-zinc-900 mx-auto mb-4"></div>
            <h2 className="text-xl font-semibold mb-2">Validating Your Idea</h2>
            <p className="text-zinc-600">Our AI agents are analyzing your business idea. This usually takes 2-3 minutes.</p>
          </div>
        ) : validation.status === 'failed' ? (
          <div className="bg-red-50 p-8 rounded-lg border border-red-200 text-center">
            <h2 className="text-xl font-semibold text-red-800 mb-2">Validation Failed</h2>
            <p className="text-red-600">{validation.error || 'An error occurred during validation. Please try again.'}</p>
            <Link href="/validate" className="mt-4 inline-block px-6 py-3 bg-zinc-900 text-white rounded-lg hover:bg-zinc-800">
              Try Again
            </Link>
          </div>
        ) : validation.results ? (
          <div className="space-y-6">
            {/* Viability Score */}
            {validation.results.viability_score && (
              <div className="bg-white p-6 rounded-lg shadow-sm border border-zinc-200">
                <h2 className="text-xl font-semibold mb-4">Viability Score</h2>
                <div className="flex items-center mb-4">
                  <div className={`text-5xl font-bold ${getViabilityColor(validation.results.viability_score.score)}`}>
                    {validation.results.viability_score.score}
                  </div>
                  <div className="text-xl text-zinc-600 ml-2">/ 100</div>
                </div>
                
                <div className="grid md:grid-cols-2 gap-4">
                  <div>
                    <h3 className="font-medium text-green-700 mb-2">Strengths</h3>
                    <ul className="space-y-1">
                      {validation.results.viability_score.strengths.map((strength, idx) => (
                        <li key={idx} className="text-sm text-zinc-600 flex items-start">
                          <span className="text-green-500 mr-2">✓</span>
                          {strength}
                        </li>
                      ))}
                    </ul>
                  </div>
                  
                  <div>
                    <h3 className="font-medium text-red-700 mb-2">Weaknesses</h3>
                    <ul className="space-y-1">
                      {validation.results.viability_score.weaknesses.map((weakness, idx) => (
                        <li key={idx} className="text-sm text-zinc-600 flex items-start">
                          <span className="text-red-500 mr-2">✗</span>
                          {weakness}
                        </li>
                      ))}
                    </ul>
                  </div>
                </div>

                <div className="mt-4">
                  <h3 className="font-medium text-zinc-700 mb-2">Recommendations</h3>
                  <ul className="space-y-2">
                    {validation.results.viability_score.recommendations.map((rec, idx) => (
                      <li key={idx} className="text-sm text-zinc-600 flex items-start">
                        <span className="text-blue-500 mr-2">→</span>
                        {rec}
                      </li>
                    ))}
                  </ul>
                </div>
              </div>
            )}

            {/* Market Analysis */}
            {validation.results.market_analysis && (
              <div className="bg-white p-6 rounded-lg shadow-sm border border-zinc-200">
                <h2 className="text-xl font-semibold mb-4">Market Analysis</h2>
                <div className="grid md:grid-cols-2 gap-4 mb-4">
                  <div>
                    <h3 className="text-sm font-medium text-zinc-500">Market Size</h3>
                    <p className="text-lg font-semibold">{validation.results.market_analysis.market_size}</p>
                  </div>
                  <div>
                    <h3 className="text-sm font-medium text-zinc-500">Growth Rate</h3>
                    <p className="text-lg font-semibold">{validation.results.market_analysis.growth_rate}</p>
                  </div>
                </div>
                
                <div className="space-y-3">
                  <div>
                    <h3 className="font-medium text-zinc-700 mb-2">Key Trends</h3>
                    <div className="flex flex-wrap gap-2">
                      {validation.results.market_analysis.trends.map((trend, idx) => (
                        <span key={idx} className="px-3 py-1 bg-zinc-100 text-zinc-700 rounded-full text-sm">
                          {trend}
                        </span>
                      ))}
                    </div>
                  </div>
                  
                  <div>
                    <h3 className="font-medium text-zinc-700 mb-2">Opportunities</h3>
                    <ul className="space-y-1">
                      {validation.results.market_analysis.opportunities.map((opp, idx) => (
                        <li key={idx} className="text-sm text-zinc-600">• {opp}</li>
                      ))}
                    </ul>
                  </div>
                </div>
              </div>
            )}

            {/* Competitor Analysis */}
            {validation.results.competitor_analysis && (
              <div className="bg-white p-6 rounded-lg shadow-sm border border-zinc-200">
                <h2 className="text-xl font-semibold mb-4">Competitor Analysis</h2>
                <div className="space-y-4">
                  {validation.results.competitor_analysis.direct_competitors.map((comp, idx) => (
                    <div key={idx} className="border-l-4 border-zinc-200 pl-4">
                      <h3 className="font-medium text-zinc-900 mb-2">{comp.name}</h3>
                      <div className="grid md:grid-cols-2 gap-2 text-sm">
                        <div>
                          <span className="text-green-600 font-medium">Strengths:</span>
                          <ul className="text-zinc-600">
                            {comp.strengths.map((s, i) => (
                              <li key={i}>• {s}</li>
                            ))}
                          </ul>
                        </div>
                        <div>
                          <span className="text-red-600 font-medium">Weaknesses:</span>
                          <ul className="text-zinc-600">
                            {comp.weaknesses.map((w, i) => (
                              <li key={i}>• {w}</li>
                            ))}
                          </ul>
                        </div>
                      </div>
                    </div>
                  ))}
                  
                  <div className="mt-4 p-4 bg-zinc-50 rounded-lg">
                    <h3 className="font-medium text-zinc-700 mb-1">Market Positioning</h3>
                    <p className="text-sm text-zinc-600">{validation.results.competitor_analysis.market_positioning}</p>
                  </div>
                </div>
              </div>
            )}

            {/* Suggested Experiments */}
            {validation.results.experiments && (
              <div className="bg-white p-6 rounded-lg shadow-sm border border-zinc-200">
                <h2 className="text-xl font-semibold mb-4">Suggested Experiments</h2>
                <div className="space-y-3">
                  {validation.results.experiments.map((exp, idx) => (
                    <div key={idx} className="border-l-4 border-blue-200 pl-4">
                      <h3 className="font-medium text-zinc-900">{exp.type}</h3>
                      <p className="text-sm text-zinc-600 mt-1">{exp.description}</p>
                      <p className="text-sm text-zinc-500 mt-1">
                        <span className="font-medium">Expected outcome:</span> {exp.expected_outcome}
                      </p>
                    </div>
                  ))}
                </div>
              </div>
            )}

            {/* Action Buttons */}
            <div className="flex gap-4 mt-8">
              <Link
                href="/validate"
                className="flex-1 px-6 py-3 bg-zinc-900 text-white text-center rounded-lg hover:bg-zinc-800 transition-colors"
              >
                Validate Another Idea
              </Link>
              <button
                onClick={() => window.print()}
                className="px-6 py-3 border border-zinc-300 rounded-lg hover:bg-zinc-50 transition-colors"
              >
                Export Report
              </button>
            </div>
          </div>
        ) : null}
      </div>
    </div>
  );
}