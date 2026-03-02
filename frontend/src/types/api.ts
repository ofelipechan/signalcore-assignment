/** Request body for POST /api/research */
export interface ResearchRequest {
  prompt: string
}

/** Source provenance from the API */
export interface Source {
  url: string
  title?: string | null
  source_type?: string | null
}

/** Response from POST /api/research */
export interface ResearchResponse {
  markdown: string
  sources: Source[]
}
