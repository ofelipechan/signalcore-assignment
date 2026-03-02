import { useLocation, useNavigate } from 'react-router-dom'
import ReactMarkdown from 'react-markdown'
import remarkGfm from 'remark-gfm'
import { ArrowLeft, ExternalLink } from 'lucide-react'
import type { ResearchResponse, Source } from '@/types/api'

interface LocationState {
  result?: ResearchResponse
}

function SourceItem({ source }: { source: Source }) {
  return (
    <li className="flex flex-col gap-1 py-2 border-b border-ai-border last:border-0">
      <a
        href={source.url}
        target="_blank"
        rel="noopener noreferrer"
        className="inline-flex items-center gap-1.5 text-ai-primary hover:underline text-sm font-medium cursor-pointer"
      >
        {source.title || source.url}
        <ExternalLink className="w-3.5 h-3.5 shrink-0" aria-hidden />
      </a>
    </li>
  )
}

export function ResultsPage() {
  const location = useLocation()
  const navigate = useNavigate()
  const state = location.state as LocationState | null
  const result = state?.result

  if (!result) {
    return (
      <div className="min-h-screen flex flex-col items-center justify-center px-4 bg-ai-bg">
        <p className="text-ai-muted mb-4">No results to show.</p>
        <button
          type="button"
          onClick={() => navigate('/')}
          className="inline-flex items-center gap-2 text-ai-primary hover:underline cursor-pointer"
        >
          <ArrowLeft className="w-4 h-4" />
          Back to search
        </button>
      </div>
    )
  }

  const { markdown, sources } = result

  return (
    <div className="min-h-screen bg-ai-bg">
      <header className="sticky top-0 z-10 border-b border-ai-border bg-ai-bg/95 backdrop-blur">
        <div className="max-w-4xl mx-auto px-4 py-3 flex items-center justify-between">
          <button
            type="button"
            onClick={() => navigate('/')}
            className="inline-flex items-center gap-2 text-ai-muted hover:text-white transition cursor-pointer"
          >
            <ArrowLeft className="w-4 h-4" />
            New research
          </button>
          <h1 className="text-lg font-semibold text-white">Research results</h1>
          <span className="w-20" aria-hidden />
        </div>
      </header>

      <div className="max-w-4xl mx-auto px-4 py-8 flex flex-col gap-8">
        <main className="min-w-0">
          <article className="markdown-body max-w-none">
            <ReactMarkdown remarkPlugins={[remarkGfm]}>
              {markdown || '_No content._'}
            </ReactMarkdown>
          </article>
        </main>

        <section
          className="rounded-xl border border-ai-border bg-ai-surface p-4"
          aria-label="Sources"
        >
          <h2 className="text-sm font-semibold text-white mb-3">
            Sources ({sources.length})
          </h2>
          <p className="text-ai-muted text-xs mb-4">
            Where this information came from. Use links to verify.
          </p>
          {sources.length > 0 ? (
            <ul className="space-y-0">
              {sources.map((source, i) => (
                <SourceItem key={`${source.url}-${i}`} source={source} />
              ))}
            </ul>
          ) : (
            <p className="text-ai-muted text-sm">No sources recorded.</p>
          )}
        </section>
      </div>
    </div>
  )
}
