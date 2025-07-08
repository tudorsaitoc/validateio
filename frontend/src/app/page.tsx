import Link from 'next/link';

export default function HomePage() {
  return (
    <div className="min-h-screen bg-gradient-to-b from-zinc-50 to-white">
      <div className="container mx-auto px-4 py-16">
        <header className="text-center mb-16">
          <h1 className="text-5xl font-bold text-zinc-900 mb-4">
            ValidateIO
          </h1>
          <p className="text-xl text-zinc-600 mb-8">
            AI-Powered Business Idea Validation in Under 3 Minutes
          </p>
          <div className="flex gap-4 justify-center">
            <Link
              href="/validate"
              className="px-6 py-3 bg-zinc-900 text-white rounded-lg hover:bg-zinc-800 transition-colors"
            >
              Start Validation
            </Link>
            <Link
              href="/login"
              className="px-6 py-3 border border-zinc-300 rounded-lg hover:bg-zinc-50 transition-colors"
            >
              Sign In
            </Link>
          </div>
        </header>

        <section className="grid md:grid-cols-3 gap-8 max-w-5xl mx-auto">
          <div className="bg-white p-6 rounded-lg shadow-sm border border-zinc-200">
            <div className="w-12 h-12 bg-zinc-100 rounded-lg flex items-center justify-center mb-4">
              <svg className="w-6 h-6 text-zinc-700" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z" />
              </svg>
            </div>
            <h3 className="text-lg font-semibold mb-2">Market Research</h3>
            <p className="text-zinc-600">
              AI analyzes competitors, market size, and customer pain points automatically
            </p>
          </div>

          <div className="bg-white p-6 rounded-lg shadow-sm border border-zinc-200">
            <div className="w-12 h-12 bg-zinc-100 rounded-lg flex items-center justify-center mb-4">
              <svg className="w-6 h-6 text-zinc-700" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 5 0 117.072 0l-.548.547A3.374 3.374 0 0014 18.469V19a2 2 0 11-4 0v-.531c0-.895-.356-1.754-.988-2.386l-.548-.547z" />
              </svg>
            </div>
            <h3 className="text-lg font-semibold mb-2">Experiment Generation</h3>
            <p className="text-zinc-600">
              Generate landing pages and A/B tests to validate product-market fit
            </p>
          </div>

          <div className="bg-white p-6 rounded-lg shadow-sm border border-zinc-200">
            <div className="w-12 h-12 bg-zinc-100 rounded-lg flex items-center justify-center mb-4">
              <svg className="w-6 h-6 text-zinc-700" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M11 5.882V19.24a1.76 1.76 0 01-3.417.592l-2.147-6.15M18 13a3 3 0 100-6M5.436 13.683A4.001 4.001 0 017 6h1.832c4.1 0 7.625-1.234 9.168-3v14c-1.543-1.766-5.067-3-9.168-3H7a3.988 3.988 0 01-1.564-.317z" />
              </svg>
            </div>
            <h3 className="text-lg font-semibold mb-2">Marketing Campaigns</h3>
            <p className="text-zinc-600">
              Create and launch targeted marketing campaigns based on validated insights
            </p>
          </div>
        </section>

        <section className="mt-16 text-center">
          <h2 className="text-3xl font-bold mb-4">How It Works</h2>
          <ol className="text-left max-w-2xl mx-auto space-y-4">
            <li className="flex gap-4">
              <span className="flex-shrink-0 w-8 h-8 bg-zinc-900 text-white rounded-full flex items-center justify-center font-semibold">1</span>
              <div>
                <h4 className="font-semibold">Describe Your Idea</h4>
                <p className="text-zinc-600">Enter your business idea and target market</p>
              </div>
            </li>
            <li className="flex gap-4">
              <span className="flex-shrink-0 w-8 h-8 bg-zinc-900 text-white rounded-full flex items-center justify-center font-semibold">2</span>
              <div>
                <h4 className="font-semibold">AI Validation</h4>
                <p className="text-zinc-600">Our AI agents research, experiment, and analyze your idea</p>
              </div>
            </li>
            <li className="flex gap-4">
              <span className="flex-shrink-0 w-8 h-8 bg-zinc-900 text-white rounded-full flex items-center justify-center font-semibold">3</span>
              <div>
                <h4 className="font-semibold">Get Results</h4>
                <p className="text-zinc-600">Receive comprehensive validation report in under 3 minutes</p>
              </div>
            </li>
          </ol>
        </section>
      </div>
    </div>
  );
}