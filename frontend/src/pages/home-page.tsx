import { useState, useCallback, useEffect } from 'react'
import { useNavigate } from 'react-router-dom'
import { Loader2 } from 'lucide-react'
import { runResearch } from '@/api/research'
import type { ResearchResponse } from '@/types/api'

const LOADING_MESSAGES = [
  'researching...',
  'thinking...',
  'please wait...',
  'processing....',
  'researching...',
] as const
const MESSAGE_INTERVAL_MS = 10_000

const DEFAULT_PROMPT = `We need to select an LLM observability platform to monitor, trace, and evaluate our production LLM applications. We run a mix of RAG pipelines and multi-step agents and need to compare vendors before committing.

Vendors to evaluate:
- LangSmith
- Langfuse
- Braintrust
- Posthog

Requirements to evaluate against (by priority):
- High: Framework-agnostic tracing (not locked into LangChain or any single framework)
- High: Self-hosting option with full data sovereignty
- High: Built-in evaluation framework (LLM-as-judge, custom metrics, regression testing)
- Medium: OpenTelemetry support for integration with existing observability stack
- Medium: Prompt management and versioning with rollback capability
- Low: Transparent, predictable pricing at scale (100K+ traces/month)

Compare these four vendors against the requirements above and help us decide.`

export function HomePage() {
  const [prompt, setPrompt] = useState(DEFAULT_PROMPT)
  const [isLoading, setIsLoading] = useState(false)
  const [loadingMessageIndex, setLoadingMessageIndex] = useState(0)
  const [error, setError] = useState<string | null>(null)
  const navigate = useNavigate()

  useEffect(() => {
    if (!isLoading) return
    setLoadingMessageIndex(0)
    const id = setInterval(() => {
      setLoadingMessageIndex((i) => (i + 1) % LOADING_MESSAGES.length)
    }, MESSAGE_INTERVAL_MS)
    return () => clearInterval(id)
  }, [isLoading])

  const handleSubmit = useCallback(
    async (e: React.FormEvent) => {
      e.preventDefault()
      const trimmed = prompt.trim()
      if (!trimmed || isLoading) return
      setIsLoading(true)
      setError(null)
      try {
        const result: ResearchResponse = await runResearch({ prompt: trimmed })
        navigate('/results', { state: { result } })
      } catch (err) {
        setError(err instanceof Error ? err.message : 'Research request failed')
      } finally {
        setIsLoading(false)
      }
    },
    [prompt, isLoading, navigate]
  )

  const locked = isLoading

  return (
    <div className="min-h-screen flex flex-col items-center justify-center px-4 py-12 bg-ai-bg">
      <div className="w-full max-w-2xl mx-auto">
        <header className="text-center mb-10">
          <h1 className="text-3xl font-bold text-white tracking-tight">
            Vendor Research
          </h1>
          <p className="mt-2 text-ai-muted text-sm">
            Describe what you need and we’ll compare options for you
          </p>
        </header>

        <form onSubmit={handleSubmit} className="space-y-6">
          <div>
            <label htmlFor="prompt" className="sr-only">
              Research prompt
            </label>
            <textarea
              id="prompt"
              name="prompt"
              value={prompt}
              onChange={(e) => setPrompt(e.target.value)}
              disabled={locked}
              placeholder="e.g. Compare observability platforms for production LLM apps. I need tracing, metrics, and support for LangChain. Evaluate Langsmith, Langfuse, and Braintrust."
              rows={6}
              className="w-full px-4 py-3 rounded-xl border border-ai-border bg-ai-surface text-white placeholder:text-ai-muted focus:outline-none focus:ring-2 focus:ring-ai-primary focus:border-transparent resize-y min-h-[140px] disabled:opacity-60 disabled:cursor-not-allowed transition duration-200"
              aria-describedby={error ? 'prompt-error' : undefined}
            />
            {error && (
              <p id="prompt-error" className="mt-2 text-sm text-red-400" role="alert">
                {error}
              </p>
            )}
          </div>

          <div className="flex justify-center">
            <button
              type="submit"
              disabled={locked || !prompt.trim()}
              className="inline-flex items-center gap-2 px-6 py-3 rounded-xl bg-ai-primary text-white font-medium hover:bg-indigo-600 focus:outline-none focus:ring-2 focus:ring-ai-primary focus:ring-offset-2 focus:ring-offset-ai-bg disabled:opacity-60 disabled:cursor-not-allowed transition duration-200 cursor-pointer"
            >
              {isLoading ? (
                <>
                  <Loader2 className="w-5 h-5 animate-spin" aria-hidden />
                  <span>{LOADING_MESSAGES[loadingMessageIndex]}</span>
                </>
              ) : (
                <span>Start research</span>
              )}
            </button>
          </div>
        </form>

        <p className="mt-8 text-center text-ai-muted text-xs max-w-md mx-auto">
          The AI will search the web and compare vendors based on your requirements. Results open on a new page with sources you can verify.
        </p>
      </div>
    </div>
  )
}
