import React, { useState, useRef, useEffect } from 'react';
import { SendHorizontal } from 'lucide-react';

interface ChatInputProps {
  onSend: (text: string) => void;
  disabled?: boolean;
}

export const ChatInput: React.FC<ChatInputProps> = ({ onSend, disabled = false }) => {
  const [text, setText] = useState<string>('');
  const inputRef = useRef<HTMLInputElement>(null);

  useEffect(() => {
    if (!disabled) {
      inputRef.current?.focus();
    }
  }, [disabled]);

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    const trimmed = text.trim();
    if (!trimmed || disabled) return;

    onSend(trimmed);
    setText('');
  };

  return (
    <div className="p-3 bg-white border-t border-slate-200">
      <form onSubmit={handleSubmit} className="flex items-center gap-2">
        <input
          ref={inputRef}
          type="text"
          value={text}
          onChange={(e) => setText(e.target.value)}
          placeholder="Type your message..."
          className="flex-1 bg-slate-100 hover:bg-slate-100/80 focus:bg-white text-slate-800 placeholder-slate-400 text-sm px-4 py-2.5 rounded-xl border border-transparent focus:border-indigo-500 focus:outline-none transition-all"
          disabled={disabled}
        />
        <button
          type="submit"
          disabled={!text.trim() || disabled}
          className="w-10 h-10 rounded-xl bg-indigo-600 hover:bg-indigo-700 text-white flex items-center justify-center shadow-md shadow-indigo-600/20 disabled:opacity-40 disabled:cursor-not-allowed transition-all hover:scale-105 active:scale-95 shrink-0 cursor-pointer"
          aria-label="Send message"
          title="Send message"
        >
          <SendHorizontal className="w-4 h-4" />
        </button>
      </form>
      <div className="text-center mt-2 text-[10px] text-slate-400 font-medium select-none">
        Powered by <b>Llama 3.2 3B</b> & <b>ChromaDB</b>
      </div>
    </div>
  );
};

export default ChatInput;
