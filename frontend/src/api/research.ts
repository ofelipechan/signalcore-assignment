import type { ResearchRequest, ResearchResponse } from '@/types/api'

const API_BASE =
  import.meta.env.VITE_API_URL ?? 'http://localhost:8001'

export async function runResearch(
  payload: ResearchRequest
): Promise<ResearchResponse> {
  const res = await fetch(`${API_BASE}/api/research`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ prompt: payload.prompt }),
  })
  if (!res.ok) {
    const text = await res.text()
    throw new Error(text || `HTTP ${res.status}`)
  }
  return res.json() as Promise<ResearchResponse>
}
