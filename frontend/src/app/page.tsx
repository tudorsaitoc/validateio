import Link from 'next/link';

export default function HomePage() {
  return (
    <div className="min-h-screen bg-gradient-to-b from-zinc-50 to-white">
      {/* Hero Section */}
      <div className="container mx-auto px-4 py-20">
        <div className="text-center max-w-4xl mx-auto">
          <div className="inline-flex items-center gap-2 px-4 py-2 bg-zinc-100 rounded-full text-sm text-zinc-700 mb-8">
            <span className="animate-pulse">🚀</span>
            <span>Validate ideas in seconds, not months</span>
          </div>
          
          <h1 className="text-6xl md:text-7xl font-bold text-zinc-900 mb-6 leading-tight">
            Turn your idea into
            <br />
            <span className="bg-gradient-to-r from-zinc-700 to-zinc-900 bg-clip-text text-transparent">
              validated reality
            </span>
          </h1>
          
          <p className="text-xl md:text-2xl text-zinc-600 mb-12 leading-relaxed">
            Drop in your business idea, pitch deck, or even a napkin sketch.
            <br />
            Get AI-powered validation and experiments in under 3 minutes.
          </p>

          {/* CTA Section */}
          <div className="flex flex-col sm:flex-row gap-4 justify-center items-center mb-8">
            <Link
              href="/validate"
              className="group px-8 py-4 bg-zinc-900 text-white rounded-xl hover:bg-zinc-800 transition-all text-lg font-medium shadow-lg hover:shadow-2xl flex items-center gap-2"
            >
              Start Validating
              <svg className="w-5 h-5 group-hover:translate-x-1 transition-transform" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5l7 7-7 7" />
              </svg>
            </Link>
            
            <button className="px-8 py-4 border-2 border-zinc-300 rounded-xl hover:border-zinc-400 transition-all text-lg font-medium flex items-center gap-2">
              <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M14.752 11.168l-3.197-2.132A1 1 0 0010 9.87v4.263a1 1 0 001.555.832l3.197-2.132a1 1 0 000-1.664z" />
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
              </svg>
              Watch Demo
            </button>
          </div>

          {/* Quick Input Preview */}
          <div className="relative max-w-2xl mx-auto">
            <div className="absolute inset-0 bg-gradient-to-r from-zinc-200 to-zinc-300 rounded-2xl blur-xl opacity-50"></div>
            <div className="relative bg-white rounded-2xl shadow-xl p-6 border border-zinc-200">
              <div className="flex items-center gap-3 mb-4">
                <div className="w-3 h-3 bg-red-500 rounded-full"></div>
                <div className="w-3 h-3 bg-yellow-500 rounded-full"></div>
                <div className="w-3 h-3 bg-green-500 rounded-full"></div>
                <span className="text-sm text-zinc-500 ml-2">validateio.app</span>
              </div>
              
              <div className="text-left">
                <p className="text-zinc-600 mb-2">Try it now:</p>
                <div className="bg-zinc-50 rounded-lg p-4 font-mono text-sm">
                  <span className="text-zinc-500">$</span> It's like Uber but for dog walking...
                  <span className="animate-pulse">|</span>
                </div>
              </div>
              
              <div className="mt-4 flex items-center gap-2 text-sm text-zinc-500">
                <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 10V3L4 14h7v7l9-11h-7z" />
                </svg>
                <span>AI analyzing market opportunity...</span>
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* Features Grid */}
      <div className="container mx-auto px-4 py-20">
        <div className="grid md:grid-cols-3 gap-8 max-w-5xl mx-auto">
          <div className="group hover:scale-105 transition-transform">
            <div className="bg-white p-8 rounded-2xl shadow-lg border border-zinc-200 h-full">
              <div className="w-14 h-14 bg-gradient-to-br from-blue-100 to-blue-200 rounded-xl flex items-center justify-center mb-6 group-hover:scale-110 transition-transform">
                <span className="text-2xl">🔍</span>
              </div>
              <h3 className="text-xl font-bold mb-3">Smart Research</h3>
              <p className="text-zinc-600">
                AI agents analyze competitors, market size, and validate demand automatically
              </p>
            </div>
          </div>

          <div className="group hover:scale-105 transition-transform">
            <div className="bg-white p-8 rounded-2xl shadow-lg border border-zinc-200 h-full">
              <div className="w-14 h-14 bg-gradient-to-br from-green-100 to-green-200 rounded-xl flex items-center justify-center mb-6 group-hover:scale-110 transition-transform">
                <span className="text-2xl">🧪</span>
              </div>
              <h3 className="text-xl font-bold mb-3">Instant Experiments</h3>
              <p className="text-zinc-600">
                Generate landing pages, A/B tests, and validation experiments in seconds
              </p>
            </div>
          </div>

          <div className="group hover:scale-105 transition-transform">
            <div className="bg-white p-8 rounded-2xl shadow-lg border border-zinc-200 h-full">
              <div className="w-14 h-14 bg-gradient-to-br from-purple-100 to-purple-200 rounded-xl flex items-center justify-center mb-6 group-hover:scale-110 transition-transform">
                <span className="text-2xl">📊</span>
              </div>
              <h3 className="text-xl font-bold mb-3">Actionable Insights</h3>
              <p className="text-zinc-600">
                Get clear recommendations, viability scores, and next steps to move forward
              </p>
            </div>
          </div>
        </div>
      </div>

      {/* Social Proof */}
      <div className="bg-zinc-50 py-20">
        <div className="container mx-auto px-4">
          <h2 className="text-3xl font-bold text-center mb-12">
            Ideas validated this week
          </h2>
          
          <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6 max-w-5xl mx-auto">
            {[
              { 
                idea: "AI-powered meal planning for busy parents",
                time: "2 hours ago",
                score: 82,
                avatar: "👩‍🍳"
              },
              { 
                idea: "Blockchain ticketing for small venues",
                time: "5 hours ago",
                score: 67,
                avatar: "🎫"
              },
              { 
                idea: "Mental health app for remote workers",
                time: "Yesterday",
                score: 91,
                avatar: "🧠"
              },
              { 
                idea: "Sustainable packaging marketplace",
                time: "Yesterday",
                score: 78,
                avatar: "📦"
              },
              { 
                idea: "Pet care scheduling platform",
                time: "2 days ago",
                score: 85,
                avatar: "🐕"
              },
              { 
                idea: "AR furniture visualization tool",
                time: "3 days ago",
                score: 73,
                avatar: "🪑"
              }
            ].map((item, idx) => (
              <div key={idx} className="bg-white p-6 rounded-xl border border-zinc-200 hover:shadow-lg transition-all cursor-pointer">
                <div className="flex items-start justify-between mb-3">
                  <div className="flex items-center gap-3">
                    <span className="text-3xl">{item.avatar}</span>
                    <span className="text-sm text-zinc-500">{item.time}</span>
                  </div>
                  <div className="text-right">
                    <div className="text-2xl font-bold text-zinc-900">{item.score}</div>
                    <div className="text-xs text-zinc-500">score</div>
                  </div>
                </div>
                <p className="text-zinc-700 font-medium">{item.idea}</p>
              </div>
            ))}
          </div>
        </div>
      </div>

      {/* Footer CTA */}
      <div className="container mx-auto px-4 py-20">
        <div className="bg-zinc-900 rounded-3xl p-12 text-center text-white">
          <h2 className="text-3xl md:text-4xl font-bold mb-4">
            Stop wondering "what if?"
          </h2>
          <p className="text-xl text-zinc-300 mb-8">
            Validate your idea in minutes, not months
          </p>
          <Link
            href="/validate"
            className="inline-flex items-center gap-2 px-8 py-4 bg-white text-zinc-900 rounded-xl hover:bg-zinc-100 transition-all text-lg font-medium"
          >
            Start for free
            <span className="text-2xl">→</span>
          </Link>
        </div>
      </div>
    </div>
  );
}