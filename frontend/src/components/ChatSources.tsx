import React from 'react';
import { BookOpen } from 'lucide-react';
import { SourceDocument } from '../types/chat';

interface ChatSourcesProps {
  sources: SourceDocument[];
}

export const ChatSources: React.FC<ChatSourcesProps> = ({ sources }) => {
  if (!sources || sources.length === 0) return null;

  return (
    <div className="mt-2.5 pt-2 border-t border-slate-100 text-[11px]">
      <div className="flex items-center gap-1 text-indigo-600 font-semibold mb-1">
        <BookOpen className="w-3 h-3" />
        <span>Źródła z bazy Excel:</span>
      </div>
      <div className="flex flex-wrap gap-1">
        {sources.map((src, idx) => {
          const meta = src.metadata || {};
          const nr = meta.nr_pytania || meta.row_index || idx + 1;
          const sheet = meta.sheet_name || 'FAQ';
          return (
            <span
              key={idx}
              className="inline-block px-1.5 py-0.5 rounded bg-slate-100 text-slate-600 border border-slate-200 text-[10px] font-mono cursor-default hover:bg-slate-200 transition-colors"
              title={src.content}
            >
              {sheet} #{nr}
            </span>
          );
        })}
      </div>
    </div>
  );
};

export default ChatSources;
