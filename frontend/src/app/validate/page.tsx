'use client';

import { useState } from 'react';
import { useRouter } from 'next/navigation';
import api from '@/services/api';

interface ValidationFormData {
  idea_description: string;
  target_audience: string;
  problem_statement: string;
  value_proposition?: string;
  market_size?: string;
  competitors?: string[];
  unique_features?: string[];
  revenue_model?: string;
}

export default function ValidatePage() {
  const router = useRouter();
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [formData, setFormData] = useState<ValidationFormData>({
    idea_description: '',
    target_audience: '',
    problem_statement: '',
    value_proposition: '',
    market_size: '',
    competitors: [],
    unique_features: [],
    revenue_model: '',
  });

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError('');
    setLoading(true);

    try {
      // Test if API is working first
      const healthCheck = await api.get('/health');
      console.log('API Health:', healthCheck.data);

      // Submit validation
      const response = await api.post('/api/v1/validations', {
        ...formData,
        validation_type: 'full',
        timeline_days: 30,
      });

      console.log('Validation created:', response.data);
      
      // Redirect to results page
      router.push(`/validations/${response.data.id}`);
    } catch (err: any) {
      console.error('Validation error:', err);
      
      // Check if API is in limited mode
      if (err.response?.data?.error === 'API running in limited mode') {
        setError('The API is currently running in limited mode. Full validation features are being set up.');
      } else {
        setError(err.response?.data?.detail || 'Failed to create validation. Please try again.');
      }
    } finally {
      setLoading(false);
    }
  };

  const handleCompetitorAdd = (e: React.KeyboardEvent<HTMLInputElement>) => {
    if (e.key === 'Enter' && e.currentTarget.value) {
      e.preventDefault();
      setFormData({
        ...formData,
        competitors: [...(formData.competitors || []), e.currentTarget.value],
      });
      e.currentTarget.value = '';
    }
  };

  const handleFeatureAdd = (e: React.KeyboardEvent<HTMLInputElement>) => {
    if (e.key === 'Enter' && e.currentTarget.value) {
      e.preventDefault();
      setFormData({
        ...formData,
        unique_features: [...(formData.unique_features || []), e.currentTarget.value],
      });
      e.currentTarget.value = '';
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-b from-zinc-50 to-white py-8">
      <div className="container mx-auto px-4 max-w-3xl">
        <h1 className="text-4xl font-bold text-zinc-900 mb-8">Validate Your Idea</h1>
        
        {error && (
          <div className="bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded-lg mb-6">
            {error}
          </div>
        )}

        <form onSubmit={handleSubmit} className="space-y-6">
          <div className="bg-white p-6 rounded-lg shadow-sm border border-zinc-200">
            <h2 className="text-xl font-semibold mb-4">Core Information</h2>
            
            <div className="space-y-4">
              <div>
                <label htmlFor="idea" className="block text-sm font-medium text-zinc-700 mb-1">
                  Business Idea Description *
                </label>
                <textarea
                  id="idea"
                  required
                  rows={4}
                  className="w-full px-3 py-2 border border-zinc-300 rounded-lg focus:ring-2 focus:ring-zinc-500 focus:border-transparent"
                  placeholder="Describe your business idea in detail..."
                  value={formData.idea_description}
                  onChange={(e) => setFormData({ ...formData, idea_description: e.target.value })}
                />
              </div>

              <div>
                <label htmlFor="audience" className="block text-sm font-medium text-zinc-700 mb-1">
                  Target Audience *
                </label>
                <input
                  id="audience"
                  type="text"
                  required
                  className="w-full px-3 py-2 border border-zinc-300 rounded-lg focus:ring-2 focus:ring-zinc-500 focus:border-transparent"
                  placeholder="Who is your target customer?"
                  value={formData.target_audience}
                  onChange={(e) => setFormData({ ...formData, target_audience: e.target.value })}
                />
              </div>

              <div>
                <label htmlFor="problem" className="block text-sm font-medium text-zinc-700 mb-1">
                  Problem Statement *
                </label>
                <textarea
                  id="problem"
                  required
                  rows={3}
                  className="w-full px-3 py-2 border border-zinc-300 rounded-lg focus:ring-2 focus:ring-zinc-500 focus:border-transparent"
                  placeholder="What problem does your idea solve?"
                  value={formData.problem_statement}
                  onChange={(e) => setFormData({ ...formData, problem_statement: e.target.value })}
                />
              </div>
            </div>
          </div>

          <div className="bg-white p-6 rounded-lg shadow-sm border border-zinc-200">
            <h2 className="text-xl font-semibold mb-4">Additional Details (Optional)</h2>
            
            <div className="space-y-4">
              <div>
                <label htmlFor="value" className="block text-sm font-medium text-zinc-700 mb-1">
                  Value Proposition
                </label>
                <input
                  id="value"
                  type="text"
                  className="w-full px-3 py-2 border border-zinc-300 rounded-lg focus:ring-2 focus:ring-zinc-500 focus:border-transparent"
                  placeholder="What unique value do you provide?"
                  value={formData.value_proposition}
                  onChange={(e) => setFormData({ ...formData, value_proposition: e.target.value })}
                />
              </div>

              <div>
                <label htmlFor="market" className="block text-sm font-medium text-zinc-700 mb-1">
                  Market Size Estimate
                </label>
                <input
                  id="market"
                  type="text"
                  className="w-full px-3 py-2 border border-zinc-300 rounded-lg focus:ring-2 focus:ring-zinc-500 focus:border-transparent"
                  placeholder="e.g., $50 billion global market"
                  value={formData.market_size}
                  onChange={(e) => setFormData({ ...formData, market_size: e.target.value })}
                />
              </div>

              <div>
                <label className="block text-sm font-medium text-zinc-700 mb-1">
                  Known Competitors (Press Enter to add)
                </label>
                <input
                  type="text"
                  className="w-full px-3 py-2 border border-zinc-300 rounded-lg focus:ring-2 focus:ring-zinc-500 focus:border-transparent"
                  placeholder="Add competitor name and press Enter"
                  onKeyDown={handleCompetitorAdd}
                />
                {formData.competitors && formData.competitors.length > 0 && (
                  <div className="mt-2 flex flex-wrap gap-2">
                    {formData.competitors.map((comp, idx) => (
                      <span
                        key={idx}
                        className="px-3 py-1 bg-zinc-100 text-zinc-700 rounded-full text-sm flex items-center gap-2"
                      >
                        {comp}
                        <button
                          type="button"
                          onClick={() => setFormData({
                            ...formData,
                            competitors: formData.competitors?.filter((_, i) => i !== idx),
                          })}
                          className="text-zinc-500 hover:text-zinc-700"
                        >
                          ×
                        </button>
                      </span>
                    ))}
                  </div>
                )}
              </div>

              <div>
                <label className="block text-sm font-medium text-zinc-700 mb-1">
                  Unique Features (Press Enter to add)
                </label>
                <input
                  type="text"
                  className="w-full px-3 py-2 border border-zinc-300 rounded-lg focus:ring-2 focus:ring-zinc-500 focus:border-transparent"
                  placeholder="Add unique feature and press Enter"
                  onKeyDown={handleFeatureAdd}
                />
                {formData.unique_features && formData.unique_features.length > 0 && (
                  <div className="mt-2 flex flex-wrap gap-2">
                    {formData.unique_features.map((feature, idx) => (
                      <span
                        key={idx}
                        className="px-3 py-1 bg-zinc-100 text-zinc-700 rounded-full text-sm flex items-center gap-2"
                      >
                        {feature}
                        <button
                          type="button"
                          onClick={() => setFormData({
                            ...formData,
                            unique_features: formData.unique_features?.filter((_, i) => i !== idx),
                          })}
                          className="text-zinc-500 hover:text-zinc-700"
                        >
                          ×
                        </button>
                      </span>
                    ))}
                  </div>
                )}
              </div>

              <div>
                <label htmlFor="revenue" className="block text-sm font-medium text-zinc-700 mb-1">
                  Revenue Model
                </label>
                <input
                  id="revenue"
                  type="text"
                  className="w-full px-3 py-2 border border-zinc-300 rounded-lg focus:ring-2 focus:ring-zinc-500 focus:border-transparent"
                  placeholder="How will you make money?"
                  value={formData.revenue_model}
                  onChange={(e) => setFormData({ ...formData, revenue_model: e.target.value })}
                />
              </div>
            </div>
          </div>

          <div className="flex gap-4">
            <button
              type="submit"
              disabled={loading}
              className="flex-1 px-6 py-3 bg-zinc-900 text-white rounded-lg hover:bg-zinc-800 transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
            >
              {loading ? 'Validating...' : 'Start Validation'}
            </button>
            <button
              type="button"
              onClick={() => router.push('/')}
              className="px-6 py-3 border border-zinc-300 rounded-lg hover:bg-zinc-50 transition-colors"
            >
              Cancel
            </button>
          </div>
        </form>
      </div>
    </div>
  );
}