export interface SourceMeta {
  source?: string;
  sheet_name?: string;
  row_index?: number;
  nr_pytania?: string;
  pytanie?: string;
  [key: string]: unknown;
}

export interface SourceDocument {
  content: string;
  metadata: SourceMeta;
}

export interface Message {
  id: string;
  sender: 'user' | 'bot';
  text: string;
  sources?: SourceDocument[];
  timestamp: string;
}

export interface AskResponse {
  query: string;
  answer: string;
  sources: SourceDocument[];
  retrieved_count: number;
}
