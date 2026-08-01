import { AskResponse } from '../types/chat';

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000';

/**
 * Service to communicate with the FastAPI RAG backend.
 */
export async function askQuestion(query: string): Promise<AskResponse> {
  const response = await fetch(`${API_BASE_URL}/api/v1/ask`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({ query }),
  });

  if (!response.ok) {
    const errorData = await response.json().catch(() => ({}));
    throw new Error(
      errorData.detail || `Błąd serwera (${response.status}: ${response.statusText})`
    );
  }

  return response.json();
}
