import React from 'react';
import { Bot } from 'lucide-react';

export const ChatTypingIndicator: React.FC = () => {
  return (
    <div className="flex gap-2.5 max-w-[85%] mr-auto items-center">
      <div className="w-7 h-7 rounded-full bg-indigo-100 text-indigo-700 flex items-center justify-center shrink-0 text-xs">
        <Bot className="w-3.5 h-3.5" />
      </div>
      <div className="bg-white border border-slate-200/80 px-4 py-2.5 rounded-2xl rounded-tl-none shadow-sm flex items-center gap-1.5">
        <span className="w-2 h-2 rounded-full bg-indigo-500 animate-bounce [animation-delay:-0.3s]"></span>
        <span className="w-2 h-2 rounded-full bg-indigo-500 animate-bounce [animation-delay:-0.15s]"></span>
        <span className="w-2 h-2 rounded-full bg-indigo-500 animate-bounce"></span>
      </div>
    </div>
  );
};

export default ChatTypingIndicator;
